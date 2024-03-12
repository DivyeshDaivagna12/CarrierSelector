from common_methods.already_exist_exce import AlreadyExistException
from i_time_definite_repo import ITimeDefiniteRepository
from time_definite_ent import TimeDefiniteEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper

_key = "TD#"
_entity = "timedefinite"
class TimeDefiniteRepository(ITimeDefiniteRepository):
   
    def save(self, enty: TimeDefiniteEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.id
            dic['SK'] = "#"+ _key + str()
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.description.upper()
            
            if self.exits(enty):
              raise AlreadyExistException(f"Time Definite '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)
        
    def get_by_id(self, id: str) -> TimeDefiniteEntity:
            key =  Key={
                    "PK": _key +id,
                    "SK": "#"+_key
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = TimeDefiniteEntity(item)
            return enty
    
    def get_all(self) -> list[TimeDefiniteEntity]:
         k=Key('SK').eq("#"+_key)
         return DBHelper.query('SK-PK-index',k,TimeDefiniteEntity)
    
    def exits(self, enty: TimeDefiniteEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,TimeDefiniteEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
       

        
  
