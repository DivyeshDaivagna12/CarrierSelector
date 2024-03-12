from common_methods.already_exist_exce import AlreadyExistException
from i_customer_product_discount_repo import ICustomerProductDiscountRepository
from customer_product_discount_ent import CustomerProductDiscountEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper


_key = "CD#CU#"
_sk = "CD#RC#"
_entity = "customerproductdiscount"
class CustomerProductDiscountRepository(ICustomerProductDiscountRepository):
   
    def save(self, enty: CustomerProductDiscountEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = self.get_pk(enty)
            dic['SK'] =  self.get_sk(enty)
            dic['entity'] = _entity
            dic['additional_piece_discount'] = enty.additional_piece_discount if enty.additional_piece_discount else 0
            DBHelper.put_item(dic)

    def create(self, enty: CustomerProductDiscountEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = self.get_pk(enty)
            dic['SK'] =  self.get_sk(enty)
            dic['entity'] = _entity
            
            if self.id_exits(enty):
              raise AlreadyExistException(f"Customer Product Discount already exist!")
           
            DBHelper.put_item(dic)
        
    def get(self, customer: str,product:str,rate_code:str) -> CustomerProductDiscountEntity:
           
            key =  Key={
                    "PK": self.get_pk_cp(customer, product),
                    "SK": self.get_sk_rc(rate_code)
                }
          #   print(key)
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = CustomerProductDiscountEntity(item)
            return enty
    
    def get_all(self) -> list[CustomerProductDiscountEntity]:
         k=Key('entity').eq(_entity)
         return DBHelper.query('entity-PK-index',k,CustomerProductDiscountEntity)
    
    def exits(self, enty: CustomerProductDiscountEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.customer.upper()) 
         items = DBHelper.query('unique_description-index',k,CustomerProductDiscountEntity)
        
         if len(items) == 1 and items[0].id != enty.product:
            return True
 
         if len(items) > 1:
            return True
         
         return False
    
    def id_exits(self, enty: CustomerProductDiscountEntity) -> bool:

         k= Key('PK').eq(self.get_pk(enty)) & Key('SK').eq(self.get_sk(enty))
         items = DBHelper.query(None,k,CustomerProductDiscountEntity)
 
         if items and len(items) > 0:
            return True
         
         return False
       
    def get_pk(self, enty: CustomerProductDiscountEntity):
         return self.get_pk_cp(enty.customer, enty.product)  
    
    def get_pk_cp(self, customer:str, product:str):
         return _key +customer + "#PR" +product  
    
    def get_sk(self, enty: CustomerProductDiscountEntity):
         return self.get_sk_rc(enty.rate_code)  
    
    def get_sk_rc(self, rate_code:str):
         sk =  _sk
         if rate_code != None:
            sk =  _sk + rate_code
         return sk
        
  
