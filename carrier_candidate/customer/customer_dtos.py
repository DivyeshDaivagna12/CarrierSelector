
from ast import List
from typing import List, Optional


class CustomerDetailDto:
        id:str
        description:str
        is_active:bool
        preferred_carrier: Optional[str]
        excluded_carriers: Optional[List[str]]
        products: Optional[List[str]]
        services: Optional[List[str]]
 
class CustomerSetDto:
        id:str
        description:str
        is_active:bool
        preferred_carrier: Optional[str]
        excluded_carriers: Optional[List[str]]
        products: Optional[List[str]]
        services: Optional[List[str]]
