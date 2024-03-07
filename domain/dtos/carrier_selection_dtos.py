
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class ProductDetail(BaseModel):
        product: str
        services: List[str]
        skids: Optional[int]
        pieces: Optional[int]

class CarrierSelectionDetailDto:
        lane_id: str
        shipment_date: int
        lane_name: str
        carrier_from_zone: str
        carrier_to_zone: str
        route_number: str
        carrier_name: str
        transit_time: str
        cost: float
        weighting: float
        customer_id: str
        customer_name: str
        
 
class CarrierSelectionSetDto(BaseModel):
        origin_address: str
        destination_address: str
        shipment_date: int
        customer: str
        product_details: List[ProductDetail]
