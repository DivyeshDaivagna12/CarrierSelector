from common_methods.already_exist_exce import AlreadyExistException
from i_packaging_repo import IPackagingRepository
from packaging_ent import PackagingEntity
from boto3.dynamodb.conditions import Key
from infrastructure.repositories.dbhelper import DBHelper

_key = "PA#"
_entity = "packaging"
class PackagingRepository(IPackagingRepository):
   
    def save(self, enty: PackagingEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.id
            dic['SK'] = "#"+ _key + str()
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.description.upper()
            
            if self.exits(enty):
              raise AlreadyExistException(f"Packaging '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)
        
    def get_by_id(self, id: str) -> PackagingEntity:
            key =  Key={
                    "PK": _key +id,
                    "SK": "#"+_key
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = PackagingEntity(item)
            return enty
    
    def get_all(self) -> list[PackagingEntity]:
         k=Key('SK').eq("#"+_key)
         return DBHelper.query('SK-PK-index',k,PackagingEntity)
    
    def exits(self, enty: PackagingEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,PackagingEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
       

        
  