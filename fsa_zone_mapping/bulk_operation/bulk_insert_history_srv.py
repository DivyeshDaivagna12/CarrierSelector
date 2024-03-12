from uuid import uuid4
from fsa_zone_mapping.bulk_operation.bulk_insert_history_ent import BulkInsertHistoryEntity
from fsa_zone_mapping.bulk_operation.bulk_insert_history_dtos import *
from fsa_zone_mapping.bulk_operation.i_bulk_insert_history_repo import IBulkInsertHistoryRepository

class BulkInsertHistoryService:
    def __init__(self, repo: IBulkInsertHistoryRepository):
        self.repo = repo 
    
    def set(self, dto: BulkInsertHistoryDetailDto)->None:
        enty = BulkInsertHistoryEntity()                      
        enty.set(dto)
        self.repo.save(enty)
     
    def get_all(self)->list[BulkInsertHistoryDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 