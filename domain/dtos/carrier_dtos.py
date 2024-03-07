
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class CarrierDetailDto:
        id:str
        description:str
        weighting: Optional[str]
        is_active:bool
 
class CarrierSetDto(BaseModel):
        id:str
        description:str
        weighting: Optional[str]
        is_active:bool

