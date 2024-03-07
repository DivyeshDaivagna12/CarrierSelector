from uuid import uuid4
from domain.dtos.rate_master_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.exceptions.bad_request_exce import BadRequestException
from infrastructure.repositories.fsa_zone_mapping_repo import FsaZoneMappingRepository, FsaZoneMappingEntity
from infrastructure.repositories.fsa_rate_mapping_repo import FsaRateMappingRepository, FsaRateMappingEntity
from infrastructure.repositories.customer_pricing_repo import CustomerPricingRepository, CustomerPricingEntity
from infrastructure.repositories.customer_surcharge_repo import CustomerSurchargeRepository, CustomerSurchargeEntity
from infrastructure.repositories.customer_repo import CustomerRepository,CustomerEntity
from infrastructure.repositories.product_repo import ProductRepository, ProductEntity
from infrastructure.repositories.service_repo import ServiceRepository, ServiceEntity
from infrastructure.repositories.customer_product_discount_repo import CustomerProductDiscountRepository, CustomerProductDiscountEntity
from infrastructure.repositories.customer_surcharge_discount_repo import CustomerSurchargeDiscountRepository, CustomerSurchargeDiscountEntity
from domain.constants import excessive_skid_id,excessive_skid_desc, loss_packaging_id, skid_packaging_id




