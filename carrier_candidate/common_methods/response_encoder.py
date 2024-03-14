import json
import decimal
from zone.zone_dtos import *
from service.service_dtos import * 
from customer.customer_dtos import * 
from carrier.carrier_dtos import * 
from product.product_dtos import * 
from lane.lane_dtos import * 
from carrier_product.carrier_product_dtos import * 
from offering.offering_dtos import * 
from carrier_candidate_dtos import *
#template-import

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ProductDetailDto):
            return obj.__dict__
        if isinstance(obj, ConstraintDto):
            return obj.__dict__
        if isinstance(obj, ZoneDetailDto):
            return obj.__dict__
        if isinstance(obj, ZoneStatusDetailDto):
            return obj.__dict__       
        if isinstance(obj, ServiceDetailDto): 
                return obj.__dict__ 
        if isinstance(obj, CustomerDetailDto): 
                return obj.__dict__ 
        if isinstance(obj, CarrierDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, ProductDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, LaneDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, CarrierProductDetailDto):        
             return obj.__dict__ 
        if isinstance(obj, OfferingDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, CostDto):
            return obj.__dict__
        if isinstance(obj, decimal.Decimal):
             return str(obj)
        if isinstance(obj, CarrierCandidateDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, ServiceDto): 
             return obj.__dict__ 
        
 		#template-con
 	
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
