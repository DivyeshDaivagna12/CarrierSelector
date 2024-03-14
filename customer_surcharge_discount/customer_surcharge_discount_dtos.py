
from typing import List, Optional


class CustomerSurchargeDiscountDetailDto:
        customer:str
        surcharge:str
        discount:str
        is_active:bool
 
class CustomerSurchargeDiscountSetDto:
        customer:Optional[str]
        surcharge:str
        discount:str
        is_active:bool

