
from ast import List
from typing import List, Optional
from common_methods.shared import CostDto

class OfferingDetailDto:
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
        services: [List[str]]
        future: int
        expired: int
        planned: int
        is_active: bool
        
 
class OfferingSetDto:
        id:Optional[str]
        description:str
        carrier: str
        status: str # Values: "RELEASED" or "PLANNING"
        version: int
        valid_from: int
        valid_to: int
        product: str
        cost: CostDto
        transit_time: str
        services: Optional[List[str]]
        is_active: bool


