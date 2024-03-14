from common_methods.already_exist_exce import AlreadyExistException
from bulk_insert_history.i_bulk_insert_history_repo import IBulkInsertHistoryRepository
from bulk_insert_history.bulk_insert_history_ent import BulkInsertHistoryEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper

_key = "BI"
_entity = "bulkinserthistory"

class BulkInsertHistoryRepository(IBulkInsertHistoryRepository):
   
    def save(self, enty: BulkInsertHistoryEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key 
            dic['SK'] = enty.date_time
            dic['entity'] = _entity
                      
            DBHelper.put_item(dic)
        
    
    def get_all(self) -> list[BulkInsertHistoryEntity]:
         k=Key('PK').eq(_key)
         return DBHelper.query(None,k,BulkInsertHistoryEntity)
    

       

        
  