
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class LaneDetailDto:
        id:str
        description:str
        offerings: List[str]
        origin: str
        destination: str
        carrier: str
        is_active:bool
 
class LaneSetDto(BaseModel):
        id:Optional[str]
        description:str
        offerings: List[str]
        origin: str
        destination: str
        carrier: str
        is_active:bool
