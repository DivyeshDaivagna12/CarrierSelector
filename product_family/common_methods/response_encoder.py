import json

from product_family_dtos import *
from common_methods.shared import *
#template-import

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, ConstraintDto):
            return obj.__dict__
        if isinstance(obj, ProductFamilyDetailDto):
            return obj.__dict__
        if isinstance(obj, ProductFamilyDetailDto): 
            return obj.__dict__ 
        if isinstance(obj, CostDto):
            return obj.__dict__
        
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
