from common_methods.already_exist_exce import AlreadyExistException
from shipment.i_shipment_history_repo import IShipmentHistoryRepository
from shipment.shipment_history_ent import ShipmentHistoryEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper

 
_key = "SH#"
_entity = "shipmenthistory"
_sk = "CU#"
class ShipmentHistoryRepository(IShipmentHistoryRepository):
   
    def save(self, enty: ShipmentHistoryEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + str(enty.shipment_date)
            dic['SK'] = _sk + enty.customer + "-" + enty.shipment_id
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + str(enty.shipment_date) + enty.customer + enty.shipment_id
            
           
            DBHelper.put_item(dic)
        
    def get_by_shipment_date_and_customer(self, shipment_date: int, customerId: str) -> ShipmentHistoryEntity:
        k= Key('PK').eq(_key + str(shipment_date)) & Key('SK').begins_with(_sk + customerId)
        items = DBHelper.query(None,k,ShipmentHistoryEntity)
        return items
    
    def get_by_customer(self, customerId: str) -> ShipmentHistoryEntity:
        k= Key('PK').begins_with(_key) & Key('SK').begins_with(_sk + customerId)
        items = DBHelper.query("SK-PK-index",k,ShipmentHistoryEntity)
        return items
    
    def get_by_shipment_date(self, shipment_date: str) -> ShipmentHistoryEntity:
        k= Key('PK').eq(_key+str(shipment_date))
        items = DBHelper.query(None,k,ShipmentHistoryEntity)
        return items
    
#     def get_all(self) -> list[ShipmentHistoryEntity]:
#          k=Key('SK').eq("#"+_key)
#          return DBHelper.query('SK-PK-index',k,ShipmentHistoryEntity)
    
#     def exits(self, enty: ShipmentHistoryEntity) -> bool:
#          k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
#          items = DBHelper.query('unique_description-index',k,ShipmentHistoryEntity)
        
#          if len(items) == 1 and items[0].id != enty.id:
#             return True
 
#          if len(items) > 1:
#             return True
         
#          return False
       

        
  