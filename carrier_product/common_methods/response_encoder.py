import json

from carrier_product_dtos import * 
from carrier_offering.carrier_offering_dtos import * 
from offering.offering_dtos import * 
import decimal

#template-import

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CarrierProductDetailDto):        
             return obj.__dict__ 
        if isinstance(obj, CarrierOfferingDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, decimal.Decimal):
             return str(obj)
        if isinstance(obj, OfferingDetailDto): 
             return obj.__dict__ 
        
 		#template-con
 	
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
