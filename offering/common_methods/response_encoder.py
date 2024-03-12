import json

from product.product_dtos import * 
from offering_dtos import * 
import decimal

#template-import

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ProductDetailDto):
            return obj.__dict__
        if isinstance(obj, ConstraintDto):
            return obj.__dict__
        if isinstance(obj, ProductDetailDto): 
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
