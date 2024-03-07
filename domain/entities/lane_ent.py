from ast import List
import json
from uuid import UUID
from domain.custom_encoder import CustomeEncoder
from domain.dtos.lane_dtos import *

class LaneEntity():
    id:str
    description:str
    offerings: List[str]
    origin: str
    destination: str
    carrier: str
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->LaneDetailDto:
        dto = LaneDetailDto()
        dto.id = self.id
        dto.description = self.description
        dto.offerings = self.offerings
        dto.origin = self.origin
        dto.destination = self.destination
        dto.carrier = self.carrier
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:LaneSetDto):
        self.id = dto.id
        self.description = dto.description
        self.offerings = dto.offerings
        self.origin = dto.origin
        self.destination = dto.destination
        self.carrier = dto.carrier
        self.is_active = dto.is_active
        return self
