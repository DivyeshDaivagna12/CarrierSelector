
from aws_lambda_powertools.utilities.parser import BaseModel
from typing import Optional


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

