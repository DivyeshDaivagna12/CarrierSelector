
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class ProductFamilyDetailDto:
        id:str
        description:str
        is_active:bool
        #modify_at:int
 
class ProductFamilySetDto(BaseModel):
        id:Optional[str]
        description:str
        is_active:bool

