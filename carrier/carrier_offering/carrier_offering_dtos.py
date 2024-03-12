
from ast import List
from pydantic import BaseModel
from typing import List, Optional


class CarrierOfferingDetailDto:
        description:str
        carrier: str
        offering: str
        is_active:bool
 
class CarrierOfferingSetDto(BaseModel):
        description:str
        carrier: str
        offering: str
        is_active:bool

