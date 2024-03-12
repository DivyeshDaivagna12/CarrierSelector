import json
from product.common_methods.shared import ConstraintDto, CostDto, ScalePiece, ScaleSkid
from product.product_dtos import ProductDetailDto

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
        if isinstance(obj, ProductDetailDto):
            return obj.__dict__
        return json.JSONEncoder.default(self,obj)

def to_custom_json(obj:any)->str:
   return json.dumps(obj, separators=(",", ":"), cls=CustomeEncoder)