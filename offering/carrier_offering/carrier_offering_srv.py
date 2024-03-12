from uuid import uuid4
from carrier_offering_ent import CarrierOfferingEntity
from carrier_offering_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from i_carrier_offering_repo import ICarrierOfferingRepository

class CarrierOfferingService:
    def __init__(self, repo: ICarrierOfferingRepository):
        self.repo = repo
 
    # def set(self, dto: CarrierOfferingSetDto)->None:
    #     enty = CarrierOfferingEntity()
    #     if dto.id is None:
    #         dto.id = uuid4().hex
            
    #     enty.set(dto)
    #     self.repo.save(enty)

    def get_by_carrierId(self, carrierId: str)->CarrierOfferingDetailDto:
    #    enty = self.repo.get_by_id(id)
    #    if enty is None:raise RescourceNotFoundException(f"CarrierOffering {id} not found")
    #    return enty.to_dto()
       list_dto = list()
       entities = self.repo.get_by_carrierId(carrierId)
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
    
    # def get_all(self)->list[CarrierOfferingDetailDto]:
    #    list_dto = list()
    #    entities = self.repo.get_all()
    #    for enty in entities:
    #       try:
    #         list_dto .append(enty.to_dto())
    #       except:
    #        pass
    #    return list_dto
 