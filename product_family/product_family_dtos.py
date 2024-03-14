
from ast import List
from typing import List, Optional


class ProductFamilyDetailDto:
        id:str
        description:str
        is_active:bool
        #modify_at:int
 
class ProductFamilySetDto:
        id:Optional[str]
        description:str
        is_active:bool

