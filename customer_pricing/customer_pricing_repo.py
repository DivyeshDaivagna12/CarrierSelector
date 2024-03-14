from customer_pricing.i_customer_pricing_repo import ICustomerPricingRepository
from customer_pricing.customer_pricing_ent import CustomerPricingEntity
from boto3.dynamodb.conditions import Key
from infrastructure.repositories.dbhelper import DBHelper

_key = "RM#PR"
_entity = "customerpricing"
_sk = "RC#"
class CustomerPricingRepository(ICustomerPricingRepository):
   
    def save(self, enty: CustomerPricingEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.product
            dic['SK'] = _sk+ enty.rate_code
            dic['entity'] = _entity
                        
            DBHelper.put_item(dic)
        
    def get_by_productId(self, rateCode:str,productId:str) -> CustomerPricingEntity:
            key =  Key={
                    "PK": _key +productId,
                    "SK": _sk+rateCode
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = CustomerPricingEntity(item)
            return enty
    
    def get_all(self, productId:str ) -> list[CustomerPricingEntity]:
         k=Key('PK').eq(_key+productId)
         return DBHelper.query(None,k,CustomerPricingEntity)
    
    def exits(self, enty: CustomerPricingEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,CustomerPricingEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
       

        
  