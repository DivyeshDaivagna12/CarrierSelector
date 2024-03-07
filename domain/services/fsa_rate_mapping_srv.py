from uuid import uuid4
from  domain.entities.fsa_rate_mapping_ent import FsaRateMappingEntity
from domain.dtos.fsa_rate_mapping_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_fsa_rate_mapping_repo import IFsaRateMappingRepository

class FsaRateMappingService:
    def __init__(self, repo: IFsaRateMappingRepository):
        self.repo = repo

    def create(self, dto: FsaRateMappingSetDto)->None:
        enty = FsaRateMappingEntity()                  
        enty.set(dto)
        self.repo.create(enty)
 
    def set(self, dto: FsaRateMappingSetDto)->None:
        enty = FsaRateMappingEntity()                  
        enty.set(dto)
        self.repo.save(enty)

    def get(self, destination_fsa:str,origin_zone:str)->FsaRateMappingDetailDto:
       enty = self.repo.get_by_origin(destination_fsa,origin_zone)
       if enty is None:raise RescourceNotFoundException(f"FsaRateMapping {origin_zone} not found")
       return enty.to_dto()
    
    def get_all(self)->list[FsaRateMappingDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 