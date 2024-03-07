from ast import List
import json
from uuid import UUID
from domain.custom_encoder import CustomeEncoder
from domain.dtos.packaging_dtos import *

class PackagingEntity():
    id:str
    description:str
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->PackagingDetailDto:
        dto = PackagingDetailDto()
        dto.id = self.id
        dto.description = self.description
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:PackagingSetDto):
        self.id = dto.id
        self.description = dto.description
        self.is_active = dto.is_active
        return self
