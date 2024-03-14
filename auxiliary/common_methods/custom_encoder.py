import json

# from domain.dtos.product_dtos import *
# from domain.dtos.offering_dtos import *
# from domain.dtos.carrier_selection_dtos import *
# from domain.dtos.skid_spacing_engine_dtos import *
# from domain.dtos.rate_master_dtos import *
# from domain.dtos.carrier_candidate_dtos import *
from common_methods.shared import *

class CustomeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ConstraintDto):
            return obj.__dict__
        if isinstance(obj, CostDto):
            return obj.__dict__
        if isinstance(obj, ScaleSkid):
            return obj.__dict__
        if isinstance(obj, ScalePiece):
            return obj.__dict__
       
        return json.JSONEncoder.default(self,obj)

def to_custom_json(obj:any)->str:
   return json.dumps(obj, separators=(",", ":"), cls=CustomeEncoder)