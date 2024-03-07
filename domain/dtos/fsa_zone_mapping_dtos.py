
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class FsaZoneMappingDetailDto:
        origin_fsa:str
        origin_zone:int
        is_active:bool
        
 
class FsaZoneMappingSetDto(BaseModel):
        origin_fsa:str
        origin_zone:int
        is_active:bool
