from common_methods.already_exist_exce import AlreadyExistException
from i_carrier_repo import ICarrierRepository
from carrier_ent import CarrierEntity
from boto3.dynamodb.conditions import Key
from infrastructure.repositories.dbhelper import DBHelper

_key = "CA#"
_entity = "carrier"
class CarrierRepository(ICarrierRepository):
   
    def save(self, enty: CarrierEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.id
            dic['SK'] = "#"+ _key + str()
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.description.upper()
            
           # if self.exits(enty):
            #  raise AlreadyExistException(f"Carrier '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)

    def create(self, enty: CarrierEntity) -> None:
        dic = enty.__dict__
        dic['PK'] = _key + enty.id
        dic['SK'] = "#"+ _key + str()
        dic['entity'] = _entity
        dic['unique_description'] = "#"+_key + enty.description.upper()

        if self.id_exits(enty):
                raise AlreadyExistException(f"Carrier with Route Number '{enty.id}' already exist!")
        
        if self.exits(enty):
                raise AlreadyExistException(f"Carrier '{enty.description}' already exist!")
        
        DBHelper.put_item(dic)
        
    def get_by_id(self, id: str) -> CarrierEntity:
            key =  Key={
                    "PK": _key +id,
                    "SK": "#"+_key
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = CarrierEntity(item)
            return enty
    
    def get_all(self) -> list[CarrierEntity]:
         k=Key('SK').eq("#"+_key)
         return DBHelper.query('SK-PK-index',k,CarrierEntity)
    
    def exits(self, enty: CarrierEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,CarrierEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
    
    def id_exits(self, enty: CarrierEntity) -> bool:

         k= Key('PK').eq(_key +  enty.id) & Key('SK').eq("#"+_key)
         items = DBHelper.query(None,k,CarrierEntity)
 
         if items and len(items) > 0:
            return True
         
         return False
       

        
  