class RateMasterService:
    def __init__(self):
        self.fsaZoneMappingRepo = FsaZoneMappingRepository()
        self.fsaRateMappingRepo = FsaRateMappingRepository()
        self.customerPricingRepo = CustomerPricingRepository()
        self.customerSurchargeRepo = CustomerSurchargeRepository()
        self.customerRepo = CustomerRepository()
        self.productRepo = ProductRepository()
        self.serviceRepo = ServiceRepository()
        self.customerProductDiscountRepo = CustomerProductDiscountRepository()
        self.customerSurchargeDiscountRepo = CustomerSurchargeDiscountRepository()
 
    def get_pricing(self, request_dto: RateMasterSetDto)->RateMasterDetailDto:
       
        customer = self.customerRepo.get_by_id(request_dto.customer_number)
        if customer is None:
           raise BadRequestException(f"Customer with id '{request_dto.customer_number}' not exist")
        
        
        product_entities = self.get_product_entities(request_dto)
        
        self.validate(request_dto,product_entities)

        rate_code_entity = self.get_rate_code(request_dto)
    
        
        final_result_array = []
        
        for i in range(len(request_dto.product_details)):
           
            final_dict = self.get_pricing_for_product(product_entities[i], request_dto, request_dto.product_details[i], rate_code_entity)
            final_result_array.append(final_dict)
            
        final_total_amount = 0
        for final_result in final_result_array:
            final_total_amount += final_result.total_amount
        
        final_total_amount = float("{:.2f}".format(final_total_amount))

        final_return_dto = RateMasterDetailDto()
        final_return_dto.pricing= final_result_array
        final_return_dto.final_total_amount = final_total_amount

        return final_return_dto


    def get_excessive_skid_price(self):
        excessive_skid_price = 0
        excessiveSkidPriceSurchargeEntity = self.customerSurchargeRepo.get_by_service(excessive_skid_id)
        if (excessiveSkidPriceSurchargeEntity is not None) and (excessiveSkidPriceSurchargeEntity.is_active):
            excessive_skid_price = float(excessiveSkidPriceSurchargeEntity.price)
        else:
            raise RescourceNotFoundException(f"Pricing for surcharge '{excessive_skid_desc}' not exist or it is inactive.")
        return excessive_skid_price

    def get_pricing_for_product(self, product_entity: ProductEntity, request_dto: RateMasterSetDto, product_detail: ProductDetail, rate_code_entity: FsaRateMappingEntity):
        # product_entity = product_entities[i]
        skids = product_detail.skids
        pieces = product_detail.pieces
        product = product_detail.product
        services = product_detail.services

        discount_pricing = self.customerProductDiscountRepo.get(request_dto.customer_number,product,rate_code_entity.rate_code)
        additional_piece_discount = 0
        try:
            if discount_pricing:
                if discount_pricing.additional_piece_discount:
                    additional_piece_discount =discount_pricing.additional_piece_discount
                else:
                    additional_piece_discount = 0
        except:
            additional_piece_discount =0

        pricing = self.customerPricingRepo.get_by_productId(rate_code_entity.rate_code, product)
        
        if pricing is None:
            raise RescourceNotFoundException(f"Pricing for product '{product_entity.description}' and for rate code '{rate_code_entity.rate_code}' not exist.")
        
        product_cost, service_id_array, surcharges_cost_detail,product_cost_additional = self.calculate_base_charges_for_product_and_services(skids, pieces, services, product_entity, pricing,additional_piece_discount)
        
        
        final_dto= ProductRateDetailDto()
        final_dto.base_product_cost = product_cost
        final_dto.base_surcharges_cost = surcharges_cost_detail
  

        product_discount_dict = self.get_product_discount_percentage_detail(product_entity, request_dto, product, rate_code_entity)
        surcharges_discount_percentage_detail = self.get_surcharges_discount_percentage_details(surcharges_cost_detail, request_dto, service_id_array)

        discount_percentage_dict = DiscountPercentage()
        discount_percentage_dict.product_discount_percentage = product_discount_dict
        discount_percentage_dict.surcharges_discount_percentage = surcharges_discount_percentage_detail
        final_dto.discount_percentage = discount_percentage_dict

        product_discount_in_dollar_dict = self.get_product_discount_amount_detail(product_entity, product_discount_dict, product_cost,product_cost_additional)
        surcharges_discount_in_dollar_detail = self.get_surcharges_discount_amount_details(surcharges_cost_detail, surcharges_discount_percentage_detail)
        
        discount_amount = DiscountAmount()
        discount_amount.product_discount_amount = product_discount_in_dollar_dict
        discount_amount.surcharges_discount_amount = surcharges_discount_in_dollar_detail
        final_dto.discount_amount = discount_amount

        product_final_price_dict = self.get_product_final_price_detail(product_entity, product_cost, product_discount_in_dollar_dict,product_cost_additional)
        surcharges_final_price_detail = self.get_surcharges_final_price_details(surcharges_cost_detail, surcharges_discount_in_dollar_detail)
        
        final_price = FinalPrice()
        final_price.product_final_price = product_final_price_dict
        final_price.surcharges_final_price = surcharges_final_price_detail
        final_dto.final_price = final_price
    

        total = 0
        total += float(product_final_price_dict.final_product_price)

        for i in range(len(surcharges_cost_detail)):
            total += float(surcharges_final_price_detail[i].surcharge_final_price)
        
        final_dto.total_amount = float("{:.2f}".format(total))
        # print(final_dto)
        return final_dto
    
    def get_surcharges_final_price_details(self, surcharges_cost_detail, surcharges_discount_in_dollar_detail):
        surcharges_final_price_details = []
        for i in range(len(surcharges_cost_detail)):
            surcharge_final_price_dto = SurchargeFinalPrice()
            surcharge_final_price_dto.surcharge_name = surcharges_cost_detail[i].surcharge_name
            s_p_price = float(surcharges_cost_detail[i].surcharge_cost - surcharges_discount_in_dollar_detail[i].surcharge_discount_amount)
            surcharge_final_price_dto.surcharge_final_price = float("{:.2f}".format(s_p_price))
            surcharges_final_price_details.append(surcharge_final_price_dto)
        return surcharges_final_price_details

    def get_product_final_price_detail(self, product_entity: ProductEntity, product_cost: float, product_discount_in_dollar_dict: ProductDiscountAmount,product_cost_additional:float):
        product_final_price_dto = ProductFinalPrice()
        product_final_price_dto.product_name = product_entity.description
        f_p_price = float(product_cost - product_discount_in_dollar_dict.product_discount_amount)+float(product_cost_additional)
        product_final_price_dto.final_product_price = float("{:.2f}".format(f_p_price))
        return product_final_price_dto
    
    def get_surcharges_discount_amount_details(self, surcharges_cost_detail: list[SurchargeBaseCost], surcharges_discount_percentage_detail: list[SurchargesDiscountPercentage]):
        surcharges_discount_amount_details = []
        for i in range(len(surcharges_cost_detail)):
            surcharge_discount_amount_dto = SurchargesDiscountAmount()
            surcharge_discount_amount_dto.surcharge_name = surcharges_cost_detail[i].surcharge_name
            s_d_amount = float(surcharges_cost_detail[i].surcharge_cost*float((surcharges_discount_percentage_detail[i].surcharge_discount/100)))
            surcharge_discount_amount_dto.surcharge_discount_amount = float("{:.2f}".format(s_d_amount))
            surcharges_discount_amount_details.append(surcharge_discount_amount_dto)
        return surcharges_discount_amount_details

    def get_product_discount_amount_detail(self, product_entity: ProductEntity, product_discount_dict:ProductDiscountPercentage, product_cost: float,product_cost_additional:float):
        product_discount_amount_dto = ProductDiscountAmount()
        product_discount_amount_dto.product_name = product_entity.description
        p_d_amount = float(product_cost*float((product_discount_dict.product_discount/100))) 
        product_discount_amount_dto.product_discount_amount = float("{:.2f}".format(p_d_amount))
        return product_discount_amount_dto

    def get_surcharges_discount_percentage_details(self, surcharges_cost_detail: list[SurchargeBaseCost], request_dto: RateMasterSetDto, service_id_array):
        surcharges_discount_percentage_detail = []
        index = 0
        for surcharge_detail in surcharges_cost_detail:
            surchargeDiscount = self.customerSurchargeDiscountRepo.get(request_dto.customer_number,service_id_array[index])
            surcharge_discount_dto = SurchargesDiscountPercentage()
            if (surchargeDiscount is not None) and surchargeDiscount.is_active:
                # print(productDiscount.discount)
                surcharge_discount_dto.surcharge_name = surcharge_detail.surcharge_name
                surcharge_discount_dto.surcharge_discount = float(surchargeDiscount.discount)
            else:
                surcharge_discount_dto.surcharge_name = surcharge_detail.surcharge_name
                surcharge_discount_dto.surcharge_discount = float(0)
            
            surcharges_discount_percentage_detail.append(surcharge_discount_dto)
            index += 1
        return surcharges_discount_percentage_detail
    
    def get_product_discount_percentage_detail(self, product_entity: ProductEntity, request_dto: RateMasterSetDto, product: str, rate_code_entity: FsaRateMappingEntity ):
        product_discount_dto = ProductDiscountPercentage()

        productDiscount = self.customerProductDiscountRepo.get(request_dto.customer_number,product,rate_code_entity.rate_code)        
        if (productDiscount is not None) and (productDiscount.is_active) :
            # print(productDiscount.discount)
            product_discount_dto.product_name = product_entity.description
            product_discount_dto.product_discount = float(productDiscount.discount)
        else:
            # print(productDiscount)
            productDiscount = self.customerProductDiscountRepo.get(request_dto.customer_number,product, None)
            # print(productDiscount.discount)
            if productDiscount is not None and (productDiscount.is_active):
                product_discount_dto.product_name = product_entity.description
                product_discount_dto.product_discount = float(productDiscount.discount)
            else:
                product_discount_dto.product_name = product_entity.description
                product_discount_dto.product_discount = float(0)
        return product_discount_dto
    
    def calculate_base_charges_for_product_and_services(self, skids: int, pieces: int, services, product_entity: ProductEntity, pricing: CustomerPricingEntity,additional_piece_discount :float):
        service_id_array = []
        surcharges_cost_detail = []
        product_cost_additional = 0
        if product_entity.packaging == skid_packaging_id:   
            if skids <= 6:
                if skids <= 2:
                    product_cost = float(pricing.one_to_two_skid_space)
                elif skids <= 4:
                    product_cost = float(pricing.three_to_four_skid_space)
                elif skids <= 6:
                    product_cost = float(pricing.five_to_six_skid_space)
            elif skids > 6:
                excessive_skid_price = self.get_excessive_skid_price()
                product_cost = float(pricing.five_to_six_skid_space)
                service_dto = SurchargeBaseCost()
                service_dto.surcharge_name = excessive_skid_desc
                service_id_array.append(excessive_skid_id)
                s_cost = float(excessive_skid_price*(skids-6))
                service_dto.surcharge_cost = float("{:.2f}".format(s_cost))
                surcharges_cost_detail.append(service_dto)
        elif product_entity.packaging == loss_packaging_id:
       
            product_cost = 0
            pieces = pieces
            if pieces <= 1 :
                product_cost = float(pricing.first_loose_piece)
            elif pieces > 1:
                product_cost = float(pricing.first_loose_piece)
                product_cost_additional = (float(pricing.first_loose_piece) - float((float(pricing.first_loose_piece))*(float(float(additional_piece_discount)/100))))*(pieces-1)
       
        product_cost = float("{:.2f}".format(product_cost))

        for service in services:
            service_entity = self.serviceRepo.get_by_id(service)
            if (service_entity is None) :
                raise BadRequestException(f"Services is not available")
            surcharge_entity = self.customerSurchargeRepo.get_by_service(service)
            if surcharge_entity is None or (not surcharge_entity.is_active):
                raise RescourceNotFoundException(f"Pricing for surcharge '{service_entity.description}' not exists or it is inactive")
            service_dto = SurchargeBaseCost()
            service_dto.surcharge_name = service_entity.description
            service_id_array.append(service)
            service_dto.surcharge_cost = float(surcharge_entity.price)
            surcharges_cost_detail.append(service_dto)

        return product_cost, service_id_array, surcharges_cost_detail,product_cost_additional
    
    def get_rate_code(self, request_dto: RateMasterSetDto):
        origin_fsa = request_dto.origin_fsa[:3]
        destination_fsa = request_dto.destination_fsa[:3]

        origin_zone_entity = self.fsaZoneMappingRepo.get_by_origin(origin_fsa)
        if origin_zone_entity is None:
            raise RescourceNotFoundException(f"Origin fsa not found")
        rate_code_entity = self.fsaRateMappingRepo.get_by_origin(destination_fsa, origin_zone_entity.origin_zone)
        if rate_code_entity is None:
            raise RescourceNotFoundException(f"Origin zone - '{origin_zone_entity.origin_zone}' to destination fsa - '{destination_fsa}' mapping not found")
        return rate_code_entity
    
    def get_product_entities(self, request_dto: RateMasterSetDto):

        product_entities = []
        for product_detail in request_dto.product_details:
            product_entity = self.productRepo.get_by_id(product_detail.product)
            product_entities.append(product_entity)
        
        return product_entities


    def validate(self, dto: RateMasterSetDto, product_entities: List[ProductEntity]):
                        
        for i in range(len(product_entities)):
            product = product_entities[i]
            skids = dto.product_details[i].skids
            pieces = dto.product_details[i].pieces
            if product is not None:
                if (skids is None or skids == 0) and (pieces is None or pieces == 0):
                    raise BadRequestException(f"Request for Product '{product.description}' has both skids and pieces None or 0")
                
                if (skids is not None and skids > 0) and (pieces is not None and pieces > 0):
                    raise BadRequestException(f"Request for Product '{product.description}' has both skids and pieces count greater than 0")
                
                if product.packaging not in [loss_packaging_id, skid_packaging_id]:
                    raise BadRequestException(f"Packaging type 'SKID' and 'LOOSE' is only supported. Product '{product.description}' is not of packaging type 'SKID' or 'LOOSE'")

                if product.packaging == loss_packaging_id and (pieces is None or pieces == 0):
                    raise BadRequestException(f"Product {product.description} is of packaging type 'LOOSE' but requested no. of pieces is 0 or None")
                
                if product.packaging == skid_packaging_id and (skids is None or skids == 0):
                    raise BadRequestException(f"Product {product.description} is of packaging type 'SKID' but requested no. of skids is 0 or None")
            else:
                raise BadRequestException(f"Product with id '{dto.product_details[i].product}' doesnt exist")
        

    # def get(self, id: str)->RateMasterDetailDto:
    #    enty = self.repo.get_by_id(id)
    #    if enty is None:raise RescourceNotFoundException(f"RateMaster {id} not found")
    #    return enty.to_dto()
    
    # def get_all(self)->list[RateMasterDetailDto]:
    #    list_dto = list()
    #    entities = self.repo.get_all()
    #    for enty in entities:
    #       try:
    #         list_dto .append(enty.to_dto())
    #       except:
    #        pass
    #    return list_dto
 
