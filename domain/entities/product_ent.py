from ast import List
import json
from uuid import UUID
from domain.custom_encoder import CustomeEncoder, to_custom_json
from domain.dtos.product_dtos import *

class ProductEntity():
    id:str
    description:str
    family:str
    packaging:str
    services : List[str]
    constraints: List[ConstraintDto]
    time_definite: str
    is_restricted: bool
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->ProductDetailDto:
        dto = ProductDetailDto()
        dto.id = self.id
        dto.description = self.description
        dto.family = self.family
        dto.packaging = self.packaging
        dto.services = self.services
        dto.constraints = self.constraints
        dto.time_definite = self.time_definite
        dto.is_restricted = self.is_restricted
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:ProductSetDto):
        self.id = dto.id
        self.description = dto.description
        self.family = dto.family
        self.packaging = dto.packaging
        self.services = dto.services
        self.constraints =  to_custom_json(dto.constraints)
        self.time_definite = dto.time_definite
        self.is_restricted = dto.is_restricted
        self.is_active = dto.is_active
        return self
