from domain.exceptions.already_exist_exce import AlreadyExistException
from domain.interfaces.i_product_family_repo import IProductFamilyRepository
from domain.entities.product_family_ent import ProductFamilyEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper

_key = "PF#"
_entity = "productfamily"
class ProductFamilyRepository(IProductFamilyRepository):
   
    def save(self, enty: ProductFamilyEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.id
            dic['SK'] = "#"+ _key + str()
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.description.upper()
            
            if self.exits(enty):
              raise AlreadyExistException(f"Product Family '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)
        
    def get_by_id(self, id: str) -> ProductFamilyEntity:
            key =  Key={
                    "PK": _key +id,
                    "SK": "#"+_key
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = ProductFamilyEntity(item)
            return enty
    
    def get_all(self) -> list[ProductFamilyEntity]:
         k=Key('SK').eq("#"+_key)
         return DBHelper.query('SK-PK-index',k,ProductFamilyEntity)
    
    def exits(self, enty: ProductFamilyEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,ProductFamilyEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
       

        
  