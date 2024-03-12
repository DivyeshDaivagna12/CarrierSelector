
from ast import List
from pydantic import BaseModel
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

