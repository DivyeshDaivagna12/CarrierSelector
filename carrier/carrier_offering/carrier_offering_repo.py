from carrier_offering.i_carrier_offering_repo import ICarrierOfferingRepository
from carrier_offering.carrier_offering_ent import CarrierOfferingEntity
from boto3.dynamodb.conditions import Key

from infrastructure.repositories.dbhelper import DBHelper


_key = "CA#"
_entity = "carrieroffering"
_sk = "OF#"
class CarrierOfferingRepository(ICarrierOfferingRepository):
   
    def save(self, enty: CarrierOfferingEntity) -> None:
            dic = enty.__dict__
            dic['PK'] = _key + enty.carrier
            dic['SK'] = _sk + enty.offering
            dic['entity'] = _entity
            dic['unique_description'] = "#"+_key + enty.carrier +"-"+enty.offering
            dic['is_active'] = enty.is_active   
            DBHelper.put_item(dic)
        
    def get_by_carrierId(self, carrierId: str) -> CarrierOfferingEntity:
        k= Key('PK').eq(_key + carrierId) & Key('SK').begins_with(_sk)
        items = DBHelper.query(None,k,CarrierOfferingEntity)
        return items
    

        
  
