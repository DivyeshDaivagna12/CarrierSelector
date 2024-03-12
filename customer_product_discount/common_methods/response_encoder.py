import json
from customer_product_discount_dtos import * 
import decimal

#template-import

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
             return str(obj)
        if isinstance(obj, CustomerProductDiscountDetailDto):
             return obj.__dict__ 
        
 		#template-con
 	
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
