from bulk_insert_history.bulk_insert_history_ent import BulkInsertHistoryEntity
from bulk_insert_history.bulk_insert_history_dtos import *
from bulk_insert_history.i_bulk_insert_history_repo import IBulkInsertHistoryRepository

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
 