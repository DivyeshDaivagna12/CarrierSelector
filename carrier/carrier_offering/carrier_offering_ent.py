from ast import List
import json
from carrier_offering.carrier_offering_dtos import *

class CarrierOfferingEntity():
    description:str
    carrier: str
    offering: str
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->CarrierOfferingDetailDto:
        dto = CarrierOfferingDetailDto()
        dto.description = self.description
        dto.carrier = self.carrier
        dto.offering = self.offering
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:CarrierOfferingSetDto):
        self.description = dto.description
        self.carrier = dto.carrier
        self.offering = dto.offering
        self.is_active = dto.is_active
        return self
