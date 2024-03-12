from fsa_rate_mapping_dtos import *

class FsaRateMappingEntity():
    destination_fsa:str
    origin_zone:int
    rate_code:str
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->FsaRateMappingDetailDto:
        dto = FsaRateMappingDetailDto()
        dto.destination_fsa = self.destination_fsa
        dto.origin_zone = int(self.origin_zone)
        dto.rate_code = self.rate_code
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:FsaRateMappingSetDto):
        self.destination_fsa = dto.destination_fsa
        self.origin_zone = dto.origin_zone
        self.rate_code = dto.rate_code
        self.is_active = dto.is_active
        return self
