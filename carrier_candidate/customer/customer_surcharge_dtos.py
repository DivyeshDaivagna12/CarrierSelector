
from ast import List
from pydantic import BaseModel
from typing import List, Optional


class CustomerSurchargeDetailDto:
        service:str
        price:float
        is_active:bool
 
class CustomerSurchargeSetDto(BaseModel):
        service:str
        price:float
        is_active:bool
