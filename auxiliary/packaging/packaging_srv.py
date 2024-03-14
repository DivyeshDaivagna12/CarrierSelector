from uuid import uuid4
from  packaging.packaging_ent import PackagingEntity
from packaging.packaging_dtos import *
from common_methods.bad_request_exce import BadRequestException
from common_methods.not_found_exce import RescourceNotFoundException
from  packaging.i_packaging_repo import IPackagingRepository
from common_methods.constants import loss_packaging_id,skid_packaging_id

class PackagingService:
    def __init__(self, repo: IPackagingRepository):
        self.repo = repo
 
    def set(self, dto: PackagingSetDto)->None:
        enty = PackagingEntity()
        if dto.id is None:
            dto.id = uuid4().hex
        elif dto.id == loss_packaging_id or  dto.id == skid_packaging_id:
           raise BadRequestException(f"System defined packaging {dto.id} can not be modified")
            
        enty.set(dto)
        self.repo.save(enty)

    def get(self, id: str)->PackagingDetailDto:
       enty = self.repo.get_by_id(id)
       if enty is None:raise RescourceNotFoundException(f"Packaging {id} not found")
       return enty.to_dto()
    
    def get_all(self)->list[PackagingDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 
    def add_system_packaging(self)->None:
        enty = PackagingEntity()
        enty.id = loss_packaging_id
        enty.description = loss_packaging_id
        enty.is_active = True
        self.repo.save(enty)
        
        enty = PackagingEntity()
        enty.id = skid_packaging_id
        enty.description = skid_packaging_id
        enty.is_active = True
        self.repo.save(enty)