
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class SkidSpacingDetailDto:
        id:str
        skid_space:int
        longest_side_min:str
        longest_side_max:str
        second_longest_side_min:str
        second_longest_side_max:str
        is_active:bool
 
class SkidSpacingSetDto(BaseModel):
        id:Optional[str]
        skid_space:int
        longest_side_min:str
        longest_side_max:str
        second_longest_side_min:str
        second_longest_side_max:str
        is_active:bool

