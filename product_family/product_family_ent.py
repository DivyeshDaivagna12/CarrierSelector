from ast import List
import json
from uuid import UUID
from common_methods.custom_encoder import CustomeEncoder
from product_family.product_family_dtos import *

class ProductFamilyEntity():
    id:str
    description:str
    is_active:bool
    #modify_at:int

  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->ProductFamilyDetailDto:
        dto = ProductFamilyDetailDto()
        dto.id = self.id
        dto.description = self.description
        dto.is_active = self.is_active
        #dto.modify_at = int(self.modify_at)
        return dto
    
    def set(self, dto:ProductFamilySetDto):
        self.id = dto.id
        self.description = dto.description
        self.is_active = dto.is_active
        return self
