from common_methods.already_exist_exce import AlreadyExistException
from carrier_product.offering.i_offering_repo import IOfferingRepository
from carrier_product.offering.offering_ent import OfferingEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper

 
_key = "OF#"
_entity = "offering"
_sk = "V#"
class OfferingRepository(IOfferingRepository):
   
    def save(self, enty: OfferingEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.id
            dic['SK'] = _sk + str(enty.version)
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.carrier + enty.description.upper()
            dic['is_active'] = enty.is_active
            if self.exits(enty):
              raise AlreadyExistException(f"Offering '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)
        
    def get_by_id(self, id: str) -> OfferingEntity:
        k= Key('PK').eq(_key + id)
        items = DBHelper.query(None,k,OfferingEntity)
        return items
    
    def get_all(self) ->list[OfferingEntity]:
        k= Key('entity').eq(_entity)
        items = DBHelper.query("entity-PK-index",k,OfferingEntity)
        return items
    
    def get_by_version(self, id: str, version: int) -> OfferingEntity:
        k= Key('PK').eq(_key + id) & Key('SK').eq(_sk + str(version))
        items = DBHelper.query(None,k,OfferingEntity)
        if len(items) == 0:
            return None
        return items[0]
    
    def exits(self, enty: OfferingEntity) -> bool:
         k= Key('unique_description').eq("#"+_key + enty.carrier + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,OfferingEntity) 
         
         if len(items) == 0:
             return False
         else:
             for i in range(len(items)):
                 if items[i].id != enty.id:
                     return True
         
         return False
       

    def insert_batch(self, entyArray: list[OfferingEntity]) -> None:
        table = DBHelper.get_table()
        with table.batch_writer() as batch_writer:
            for enty in entyArray:
                dic = enty.__dict__
                dic['PK'] = _key + enty.id
                dic['SK'] = _sk + str(enty.version)
                dic['entity'] = _entity
                dic['unique_description'] = "#"+_key + enty.carrier + enty.description.upper()
                dic['is_active'] = enty.is_active if enty.is_active else True
                batch_writer.put_item(Item=dic)
                
  
