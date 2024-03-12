from shipment_history_dtos import *

class ShipmentHistoryEntity():
    customer:str
    origin_address:str
    shipment_id:str
    carrier_id: str
    shipment_date: int
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->ShipmentHistoryDetailDto:
        dto = ShipmentHistoryDetailDto()
        dto.customer = self.customer
        dto.origin_address = self.origin_address
        dto.shipment_id = self.shipment_id
        dto.carrier_id = self.carrier_id
        dto.shipment_date = self.shipment_date
        return dto
    
    def set(self, dto:ShipmentHistorySetDto):
        self.customer = dto.customer
        self.origin_address = dto.origin_address
        self.shipment_id = dto.shipment_id
        self.carrier_id = dto.carrier_id
        self.shipment_date = dto.shipment_date
        return self
