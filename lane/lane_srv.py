from uuid import uuid4
from lane_ent import LaneEntity
from lane_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.exceptions.already_exist_exce import AlreadyExistException

from lane.i_lane_repo import ILaneRepository
from offering.offering_repo import OfferingRepository, OfferingEntity

class LaneService:
    def __init__(self, repo: ILaneRepository):
        self.repo = repo
        self.offeringRepo = OfferingRepository()

 
    def create(self, dto: LaneSetDto)->None:
        self.duplicate_product_validation(dto)

        enty = LaneEntity()
        dto.id = dto.origin + "-" + dto.destination + "-" + dto.carrier
        enty.set(dto)
        self.repo.create(enty)

    def update(self, dto: LaneSetDto)->None:
        self.duplicate_product_validation(dto)

        enty = LaneEntity()
        enty.set(dto)
        self.repo.save(enty)

    def duplicate_product_validation(self, dto: LaneSetDto):
       offering_entities = self.offeringRepo.get_all()

       res_dict = dict()
       for offering_entity in offering_entities:
            if not (offering_entity.id in res_dict):
               res_dict[offering_entity.id] = offering_entity

       product_dict = dict()
       for offering_id in dto.offerings:
          offering_entity: OfferingEntity = res_dict[offering_id]
          if offering_entity.product not in product_dict:
             product_dict[offering_entity.product] = offering_entity.description
          else:
             raise AlreadyExistException(f"Duplicate product found in offerings of lane. Offering '{offering_entity.description}' and '{product_dict[offering_entity.product]}' contains same product.")



    def get(self, id: str)->LaneDetailDto:
       enty = self.repo.get_by_id(id)
       if enty is None:raise RescourceNotFoundException(f"Lane {id} not found")
       return enty.to_dto()
    
    def get_by_carrierId(self,carrierId: str)->list[LaneDetailDto]:
       list_dto = list()
       entities = self.repo.get_by_carrierId(carrierId)
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 
