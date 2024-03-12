
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional
from domain.dtos.shared import ConstraintDto

class ProductDetailDto:
        id:str
        description:str
        family:str
        packaging:str
        services : List[str]
        constraints: List[ConstraintDto]
        time_definite: str
        is_restricted: bool
        is_active:bool
 
class ProductSetDto(BaseModel):
        id:str
        description:str
        family:str
        packaging:str
        services:Optional[List[str]]
        time_definite: str
        constraints:Optional[List[ConstraintDto]]
        is_restricted: bool
        is_active:bool

