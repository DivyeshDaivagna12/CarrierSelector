from rate_master.common_methods.already_exist_exce import AlreadyExistException
from boto3.dynamodb.conditions import Key
from rate_master.infrastructure.dbhelper import DBHelper
from rate_master.service.i_service_repo import IServiceRepository
from rate_master.service.service_ent import ServiceEntity

_key = "SE#"
_entity = "service"
class ServiceRepository(IServiceRepository):
   
    def save(self, enty: ServiceEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.id
            dic['SK'] = "#"+ _key + str()
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.description.upper()
            
            if self.exits(enty):
              raise AlreadyExistException(f"Service '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)
        
    def get_by_id(self, id: str) -> ServiceEntity:
            key =  Key={
                    "PK": _key +id,
                    "SK": "#"+_key
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = ServiceEntity(item)
            return enty
    
    def get_all(self) -> list[ServiceEntity]:
         k=Key('SK').eq("#"+_key)
         return DBHelper.query('SK-PK-index',k,ServiceEntity)
    
    def exits(self, enty: ServiceEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,ServiceEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
       

        
  