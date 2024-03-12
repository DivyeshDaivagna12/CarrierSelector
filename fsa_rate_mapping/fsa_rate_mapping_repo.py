from domain.exceptions.already_exist_exce import AlreadyExistException
from i_fsa_rate_mapping_repo import IFsaRateMappingRepository
from fsa_rate_mapping_ent import FsaRateMappingEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper

_key = "#OZ"
_entity = "fsaratemapping"
_sk ="#FSA"
class FsaRateMappingRepository(IFsaRateMappingRepository):
    
    def create(self, enty: FsaRateMappingEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + str(enty.origin_zone)
            dic['SK'] = _sk+enty.destination_fsa
            dic['entity'] = _entity 

            if self.origin_zone_exists(enty):
                 raise AlreadyExistException(f"Destination FSA already mapped to Zone!")
                                
            DBHelper.put_item(dic)

   
    def save(self, enty: FsaRateMappingEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + str(enty.origin_zone)
            dic['SK'] = _sk+enty.destination_fsa
            dic['entity'] = _entity                     
            DBHelper.put_item(dic)
        
    def get_by_origin(self, destination_fsa:str,origin_zone:str) -> FsaRateMappingEntity:
            key =  Key={
                    "PK": _key + str(origin_zone),
                    "SK": _sk + destination_fsa
                }
            item = DBHelper.get_item(key)
            if item is None:
                   return None
            enty = FsaRateMappingEntity(item)
            return enty
    
    def get_all(self) -> list[FsaRateMappingEntity]:
         k=Key('entity').eq(_entity)
         return DBHelper.query('entity-PK-index',k,FsaRateMappingEntity)
    
    def origin_zone_exists(self, entity:FsaRateMappingEntity) -> bool:
        k = Key('PK').eq(_key + str(entity.origin_zone)) & Key('SK').eq( _sk + entity.destination_fsa)
        items = DBHelper.query(None,k,FsaRateMappingEntity)

        if items and len(items) > 0:
            return True
                
        return False
       

        
  