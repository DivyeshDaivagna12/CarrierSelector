
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel
from typing import List, Optional
from domain.dtos.shared import ConstraintDto

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

