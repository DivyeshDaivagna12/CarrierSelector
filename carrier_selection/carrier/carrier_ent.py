from ast import List
import json
from uuid import UUID
from domain.custom_encoder import CustomeEncoder
from domain.dtos.carrier_dtos import *

class CarrierEntity():
    id:str
    description:str
    weighting: str
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->CarrierDetailDto:
        dto = CarrierDetailDto()
        dto.id = self.id
        dto.description = self.description
        dto.weighting = self.weighting
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:CarrierSetDto):
        self.id = dto.id
        self.description = dto.description
        self.weighting = dto.weighting
        self.is_active = dto.is_active
        return self
