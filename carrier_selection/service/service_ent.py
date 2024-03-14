from common_methods.custom_encoder import CustomeEncoder
from service.service_dtos import *

class ServiceEntity():
    id:str
    description:str
    constraints:[]
    is_restricted: bool
    is_system: bool
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->ServiceDetailDto:
        dto = ServiceDetailDto()
        dto.id = self.id
        dto.is_system = self.is_system
        dto.description = self.description
        dto.constraints = self.constraints
        dto.is_restricted = self.is_restricted
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:ServiceSetDto):
        self.id = dto.id
        self.is_system=False
        self.description = dto.description
        cn =json.dumps(dto.constraints, separators=(",", ":"), cls=CustomeEncoder)
        self.constraints =  cn
        self.is_restricted = dto.is_restricted
        self.is_active = dto.is_active
        return self
