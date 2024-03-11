
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class CustomerSurchargeDiscountDetailDto:
        customer:str
        surcharge:str
        discount:str
        is_active:bool
 
class CustomerSurchargeDiscountSetDto(BaseModel):
        customer:Optional[str]
        surcharge:str
        discount:str
        is_active:bool

