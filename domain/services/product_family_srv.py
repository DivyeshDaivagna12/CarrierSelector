from uuid import uuid4
from  domain.entities.product_family_ent import ProductFamilyEntity
from domain.dtos.product_family_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_product_family_repo import IProductFamilyRepository

class ProductFamilyService:
    def __init__(self, repo: IProductFamilyRepository):
        self.repo = repo
 
    def set(self, dto: ProductFamilySetDto)->None:
        enty = ProductFamilyEntity()
        if dto.id is None:
            dto.id = uuid4().hex
            
        enty.set(dto)
        self.repo.save(enty)

    def get(self, id: str)->ProductFamilyDetailDto:
       enty = self.repo.get_by_id(id)
       if enty is None:raise RescourceNotFoundException(f"ProductFamily {id} not found")
       return enty.to_dto()
    
    def get_all(self)->list[ProductFamilyDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 