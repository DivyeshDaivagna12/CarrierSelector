
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class TimeDefiniteDetailDto:
        id:str
        description:str
        is_active:bool
 
class TimeDefiniteSetDto(BaseModel):
        id:Optional[str]
        description:str
        is_active:bool
