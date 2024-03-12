import json
import decimal
from domain.dtos.skid_spacing_dtos import * 
from domain.dtos.skid_spacing_engine_dtos import *
from skid_spacing_engine.common_methods.shared import ConstraintDto 
#template-import

class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ConstraintDto):
            return obj.__dict__   
        if isinstance(obj, decimal.Decimal):
             return str(obj)
        if isinstance(obj, SkidSpacingDetailDto): 
             return obj.__dict__ 
        if isinstance(obj, SkidSpacingEngineDetailDto): 
             return obj.__dict__ 

 		#template-con
 	
        return json.JSONEncoder.default(self,obj)

def custom_serializer(obj) -> str:
    """Your custom serializer function APIGatewayRestResolver will use"""
    return json.dumps(obj, separators=(",", ":"), cls=ResponseEncoder)
