from domain.exceptions.already_exist_exce import AlreadyExistException
from domain.interfaces.i_carrier_product_repo import ICarrierProductRepository
from domain.entities.carrier_product_ent import CarrierProductEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper


_key = "CA#"
_entity = "carrierproduct"
_sk = "PR#"
class CarrierProductRepository(ICarrierProductRepository):
    
    def create(self, enty: CarrierProductEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.carrier
            dic['SK'] = _sk + enty.product
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_entity + enty.description.upper()
            
            if self.record_exists(enty):
                 raise AlreadyExistException(f"Surcharge already exist!")
           
            
            if self.exits(enty):
              raise AlreadyExistException(f"Surcharge '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)
   
    def save(self, enty: CarrierProductEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.carrier
            dic['SK'] = _sk + enty.product
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_entity + enty.description.upper()
            
            if self.exits(enty):
              raise AlreadyExistException(f"Surcharge '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)
        
    def get_by_carrier_product(self, carrier: str, product: str) -> CarrierProductEntity:
            key =  Key={
                    "PK": _key +carrier,
                    "SK": _sk+product
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = CarrierProductEntity(item)
            return enty
    
    def get_all(self, carrier: str) -> list[CarrierProductEntity]:
         k=Key('PK').eq(_key+carrier)
         return DBHelper.query(None,k,CarrierProductEntity)
    
    def exits(self, enty: CarrierProductEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,CarrierProductEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
    
    def record_exists(self, entity:CarrierProductEntity) -> bool:
        k = Key('PK').eq(_key + entity.carrier) & Key('SK').eq( _sk + entity.product)
        items = DBHelper.query(None,k,CarrierProductEntity)

        if items and len(items) > 0:
             return True
        
        return False
        
       

        
  