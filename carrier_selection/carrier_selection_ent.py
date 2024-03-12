from ast import List
from carrier_selection.carrier_selection_dtos import *

class CarrierSelectionEntity():
    lane: str
    lane_name: str
    carrier_from_zone: str
    carrier_to_zone: str
    shipment_date: int
    carrier: str
    carrier_name: str
    cost: float
    existing_lanes_name: List[str]
    transit_time: str
    customer_id: str
    customer_name: str
    
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->CarrierSelectionDetailDto:
        dto = CarrierSelectionDetailDto()
        # dto.lane_id = self.lane
        # dto.lane_name = self.lane_name
        dto.carrier_from_zone = self.carrier_from_zone
        dto.carrier_to_zone = self.carrier_to_zone
        dto.shipment_date = self.shipment_date
        dto.route_number = self.carrier
        dto.carrier_name = self.carrier_name
        # dto.cost = self.cost
        dto.transit_time = self.transit_time
        dto.customer_id = self.customer_id
        dto.customer_name = self.customer_name
        return dto
    
    # def set(self, dto:CarrierSelectionSetDto):
    #     self.id = dto.id
    #     self.description = dto.description
    #     self.carrier = dto.carrier
    #     self.status = dto.status
    #     self.version = dto.version
    #     self.valid_from = dto.valid_from
    #     self.valid_to = dto.valid_to
    #     self.product = dto.product
    #     self.cost = to_custom_json(dto.cost)
    #     self.transit_time = dto.transit_time
    #     self.services = dto.services
    #     return self
