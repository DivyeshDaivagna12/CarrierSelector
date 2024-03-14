from uuid import uuid4
from carrier.carrier_ent import CarrierEntity
from carrier.carrier_dtos import *
from common_methods.not_found_exce import RescourceNotFoundException
from carrier.i_carrier_repo import ICarrierRepository

class CarrierService:
    def __init__(self, repo: ICarrierRepository):
        self.repo = repo
 
    def create(self, dto: CarrierSetDto)->None:
        enty = CarrierEntity()
        enty.set(dto)
        self.repo.create(enty)
        
    def update(self, dto: CarrierSetDto)->None:
        enty = CarrierEntity()            
        enty.set(dto)
        self.repo.save(enty)

    def get(self, id: str)->CarrierDetailDto:
       enty = self.repo.get_by_id(id)
       if enty is None:raise RescourceNotFoundException(f"Carrier {id} not found")
       return enty.to_dto()
    
    def get_all(self)->list[CarrierDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 