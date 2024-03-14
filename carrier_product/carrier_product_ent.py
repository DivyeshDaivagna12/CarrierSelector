from common_methods.custom_encoder import CustomeEncoder
from carrier_product.carrier_product_dtos import *


class CarrierProductEntity():
    description:str
    carrier:str
    product:str
    cost:str
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->CarrierProductDetailDto:
        dto = CarrierProductDetailDto()
        dto.description = self.description
        dto.carrier = self.carrier
        dto.product = self.product
        dto.cost = float(self.cost)
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:CarrierProductSetDto):
        self.description = dto.carrier+dto.product
        self.carrier = dto.carrier
        self.product = dto.product
        self.cost = str(dto.cost)
        self.is_active = dto.is_active
        return self
