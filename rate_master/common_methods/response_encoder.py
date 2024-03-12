import json

from domain.dtos.product_dtos import *
from domain.dtos.service_dtos import * 
from domain.dtos.customer_dtos import *  
from domain.dtos.product_dtos import * 
import decimal
from domain.dtos.customer_pricing_dtos import * 
from domain.dtos.customer_surcharge_dtos import * 
from domain.dtos.fsa_zone_mapping_dtos import *  
from domain.dtos.fsa_rate_mapping_dtos import * 
from domain.dtos.customer_product_discount_dtos import * 
from domain.dtos.customer_surcharge_discount_dtos import * 
from domain.dtos.rate_master_dtos import * 
#template-import

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ProductDetailDto):
            return obj.__dict__
        if isinstance(obj, ConstraintDto):
            return obj.__dict__    
        if isinstance(obj, ServiceDetailDto): 
                return obj.__dict__ 
        if isinstance(obj, CustomerDetailDto): 
                return obj.__dict__      
        if isinstance(obj, CustomerPricingDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, CustomerSurchargeDetailDto): 
            return obj.__dict__ 
        if isinstance(obj, FsaZoneMappingDetailDto): 
            return obj.__dict__ 
        if isinstance(obj, FsaRateMappingDetailDto): 
            return obj.__dict__     
        if isinstance(obj, decimal.Decimal):
             return str(obj)
        if isinstance(obj, CustomerProductDiscountDetailDto):
             return obj.__dict__ 
        if isinstance(obj, CustomerSurchargeDiscountDetailDto): 
            return obj.__dict__       				 	
        if isinstance(obj, RateMasterDetailDto): 
                  return obj.__dict__ 
        if isinstance(obj, ProductRateDetailDto): 
                  return obj.__dict__
        if isinstance(obj, SurchargeBaseCost): 
                  return obj.__dict__
        if isinstance(obj, DiscountPercentage): 
                  return obj.__dict__
        if isinstance(obj, ProductDiscountPercentage): 
                  return obj.__dict__
        if isinstance(obj, SurchargesDiscountPercentage): 
                  return obj.__dict__
        if isinstance(obj, DiscountAmount): 
                  return obj.__dict__
        if isinstance(obj, ProductDiscountAmount): 
                  return obj.__dict__
        if isinstance(obj, SurchargesDiscountAmount): 
                  return obj.__dict__
        if isinstance(obj, FinalPrice): 
                  return obj.__dict__
        if isinstance(obj, ProductFinalPrice): 
                  return obj.__dict__
        if isinstance(obj, SurchargeFinalPrice): 
                  return obj.__dict__
 		#template-con
 	
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
