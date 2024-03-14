from ast import List
import json
from common_methods.custom_encoder import CustomeEncoder, to_custom_json
from offering.offering_dtos import *

class OfferingEntity():
    id:str
    description:str
    carrier: str
    status: str # Values: "RELEASED" or "PLANNING"
    version: int
    valid_from: int
    valid_to: int
    product: str
    cost: CostDto
    transit_time: str
    services: List[str]
    is_active: bool
    
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->OfferingDetailDto:
        dto = OfferingDetailDto()
        dto.id = self.id
        dto.description = self.description
        dto.carrier = self.carrier
        dto.status = self.status
        dto.version = self.version
        dto.valid_from = self.valid_from
        dto.valid_to = self.valid_to
        dto.product = self.product
        dto.cost= json.loads(self.cost)
        dto.transit_time = self.transit_time
        dto.services = self.services
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:OfferingSetDto):
        self.id = dto.id
        self.description = dto.description
        self.carrier = dto.carrier
        self.status = dto.status
        self.version = dto.version
        self.valid_from = dto.valid_from
        self.valid_to = dto.valid_to
        self.product = dto.product
        self.cost = to_custom_json(dto.cost)
        self.transit_time = dto.transit_time
        self.services = dto.services
        self.is_active = dto.is_active
        return self
    
    # def to_cost_model(self)->OfferingDetailDto:
    #     dto = self.to_dto()
    #     dto.cost = CostDto.model_construct(CostDto.model_fields_set, **dto.cost)
    #     scalePiece = None
    #     scaleSkid = None
      
    #     if dto.cost.scale_piece is not None:
    #       scalePiece = ScalePiece.model_construct(ScalePiece.model_fields_set, **dto.cost.scale_piece)
    #     if dto.cost.scale_skid is not None:
    #       scaleSkid = ScaleSkid.model_construct(ScaleSkid.model_fields_set, **dto.cost.scale_skid)
          
    #     dto.cost = CostDto.model_construct(scale_piece=scalePiece,scale_skid=scaleSkid,method=dto.cost.method,fixed_cost=dto.cost.fixed_cost,attribute=dto.cost.attribute )
    #     return dto
