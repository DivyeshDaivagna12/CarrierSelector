
from pydantic import BaseModel
from typing import Optional


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
