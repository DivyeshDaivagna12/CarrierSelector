from customer_pricing.customer_pricing_ent import CustomerPricingEntity
from customer_pricing.customer_pricing_dtos import *
from customer_pricing.common_methods.not_found_exce import ResourceNotFoundException
from customer_pricing.i_customer_pricing_repo import ICustomerPricingRepository

class CustomerPricingService:
    def __init__(self, repo: ICustomerPricingRepository):
        self.repo = repo
 
    def set(self, dto: CustomerPricingSetDto)->None:
        enty = CustomerPricingEntity()              
        enty.set(dto)
        self.repo.save(enty)

    def get(self, rateCode:str,productId:str)->CustomerPricingDetailDto:
        enty = self.repo.get_by_productId(rateCode,productId)
        if enty is None:
            raise ResourceNotFoundException(f"RateCode{rateCode} and ProductId{productId} not found")
        return enty.to_dto()

    def get_all(self,productId:str)->list[CustomerPricingDetailDto]:
        list_dto = list()
        entities = self.repo.get_all(productId)
        for enty in entities:
            try:
                list_dto.append(enty.to_dto())
            except:
                pass
        return list_dto
 