
from ast import List
from pydantic import BaseModel
from typing import List, Optional


class PackagingDetailDto:
        id:str
        description:str
        is_active:bool
 
class PackagingSetDto(BaseModel):
        id:Optional[str]
        description:str
        is_active:bool

