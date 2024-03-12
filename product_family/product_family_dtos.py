
from ast import List
from pydantic import BaseModel
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

