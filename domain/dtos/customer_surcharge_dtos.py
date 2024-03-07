
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class CustomerSurchargeDetailDto:
        service:str
        price:float
        is_active:bool
 
class CustomerSurchargeSetDto(BaseModel):
        service:str
        price:float
        is_active:bool
