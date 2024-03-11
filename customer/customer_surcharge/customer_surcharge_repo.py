from domain.exceptions.already_exist_exce import AlreadyExistException
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_customer_surcharge_repo import ICustomerSurchargeRepository
from domain.entities.customer_surcharge_ent import CustomerSurchargeEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper


_key = "RM#SR"
_entity = "customersurcharge"
_sk = "SR#"
class CustomerSurchargeRepository(ICustomerSurchargeRepository):
    
    def create(self, enty: CustomerSurchargeEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.service
            dic['SK'] = _sk
            dic['entity'] = _entity
                        
            if self.service_exists(enty):
                 raise AlreadyExistException(f"Customer Service Pricing already exist!")
                   
            DBHelper.put_item(dic)    
   
    def save(self, enty: CustomerSurchargeEntity) -> None:
           
            dic = enty.__dict__
            dic['PK'] = _key + enty.service
            dic['SK'] = _sk
            dic['entity'] = _entity                 
            DBHelper.put_item(dic)
        
    def get_by_service(self, service: str) -> CustomerSurchargeEntity:
            key =  Key={
                    "PK": _key +service,
                    "SK": _sk
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = CustomerSurchargeEntity(item)
            return enty
    
    def get_all(self) -> list[CustomerSurchargeEntity]:
         k=Key('SK').eq(_sk)
         return DBHelper.query('SK-PK-index',k,CustomerSurchargeEntity)    
   
    def service_exists(self, entity:CustomerSurchargeEntity) -> bool:
        k = Key('PK').eq(_key + entity.service) & Key('SK').eq( _sk)
        items = DBHelper.query(None,k,CustomerSurchargeEntity)

        if items and len(items) > 0:
             return True
        
        return False
       

        
  