from uuid import uuid4
from  domain.entities.customer_surcharge_discount_ent import CustomerSurchargeDiscountEntity
from domain.dtos.customer_surcharge_discount_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_customer_surcharge_discount_repo import ICustomerSurchargeDiscountRepository

class CustomerSurchargeDiscountService:
    def __init__(self, repo: ICustomerSurchargeDiscountRepository):
        self.repo = repo
 
    def set(self, dto: CustomerSurchargeDiscountSetDto)->None:
        enty = CustomerSurchargeDiscountEntity()
        enty.set(dto)
        self.repo.save(enty)
    
    def create(self, dto: CustomerSurchargeDiscountSetDto)->None:
        enty = CustomerSurchargeDiscountEntity()
        enty.set(dto)
        self.repo.create(enty)

    def get(self, customer: str,surcharge:str)->CustomerSurchargeDiscountDetailDto:
       enty = self.repo.get(customer,surcharge)
       if enty is None:raise RescourceNotFoundException(f"Customer Service Discount not found")
       return enty.to_dto()
    
    def get_all(self)->list[CustomerSurchargeDiscountDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 