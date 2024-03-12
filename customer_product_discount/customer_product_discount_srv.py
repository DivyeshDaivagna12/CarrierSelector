from uuid import uuid4
from customer_product_discount.customer_product_discount_ent import CustomerProductDiscountEntity
from customer_product_discount.customer_product_discount_dtos import *
from common_methods.not_found_exce import RescourceNotFoundException
from i_customer_product_discount_repo import ICustomerProductDiscountRepository

class CustomerProductDiscountService:
    def __init__(self, repo: ICustomerProductDiscountRepository):
        self.repo = repo
 
    def set(self, dto: CustomerProductDiscountSetDto)->None:
        enty = CustomerProductDiscountEntity()
        enty.set(dto)
        self.repo.save(enty)
    
    def create(self, dto: CustomerProductDiscountSetDto)->None:
        enty = CustomerProductDiscountEntity()
        enty.set(dto)
        self.repo.create(enty)

    def get(self, customer: str,product:str,rate_code:str)->CustomerProductDiscountDetailDto:
       enty = self.repo.get(customer,product,rate_code)
       if enty is None:raise RescourceNotFoundException(f"CustomerProductDiscount not found")
       return enty.to_dto()
    
    def get_all(self)->list[CustomerProductDiscountDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          additional_discount = 0
          try:
            if not enty.additional_piece_discount:
               enty.additional_piece_discount = additional_discount
          except:
             enty.additional_piece_discount = additional_discount
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 
