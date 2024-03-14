from carrier_selection.carrier_selection_dtos import *
from shared import *
from carrier_selection.offering.offering_dtos import OfferingDetailDto
from common_methods.not_found_exce import RescourceNotFoundException
from carrier_selection.zone.zone_srv import ZoneService
from carrier_selection.carrier_selection_ent import CarrierSelectionEntity
# from domain.services.lane_srv import LaneService
from carrier_selection.lane.lane_repo import LaneRepository,LaneEntity
from carrier_selection.offering.offering_repo import OfferingRepository
from carrier_selection.carrier.carrier_repo import CarrierRepository, CarrierEntity
from carrier_selection.service.service_repo import ServiceRepository
from carrier_selection.carrier_product.carrier_product_repo import CarrierProductRepository
from carrier_selection.customer.customer_repo import CustomerRepository,CustomerEntity
from carrier_selection.product.product_repo import ProductRepository
from carrier_selection.zone.zone_repo import *
from carrier_selection.shipment.shipment_history_repo import ShipmentHistoryRepository
from common_methods.constants import excessive_skid_id,excessive_skid_desc, loss_packaging_id, skid_packaging_id
from common_methods.bad_request_exce import BadRequestException
import re


class CarrierSelectionService:
    def __init__(self):
        
        self.laneRepo = LaneRepository()
        self.offeringRepo = OfferingRepository()
        self.carrierRepo = CarrierRepository()
        self.carrierProductRepo = CarrierProductRepository()
        self.customerRepo = CustomerRepository()
        self.productRepo = ProductRepository()
        self.shipmentHistoryRepo = ShipmentHistoryRepository()
        self.serviceRepo = ServiceRepository()
        repo = ZoneRepository()
        self.zs = ZoneService(repo)
        self.matched_lanes_dict = None
        self.vaild_offerings_for_shipment_date_dict = None
 
    def selection(self, request_dto: CarrierSelectionSetDto)->CarrierSelectionDetailDto:
       
       customer = self.customerRepo.get_by_id(request_dto.customer)
       if customer is None:
           raise BadRequestException(f"Customer with id '{request_dto.customer}' not exist")
       
       self.validate(request_dto)

       probable_lanes_ids = self.get_propable_lanes(request_dto.origin_address, request_dto.destination_address)

       matched_lanes = self.get_matched_lanes(probable_lanes_ids)
    
       self.vaild_offerings_for_shipment_date_dict = self.get_vaild_offerings_for_shipment_date(request_dto)
   
       eligible_carrier_offerings = self.find_eligible_carrier_offerings(matched_lanes,request_dto, customer)
    
       if len(eligible_carrier_offerings) == 0:
           raise RescourceNotFoundException(f"No carrier found for shipment")


       result = self.check_preferred_carrier(customer, eligible_carrier_offerings)
       if result is not None:
           return result 
       
       result = self.check_shipment_already_exist_for_sameday(request_dto, eligible_carrier_offerings)  
       if result is not None:
           return result

       filtered_eligible_lanes = self.filter_by_excluded_carriers(customer, eligible_carrier_offerings)
       
       if len(filtered_eligible_lanes) == 0:
           raise RescourceNotFoundException(f"After removing exculded carriers. No carrier found for shipment")
       elif len(filtered_eligible_lanes) == 1:
           return CarrierSelectionEntity(filtered_eligible_lanes[0]).to_dto()
       # factor calculation
       elif len(filtered_eligible_lanes) > 1:
           return self.factor_calculation_and_get_minimum_factor_eligible_lane(filtered_eligible_lanes)


    def filter_by_excluded_carriers(self, customer: CustomerEntity, eligible_carrier_offerings):
        updated_eligible_lanes= []
       # remove excluded carriers
        for carrier_offering in eligible_carrier_offerings:
            if (customer.excluded_carriers is None) or (carrier_offering["carrier"] not in customer.excluded_carriers):
                updated_eligible_lanes.append(carrier_offering)
        return updated_eligible_lanes

    def check_preferred_carrier(self, customer:CustomerEntity, eligible_carrier_offerings):
       # check for preffered carrier
        for carrier_offering in eligible_carrier_offerings:
            if customer.preferred_carrier is not None and carrier_offering["carrier"] == customer.preferred_carrier:
                return CarrierSelectionEntity(carrier_offering).to_dto()
            
        return None

    def check_shipment_already_exist_for_sameday(self, request_dto:CarrierSelectionSetDto, eligible_carrier_offerings):
       # get shipment history for this date and customer
        shipment_histories = self.shipmentHistoryRepo.get_by_shipment_date_and_customer(request_dto.shipment_date, request_dto.customer)
       
       # check for same day shipment history to same customer on this date and same address
        if len(shipment_histories) > 0:
             for carrier_offering in eligible_carrier_offerings:
                 for shipment_history in shipment_histories:
                     shipment_history_dict = shipment_history.__dict__
                     if request_dto.origin_address == shipment_history_dict["origin_address"] and carrier_offering["carrier"] == shipment_history_dict["carrier_id"]:
                         return CarrierSelectionEntity(carrier_offering).to_dto()
        
        return None

    def get_vaild_offerings_for_shipment_date(self, request_dto:CarrierSelectionSetDto):
        all_offering_entities = self.offeringRepo.get_all()
 
        shipment_date = request_dto.shipment_date 
        offering_dict = dict()
       
       # getting offering released version which is applicable to requested shipment date 
        for offering_entity in all_offering_entities:
          try:
            if offering_entity.is_active:
              pass
          except:
            offering_entity.is_active = True 
               
         #  if not (offering_entity.id in res_dict):
          if shipment_date >=int( offering_entity.valid_from) and shipment_date <= int(offering_entity.valid_to) and offering_entity.status == "RELEASED":
             if not (offering_entity.id in offering_dict):
                offering_dict[offering_entity.id] = offering_entity.to_dto()
 
        return offering_dict

    def get_matched_lanes(self, probable_lanes_ids):
        matched_lanes = []
        matched_lanes_dict = dict()

       # getting lanes all at one 
        all_lane_entities:list[LaneEntity] = self.laneRepo.get_all()

       # finding existing lanes out of probable lanes
        for lane_id in probable_lanes_ids:
            for lane_entity in all_lane_entities:
                if lane_entity.id == lane_id and lane_entity.is_active:
                    matched_lanes_dict[lane_id] = lane_entity
                    matched_lanes.append(lane_id)

        self.matched_lanes_dict = matched_lanes_dict
        return matched_lanes

    def get_propable_lanes(self, origin_address:str, destination_address:str):
       # getting origin zones that occupy origin address
       origin_zones = self.zs.get_zones_for_address(origin_address)

       # getting destination zones that occupy destination address
       destination_zones = self.zs.get_zones_for_address(destination_address)
       probable_lanes = []
       # creating probable lanes by combination of origin zones and destination zones
       for origin_zone in origin_zones:
            for destination_zone in destination_zones:
                probable_lanes.append(str(origin_zone.id)+"-"+str(destination_zone.id))
       return probable_lanes
           

    def validate(self, dto: CarrierSelectionSetDto):
        for product_detail in dto.product_details:
            
            product = self.productRepo.get_by_id(product_detail.product)
            if product is not None:
                if (product_detail.skids is None or product_detail.skids == 0) and (product_detail.pieces is None or product_detail.pieces == 0):
                    raise BadRequestException(f"Request for Product '{product.description}' has both skids and pieces None or 0")
                
                if (product_detail.skids is not None and product_detail.skids > 0) and (product_detail.pieces is not None and product_detail.pieces > 0):
                    raise BadRequestException(f"Request for Product '{product.description}' has both skids and pieces count greater than 0")
                
                if product.packaging not in [loss_packaging_id, skid_packaging_id]:
                    raise BadRequestException(f"Packaging type 'SKID' and 'LOOSE' is only supported. Product '{product.description}' is not of packaging type 'SKID' or 'LOOSE'")

                if product.packaging == loss_packaging_id and (product_detail.pieces is None or product_detail.pieces == 0):
                    raise BadRequestException(f"Product {product.description} is of packaging type 'LOOSE' but requested no. of pieces is 0 or None")
                
                if product.packaging == skid_packaging_id and (product_detail.skids is None or product_detail.skids == 0):
                    raise BadRequestException(f"Product {product.description} is of packaging type 'SKID' but requested no. of skids is 0 or None")
            else:
                raise BadRequestException(f"Product with id '{product_detail.product}' doesnt exist")
    
    def factor_calculation_and_get_minimum_factor_eligible_lane(self, updated_eligible_lanes):
        new_list = sorted(updated_eligible_lanes, key=lambda x: x["cost"], reverse=False)
        min_cost = new_list[0]["cost"]
        for updated_eligible_lane in updated_eligible_lanes:
            updated_eligible_lane["cost_factor"] = float(updated_eligible_lane["cost"]/min_cost)
        
        new_list = sorted(updated_eligible_lanes, key=lambda x: x["transit_time"], reverse=False)
        min_transit_time = float(new_list[0]["transit_time"])
        for updated_eligible_lane in updated_eligible_lanes:
            updated_eligible_lane["transit_time_factor"] = float(float(updated_eligible_lane["transit_time"])/min_transit_time)
        
        new_list = sorted(updated_eligible_lanes, key=lambda x: x["weighting"], reverse=True)
        max_weighting = new_list[0]["weighting"]
        for updated_eligible_lane in updated_eligible_lanes:
            updated_eligible_lane["weighting_factor"] = float(max_weighting/ updated_eligible_lane["weighting"])
        
        for updated_eligible_lane in updated_eligible_lanes:
            updated_eligible_lane["factor"] = float(updated_eligible_lane["cost_factor"]+updated_eligible_lane["transit_time_factor"]+ updated_eligible_lane["weighting_factor"])
        
        new_list = sorted(updated_eligible_lanes, key=lambda x: x["factor"], reverse=False)
       
        return CarrierSelectionEntity(new_list[0]).to_dto()
    
    def find_eligible_carrier_offerings(self, matched_lanes_ids, request_dto:CarrierSelectionSetDto, customer):
        eligible_carrier_offerings = []
        
        #iterate all matched lanes (one carrier will have only one matched lane)
    
        for lane_id in matched_lanes_ids:
           carrier = self.carrierRepo.get_by_id(self.matched_lanes_dict[lane_id].carrier)
           weighting = self.get_weighting(carrier)
           excessive_skid_price = self.get_excessive_skid_price(carrier)
           

           lane_products_ship_details = []
           #iterate all requested products and check if they are available in lane
           for product_detail in request_dto.product_details:
               found_offering = self.find_lane_offering_by_product_detail(lane_id,product_detail)
               
               if found_offering is not None:
                   offering_cost = self.find_offering_cost(carrier, found_offering, product_detail, excessive_skid_price)
                   lane_products_ship_details.append(offering_cost)
       
           
           #if all requested products & services available in lane then add it in eligible carrier offerings list  
           if len(lane_products_ship_details) == len(request_dto.product_details):
               res = dict()
               cost = 0
               transit_time = 0
               for product_ship_detail in lane_products_ship_details:
                   cost += product_ship_detail["cost"]
                   transit_time = max(transit_time, float(product_ship_detail["transit_time"]))
               lane_dict = self.matched_lanes_dict[lane_id].__dict__
               zones = lane_id.split("-")
               res["lane"] = lane_id
               res["lane_name"] = lane_dict["description"]
               res["carrier_from_zone"] = zones[0]
               res["carrier_to_zone"] = zones[1]
               res["carrier"] = carrier.id
               res["carrier_name"] = carrier.description
               res["cost"]=  cost
               res["transit_time"] = transit_time
               res["weighting"] = weighting
               res["customer_id"]= customer.id
               res["customer_name"] = customer.description
               res["shipment_date"] = request_dto.shipment_date
               existing_lanes_names = []
               
               for lane_id in matched_lanes_ids:
                   existing_lanes_names.append(self.matched_lanes_dict[lane_id].description)
               res["existing_lanes_name"] = existing_lanes_names
               eligible_carrier_offerings.append(res)
        return eligible_carrier_offerings

    def get_weighting(self, carrier:CarrierEntity):
        weighting = 1
        if (carrier.weighting is not None) and (carrier.weighting != ""):
            weighting = float(carrier.weighting)
        return weighting

    def get_excessive_skid_price(self, carrier:CarrierEntity):
        excessive_skid_price = 1.0
        carrierProductEntity = self.carrierProductRepo.get_by_carrier_product(carrier.id, excessive_skid_id)
             
        if carrierProductEntity and carrierProductEntity.cost is not None:
            excessive_skid_price = float(carrierProductEntity.cost)
            return excessive_skid_price
        else:
            raise RescourceNotFoundException(f"Costing for Carrier '{carrier.description}' and surcharge '{excessive_skid_desc}' not exists or it is inactive.")
        
    def offerning_cost_convert_dict(self,offering):
        print("---offering--", offering.__dict__)
        print("----offering.cost----", type(offering.cost))
        cost=  offering.cost 
        try:
            cost = (cost.replace('""','"').replace("null",'""'))
            cost  = re.findall('{(.*)}',cost)
            cost = json.loads('{'+cost[0]+'}')
            offering.cost = cost
            return offering
        except Exception as e:
            return e
        
    def find_offering_cost(self, carrier: CarrierEntity, found_offering: OfferingDetailDto , product_detail :ProductDetail, excessive_skid_price):
        product_ship_detail_data = dict()
        product_ship_detail_data["transit_time"] = float(found_offering.transit_time)

        
        found_offering = found_offering.__dict__
        
        #TODO:Cost type should get validate against product packaging at time of adding offering
        if found_offering["cost"]["method"] == "FIXED":
            product_ship_detail_data["cost"] = float(found_offering["cost"]["fixed_cost"])
        elif found_offering["cost"]["method"] == "SCALE" and found_offering["cost"]["attribute"] == "PIECES":
            pieces_count = product_detail.pieces
            product_ship_detail_data["cost"] = self.get_pieces_cost(found_offering, pieces_count)
        elif found_offering["cost"]["method"] == "SCALE" and found_offering["cost"]["attribute"] == "SKIDS":
             product_ship_detail_data["cost"] = self.get_skids_cost(found_offering, product_detail.skids,excessive_skid_price)
        
        for surcharge in product_detail.services:
            carrierProductEntity = self.carrierProductRepo.get_by_carrier_product(carrier.id, surcharge)
            if carrierProductEntity is not None and carrierProductEntity.is_active:
                product_ship_detail_data["cost"] += float(carrierProductEntity.cost)
            else:
                serviceEntity = self.serviceRepo.get_by_id(surcharge)
                raise RescourceNotFoundException(f"Costing for Carrier '{carrier.description}' and surcharge '{serviceEntity.description}' not exists or it is inactive.")
        return product_ship_detail_data
      
    def get_skids_cost(self,found_offering, skids_count,excessive_skid_price):
            if skids_count is not None and skids_count > 0:
                if skids_count <= 6:
                    if skids_count <= 2:
                        return float(found_offering["cost"]["scale_skid"]["two_skid_cost"])
                    elif skids_count <= 4:
                        return float(found_offering["cost"]["scale_skid"]["four_skid_cost"])                        
                    elif skids_count <= 6:
                        return float(found_offering["cost"]["scale_skid"]["six_skid_cost"])   
                else:
                    cost = float(found_offering["cost"]["scale_skid"]["six_skid_cost"])
                    left_count = skids_count-6
                    cost += excessive_skid_price*left_count
                    return cost
                
    def get_pieces_cost(self,found_offering, pieces_count):
        if pieces_count <= 4:
            if pieces_count == 1:
               return float(found_offering["cost"]["scale_piece"]["one_piece_cost"])
            if pieces_count == 2:
                return float(found_offering["cost"]["scale_piece"]["two_piece_cost"])
            if pieces_count == 3:
                return float(found_offering["cost"]["scale_piece"]["three_piece_cost"])
            if pieces_count == 4:
                return float(found_offering["cost"]["scale_piece"]["four_piece_cost"])
        else:
            cost = float(float(found_offering["cost"]["scale_piece"]["four_piece_cost"]))
            left_count = pieces_count-4
            cost += float(found_offering["cost"]["scale_piece"]["additional_piece_cost"])*left_count
            return cost
       
    
    def find_lane_offering_by_product_detail(self, lane_id, product_detail)-> OfferingDetailDto:
        
        for offering_id in  self.matched_lanes_dict[lane_id].offerings:
            if offering_id in  self.vaild_offerings_for_shipment_date_dict:
                if product_detail.product == self.vaild_offerings_for_shipment_date_dict[offering_id].product:
                    service_flag = True
                    for service in product_detail.services:
                        if service not in self.vaild_offerings_for_shipment_date_dict[offering_id].services:
                            service_flag = False
                            break
                            
                    if service_flag:
                        current_offering = self.vaild_offerings_for_shipment_date_dict[offering_id]
                        return current_offering
        return None


