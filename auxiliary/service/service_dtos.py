
from ast import List
from pydantic import BaseModel
from typing import List, Optional
from common_methods.shared import ConstraintDto

class ServiceDetailDto:
        id:str
        description:str
        constraints: List[ConstraintDto]
        is_restricted: bool
        is_system:bool
        is_active:bool
 
class ServiceSetDto(BaseModel):
        id:Optional[str]
        description:str
        constraints: Optional[List[ConstraintDto]]
        is_restricted: bool
        is_active:bool

