from uuid import uuid4
from  domain.entities.carrier_product_ent import CarrierProductEntity
from domain.dtos.carrier_product_dtos import *
from domain.exceptions.bad_request_exce import BadRequestException
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_carrier_product_repo import ICarrierProductRepository
from infrastructure.repositories.offering_repo import OfferingRepository, OfferingEntity
from domain.constants import excessive_skid_id,excessive_skid_desc

class CarrierProductService:
    def __init__(self, repo: ICarrierProductRepository):
        self.repo = repo
        self.offeringRepo = OfferingRepository()

    def create(self, dto: CarrierProductSetDto)->None:
        enty = CarrierProductEntity()
        enty.set(dto)
        self.repo.create(enty)
 
    def set(self, dto: CarrierProductSetDto)->None:
        if dto.product == excessive_skid_id and dto.is_active == False:
            raise BadRequestException(f"{excessive_skid_desc} can not be deactivated")
        elif dto.is_active == False:
           self.remove_surcharge_from_all_offering(dto)
        enty = CarrierProductEntity()
        enty.set(dto)
        self.repo.save(enty)


    def add_system_products(self, carrier:str)->None:
        enty = CarrierProductEntity()
        enty.description = carrier + excessive_skid_id
        enty.carrier = carrier
        enty.product = excessive_skid_id
        enty.cost = "0"
        enty.is_active = True
        enty.carrier = carrier
        self.repo.save(enty)


    def get(self, carrier: str, product: str)->CarrierProductDetailDto:
       enty = self.repo.get_by_carrier_product(carrier, product)
       if enty is None:raise RescourceNotFoundException(f"Carrier{carrier} and Product{product} not found")
       return enty.to_dto()
    
    def get_all(self, carrier: str)->list[CarrierProductDetailDto]:
       list_dto = list()
       entities = self.repo.get_all(carrier)
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
    
    def remove_surcharge_from_all_offering(self, dto: CarrierProductSetDto)->None:
       offering_entities = self.offeringRepo.get_all()

       delta_offering_entities = []
       for offering_entity in offering_entities:
          if dto.carrier == offering_entity.carrier and dto.product in offering_entity.services:
            offering_entity.services.remove(dto.product)
            # self.offeringRepo.save(offering_entity)
            delta_offering_entities.append(offering_entity)
       if len(delta_offering_entities) > 0:
           self.offeringRepo.insert_batch(delta_offering_entities)