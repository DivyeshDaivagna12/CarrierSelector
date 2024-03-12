import json

from lane_dtos import * 
from offering.offering_dtos import * 
import decimal

#template-import

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, LaneDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, OfferingDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, CostDto):
            return obj.__dict__
        if isinstance(obj, decimal.Decimal):
             return str(obj)
        
 		#template-con
 	
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
