import json

from zone_dtos import *
from common_methods.shared import *

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
       
        if isinstance(obj, ConstraintDto):
            return obj.__dict__
        if isinstance(obj, ZoneDetailDto):
            return obj.__dict__
        if isinstance(obj, ZoneStatusDetailDto):
            return obj.__dict__       
        if isinstance(obj, CostDto):
            return obj.__dict__
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
