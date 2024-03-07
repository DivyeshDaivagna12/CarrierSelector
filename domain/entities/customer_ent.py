from ast import List
import json
from uuid import UUID
from domain.custom_encoder import CustomeEncoder
from domain.dtos.customer_dtos import *

class CustomerEntity():
    id:str
    description:str
    is_active:bool
    preferred_carrier: str
    excluded_carriers: []
    products: []
    services: []
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->CustomerDetailDto:
        dto = CustomerDetailDto()
        dto.id = self.id
        dto.description = self.description
        dto.is_active = self.is_active
        dto.preferred_carrier = self.preferred_carrier
        dto.excluded_carriers = self.excluded_carriers
        dto.products = self.products
        dto.services = self.services
        return dto
    
    def set(self, dto:CustomerSetDto):
        self.id = dto.id
        self.description = dto.description
        self.is_active = dto.is_active
        self.preferred_carrier = dto.preferred_carrier
        self.excluded_carriers = dto.excluded_carriers
        self.products = dto.products
        self.services = dto.services
        return self
