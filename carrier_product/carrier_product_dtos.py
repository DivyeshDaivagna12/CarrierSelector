
from ast import List
import decimal
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class CarrierProductDetailDto:
        description:str
        carrier:str
        product:str
        cost:float
        is_active:bool
 
class CarrierProductSetDto(BaseModel):
        carrier:str
        product:str
        cost:float
        is_active:bool

