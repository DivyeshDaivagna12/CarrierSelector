from pydantic import BaseModel

class FsaRateMappingDetailDto:
        destination_fsa:str
        origin_zone:int
        rate_code:str
        is_active:bool
 
class FsaRateMappingSetDto(BaseModel):
        destination_fsa:str
        origin_zone:int
        rate_code:str
        is_active:bool

