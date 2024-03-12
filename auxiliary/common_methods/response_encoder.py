import json

from customer_surcharge.customer_surcharge_dtos import *
from packaging.packaging_dtos import *
from service.service_dtos import *
from time_definite.time_definite_dtos import *
from common_methods.shared import *

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ConstraintDto):
            return obj.__dict__
        if isinstance(obj, PackagingDetailDto): 
            return obj.__dict__ 
        if isinstance(obj, ServiceDetailDto): 
                return obj.__dict__ 
        if isinstance(obj, CostDto):
            return obj.__dict__
        if isinstance(obj, TimeDefiniteDetailDto):
             return obj.__dict__
        if isinstance(obj, CustomerSurchargeDetailDto):
             return obj.__dict__
 		#template-con
 		#template-con
 	
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
