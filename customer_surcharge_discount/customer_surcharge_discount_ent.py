from customer_surcharge_discount.customer_surcharge_discount_dtos import *

class CustomerSurchargeDiscountEntity():
    customer:str
    surcharge:str
    discount:str
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->CustomerSurchargeDiscountDetailDto:
        dto = CustomerSurchargeDiscountDetailDto()
        dto.customer = self.customer
        dto.surcharge = self.surcharge
        dto.discount = self.discount
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:CustomerSurchargeDiscountSetDto):
        self.customer = dto.customer
        self.surcharge = dto.surcharge
        self.discount = dto.discount
        self.is_active = dto.is_active
        return self
