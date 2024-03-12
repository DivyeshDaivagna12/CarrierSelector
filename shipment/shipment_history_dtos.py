from pydantic import BaseModel
class ShipmentHistoryDetailDto:
        customer:str
        origin_address:str
        shipment_id:str
        carrier_id: str
        shipment_date: int
 
class ShipmentHistorySetDto(BaseModel):
        customer:str
        origin_address:str
        shipment_id:str
        carrier_id: str
        shipment_date: int

