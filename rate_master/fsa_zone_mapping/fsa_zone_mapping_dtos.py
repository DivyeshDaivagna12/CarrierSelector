
from pydantic import BaseModel


class FsaZoneMappingDetailDto:
        origin_fsa:str
        origin_zone:int
        is_active:bool
        
 
class FsaZoneMappingSetDto(BaseModel):
        origin_fsa:str
        origin_zone:int
        is_active:bool
