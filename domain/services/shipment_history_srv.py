from uuid import uuid4
from  domain.entities.shipment_history_ent import ShipmentHistoryEntity
from domain.dtos.shipment_history_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_shipment_history_repo import IShipmentHistoryRepository

class ShipmentHistoryService:
    def __init__(self, repo: IShipmentHistoryRepository):
        self.repo = repo
 
    def set(self, dto: ShipmentHistorySetDto)->None:
        enty = ShipmentHistoryEntity()
        enty.set(dto)
        self.repo.save(enty)
    
    def get_by_customer(self, customerId: str)->list[ShipmentHistoryDetailDto]:
       list_dto = list()
       entities = self.repo.get_by_customer(customerId)
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
    
    def get_by_shipment_date(self, shipment_date: int)->list[ShipmentHistoryDetailDto]:
       list_dto = list()
       entities = self.repo.get_by_shipment_date(shipment_date)
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
    
    def get_by_shipment_date_and_customer(self, shipment_date: int, customerId: str)->list[ShipmentHistoryDetailDto]:
       list_dto = list()
       entities = self.repo.get_by_shipment_date_and_customer(shipment_date, customerId)
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto