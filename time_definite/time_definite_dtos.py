
from pydantic import BaseModel
from typing import Optional


class TimeDefiniteDetailDto:
        id:str
        description:str
        is_active:bool
 
class TimeDefiniteSetDto(BaseModel):
        id:Optional[str]
        description:str
        is_active:bool

