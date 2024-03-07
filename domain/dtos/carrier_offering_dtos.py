
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
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

