from skid_spacing.i_skid_spacing_repo import ISkidSpacingRepository
from skid_spacing.skid_spacing_ent import SkidSpacingEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper

_key = "SKP#"
_entity = "skidspacing"
class SkidSpacingRepository(ISkidSpacingRepository):
   
    def save(self, enty: SkidSpacingEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + str(enty.skid_space)
            dic['SK'] = enty.id 
            dic['entity'] = _entity
            DBHelper.put_item(dic)
        
    def get_by_id(self, skid_space: int) -> SkidSpacingEntity:
            key =  Key={
                    "PK": _key + str(skid_space),
                    "SK": "#"+_key
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = SkidSpacingEntity(item)
            return enty
    
    def get_all(self) -> list[SkidSpacingEntity]:
         k=Key('entity').eq(_entity)
         return DBHelper.query('entity-PK-index',k,SkidSpacingEntity)
    
  