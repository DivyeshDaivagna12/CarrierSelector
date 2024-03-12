from uuid import uuid4
from service_ent import ServiceEntity
from service_dtos import *
from common_methods.bad_request_exce import BadRequestException
from common_methods.not_found_exce import RescourceNotFoundException
from i_service_repo import IServiceRepository
from common_methods.constants import excessive_skid_id
from common_methods.constants import excessive_skid_desc

class ServiceService:

    def __init__(self, repo: IServiceRepository):
        self.repo = repo
 
    def set(self, dto: ServiceSetDto)->None:
        enty = ServiceEntity()
        if dto.id is None:
            dto.id = uuid4().hex
        elif dto.id == excessive_skid_id:
           raise BadRequestException(f"System defined Service {dto.id} can not be modified")
              
        enty.set(dto)
        self.repo.save(enty)

    def get(self, id: str)->ServiceDetailDto:
       enty = self.repo.get_by_id(id)
       if enty is None:raise RescourceNotFoundException(f"Service {id} not found")
       return enty.to_dto()
    
    def get_all(self)->list[ServiceDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
    
    def add_system_services(self)->None:
        enty = ServiceEntity()
        enty.is_system=True
        enty.id = excessive_skid_id
        enty.description = excessive_skid_desc
        enty.constraints = []
        enty.is_active = True
        enty.is_restricted = False
        self.repo.save(enty)
 