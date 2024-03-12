
from rate_master.customer_surcharge.customer_surcharge_dtos import CustomerSurchargeDetailDto, CustomerSurchargeSetDto


class CustomerSurchargeEntity():
    service:str
    price:str
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->CustomerSurchargeDetailDto:
        dto = CustomerSurchargeDetailDto()
        dto.service = self.service
        dto.price = float(self.price)
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:CustomerSurchargeSetDto):
        self.service = dto.service
        self.price = str(dto.price)
        self.is_active = dto.is_active
        return self
