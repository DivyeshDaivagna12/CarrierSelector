from uuid import uuid4
from  domain.entities.time_definite_ent import TimeDefiniteEntity
from domain.dtos.time_definite_dtos import *
from domain.exceptions.bad_request_exce import BadRequestException
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_time_definite_repo import ITimeDefiniteRepository
from domain.constants import same_day_time_definite_id, next_day_time_definite_id, same_day_time_definite_desc, next_day_time_definite_desc 

class TimeDefinteService:

    def __init__(self, repo: ITimeDefiniteRepository):
        self.repo = repo
 
    def set(self, dto: TimeDefiniteSetDto)->None:
        enty = TimeDefiniteEntity()
        print(dto)
        if dto.id is None:
            # dto.id = uuid4().hex
            dto.id = dto.description.upper()
            print( "---------------",dto.id)
        elif dto.id == same_day_time_definite_id or dto.id == next_day_time_definite_id:
           raise BadRequestException(f"System defined time definite {dto.id} can not be modified")
            
        enty.set(dto)
        self.repo.save(enty)

    def get(self, id: str)->TimeDefiniteDetailDto:
       enty = self.repo.get_by_id(id)
       if enty is None:raise RescourceNotFoundException(f"time definite {id} not found")
       return enty.to_dto()
    
    def get_all(self)->list[TimeDefiniteDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 
    def add_system_timedefinite(self)->None:
        enty = TimeDefiniteEntity()
        enty.id = same_day_time_definite_id
        enty.description = same_day_time_definite_desc
        enty.is_active = True
        self.repo.save(enty)
        
        enty = TimeDefiniteEntity()
        enty.id = next_day_time_definite_id
        enty.description = next_day_time_definite_desc
        enty.is_active = True
        self.repo.save(enty)
