
from rate_master.fsa_zone_mapping.fsa_zone_mapping_dtos import FsaZoneMappingDetailDto, FsaZoneMappingSetDto


class FsaZoneMappingEntity():
    origin_fsa:str
    origin_zone:int
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->FsaZoneMappingDetailDto:
        dto = FsaZoneMappingDetailDto()
        dto.origin_fsa = self.origin_fsa
        dto.origin_zone = self.origin_zone
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:FsaZoneMappingSetDto):
        self.origin_fsa = dto.origin_fsa
        self.origin_zone = dto.origin_zone
        self.is_active = dto.is_active
        return self
