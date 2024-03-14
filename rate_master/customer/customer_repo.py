from rate_master.common_methods.already_exist_exce import AlreadyExistException
from boto3.dynamodb.conditions import Key
from rate_master.infrastructure.dbhelper import DBHelper
from rate_master.customer.customer_ent import CustomerEntity
from rate_master.customer.i_customer_repo import ICustomerRepository

_key = "CU#"
_entity = "customer"
class CustomerRepository(ICustomerRepository):
   
    def save(self, enty: CustomerEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.id
            dic['SK'] = "#"+ _key + str()
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.description.upper()
            
            #if self.exits(enty):
             # raise AlreadyExistException(f"Customer '{enty.description}' already exist!")
            #comment the code
           
            DBHelper.put_item(dic)

        
    def get_by_id(self, id: str) -> CustomerEntity:
            key =  Key={
                    "PK": _key +id,
                    "SK": "#"+ _key
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = CustomerEntity(item)
            return enty
    
    def get_all(self) -> list[CustomerEntity]:
         k=Key('SK').eq("#"+ _key)
         return DBHelper.query('SK-PK-index',k,CustomerEntity)


    def create(self, enty: CustomerEntity) -> None:
        dic = enty.__dict__
        dic['PK'] = _key + enty.id
        dic['SK'] = "#"+ _key + str()
        dic['entity'] = _entity
        dic['unique_description'] = "#"+_key + enty.description.upper()

        if self.id_exits(enty):
                raise AlreadyExistException(f"Customer '{enty.id}' already exist!")
        
        #if self.exits(enty):
                #raise AlreadyExistException(f"Customer '{enty.description}' already exist!")
        
        DBHelper.put_item(dic)


    def exits(self, enty: CustomerEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,CustomerEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
    
    def id_exits(self, enty: CustomerEntity) -> bool:

         k= Key('PK').eq(_key +  enty.id) & Key('SK').eq("#"+ _key)
         items = DBHelper.query(None,k,CustomerEntity)
 
         if items and len(items) > 0:
            return True
         
         return False
       

        
  