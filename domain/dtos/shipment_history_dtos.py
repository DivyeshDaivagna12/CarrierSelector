
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


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

