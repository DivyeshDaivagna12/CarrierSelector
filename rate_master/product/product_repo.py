from rate_master.common_methods.already_exist_exce import AlreadyExistException
from boto3.dynamodb.conditions import Key
from infrastructure.repositories.dbhelper import DBHelper
from rate_master.product.i_product_repo import IProductRepository
from rate_master.product.product_ent import ProductEntity

_key = "PR#"
_entity = "product"
class ProductRepository(IProductRepository):
   
    def save(self, enty: ProductEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.id
            dic['SK'] = "#"+ _key + str()
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.description.upper()
            
            if self.exits(enty):
              raise AlreadyExistException(f"Product '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)
        
    def get_by_id(self, id: str) -> ProductEntity:
            key =  Key={
                    "PK": _key +id,
                    "SK": "#"+_key
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = ProductEntity(item)
            return enty
    
    def get_all(self) -> list[ProductEntity]:
         k=Key('SK').eq("#"+_key)
         return DBHelper.query('SK-PK-index',k,ProductEntity)
    
    def create(self, enty: ProductEntity) -> None:
        dic = enty.__dict__
        dic['PK'] = _key + enty.id
        dic['SK'] = "#"+ _key + str()
        dic['entity'] = _entity
        dic['unique_description'] = "#"+_key + enty.description.upper()

        if self.id_exits(enty):
                raise AlreadyExistException(f"Product '{enty.id}' already exist!")
        
        if self.exits(enty):
                raise AlreadyExistException(f"Product '{enty.description}' already exist!")
        
        DBHelper.put_item(dic)


    def exits(self, enty: ProductEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,ProductEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
    
    def id_exits(self, enty: ProductEntity) -> bool:

         k= Key('PK').eq(_key +  enty.id) & Key('SK').eq("#"+ _key)
         items = DBHelper.query(None,k,ProductEntity)
 
         if items and len(items) > 0:
            return True
         
         return False
       

        
  
       

        
  