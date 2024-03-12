
from ast import List
# from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class FsaRateMappingDetailDto:
        destination_fsa:str
        origin_zone:int
        rate_code:str
        is_active:bool
 
class FsaRateMappingSetDto:
        destination_fsa:str
        origin_zone:int
        rate_code:str
        is_active:bool

