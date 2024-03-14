from common_methods.already_exist_exce import AlreadyExistException
from customer_surcharge_discount.i_customer_surcharge_discount_repo import ICustomerSurchargeDiscountRepository
from customer_surcharge_discount.customer_surcharge_discount_ent import CustomerSurchargeDiscountEntity
from boto3.dynamodb.conditions import Key
from infrastructure.repositories.dbhelper import DBHelper

_key = "CD#CU#"
_sk = "CD#SR#"
_entity = "customersurchargediscount"
class CustomerSurchargeDiscountRepository(ICustomerSurchargeDiscountRepository):
   
    def save(self, enty: CustomerSurchargeDiscountEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = self.get_pk(enty)
            dic['SK'] = self.get_sk(enty)
            dic['entity'] = _entity
           
            DBHelper.put_item(dic)
    def create(self, enty: CustomerSurchargeDiscountEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = self.get_pk(enty)
            dic['SK'] = self.get_sk(enty)
            dic['entity'] = _entity
            
            if self.id_exits(enty):
              raise AlreadyExistException(f"Customer Service Discount already exist!")
           
            DBHelper.put_item(dic)
        
    def get(self, customer: str, surcharge: str) -> CustomerSurchargeDiscountEntity:
            key =  Key={
                    "PK": self.get_pk_c(customer),
                    "SK": self.get_sk_s(surcharge)
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = CustomerSurchargeDiscountEntity(item)
            return enty
    
    def get_all(self) -> list[CustomerSurchargeDiscountEntity]:
         k=Key('entity').eq(_entity)
         return DBHelper.query('entity-PK-index',k,CustomerSurchargeDiscountEntity)
    
    def exits(self, enty: CustomerSurchargeDiscountEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.surcharge.upper()) 
         items = DBHelper.query('unique_description-index',k,CustomerSurchargeDiscountEntity)
        
         if len(items) == 1 and items[0].id != enty.customer:
            return True
 
         if len(items) > 1:
            return True
         
         return False
       
    def id_exits(self, enty: CustomerSurchargeDiscountEntity) -> bool:

         k= Key('PK').eq(self.get_pk(enty)) & Key('SK').eq(self.get_sk(enty))
         items = DBHelper.query(None,k,CustomerSurchargeDiscountEntity)
 
         if items and len(items) > 0:
            return True
         
         return False
        
    def get_pk(self, enty: CustomerSurchargeDiscountEntity):
         return self.get_pk_c(enty.customer)  
    
    def get_pk_c(self, customer:str):
         return _key +customer
    
    def get_sk(self, enty: CustomerSurchargeDiscountEntity):
         return self.get_sk_s(enty.surcharge)  
    
    def get_sk_s(self, surcharge:str):
         return _sk + surcharge
     