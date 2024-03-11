
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class CustomerProductDiscountDetailDto:
        product:str
        customer:str
        rate_code:str
        discount:str
        is_active:bool
        additional_piece_discount:str
 
class CustomerProductDiscountSetDto(BaseModel):
        product:str
        customer:str
        rate_code:Optional[str]
        discount:str
        is_active:bool
        additional_piece_discount:str

