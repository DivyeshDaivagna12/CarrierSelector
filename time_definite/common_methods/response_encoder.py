import json
import decimal

from time_definite.time_definite_dtos import TimeDefiniteDetailDto

#template-import

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        
        if isinstance(obj, decimal.Decimal):
             return str(obj)
        
        if isinstance(obj, TimeDefiniteDetailDto):
             return obj.__dict__
 		#template-con
 	
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
