from domain.exceptions.already_exist_exce import AlreadyExistException
from i_lane_repo import ILaneRepository
from lane_ent import LaneEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper

_key = "LA#"
_entity = "lane"
_sk = "CA#"
class LaneRepository(ILaneRepository):
   
    def save(self, enty: LaneEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.id 
            dic['SK'] = _sk + enty.carrier
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.description.upper()
            
            if self.exits(enty):
              raise AlreadyExistException(f"Lane '{enty.description}' already exist!")
           
            DBHelper.put_item(dic)

    def create(self, enty: LaneEntity) -> None:
        dic = enty.__dict__
        dic['PK'] = _key + enty.id
        dic['SK'] = _sk + enty.carrier
        dic['entity'] = _entity
        dic['unique_description'] = "#"+_key + enty.description.upper()

        if self.id_exits(enty):
                raise AlreadyExistException(f"Lane with origin and destination combination already exist!")
        
        if self.exits(enty):
                raise AlreadyExistException(f"Lane '{enty.description}' already exist!")
        
        DBHelper.put_item(dic)
        
    def get_by_id(self, id: str) -> LaneEntity:
        k= Key('PK').eq(_key + id)
        items = DBHelper.query(None,k,LaneEntity)

        if len(items) == 0:
                return None

        return items[0]
    
#     def get_all(self) -> list[LaneEntity]:
#          k=Key('SK').eq("#"+_key)
#          return DBHelper.query('SK-PK-index',k,LaneEntity)
    def get_all(self) -> LaneEntity:
        k= Key('entity').eq(_entity)
        items = DBHelper.query("entity-PK-index",k,LaneEntity)
        return items

    def get_by_carrierId(self, carrierId: str):
        k=Key('SK').eq(_sk + carrierId)
        return DBHelper.query('SK-PK-index',k,LaneEntity)
    
    def exits(self, enty: LaneEntity) -> bool:
         k= Key('unique_description').eq('#' + _key + enty.description.upper()) 
         items = DBHelper.query('unique_description-index',k,LaneEntity)
        
         if len(items) == 1 and items[0].id != enty.id:
            return True
 
         if len(items) > 1:
            return True
         
         return False
    
    def id_exits(self, enty: LaneEntity) -> bool:

        k= Key('PK').eq(_key +  enty.id)
        items = DBHelper.query(None,k,LaneEntity)

        if items and len(items) > 0:
                return True
        
        return False
       

        
  