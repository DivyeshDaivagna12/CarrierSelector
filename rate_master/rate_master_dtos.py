
from ast import List
from typing import List, Optional

class ProductDetail:
        product: str
        services: List[str]
        skids: Optional[int]
        pieces: Optional[int]

class SurchargeBaseCost:
        surcharge_name: str
        surcharge_cost: float

class ProductDiscountPercentage:
        product_name: str
        product_discount: float

class SurchargesDiscountPercentage:
        surcharge_name: str
        surcharge_discount: float

class DiscountPercentage:
        product_discount_percentage: ProductDiscountPercentage
        surcharges_discount_percentage: List[SurchargesDiscountPercentage]

class ProductDiscountAmount:
        product_name: str
        product_discount_amount: float

class SurchargesDiscountAmount:
        surcharge_name: str
        surcharge_discount_amount: float

class DiscountAmount:
        product_discount_amount: ProductDiscountAmount
        surcharges_discount_amount: List[SurchargesDiscountAmount]

class ProductFinalPrice:
        product_name: str
        final_product_price: float

class SurchargeFinalPrice:
        surcharge_name: str
        surcharge_final_price: float

class FinalPrice:
        product_final_price: ProductFinalPrice
        surcharges_final_price: List[SurchargeFinalPrice]

class ProductRateDetailDto:
        base_product_cost: float
        base_surcharges_cost: List[SurchargeBaseCost]
        discount_percentage: DiscountPercentage
        discount_amount: DiscountAmount
        final_price: FinalPrice
        total_amount: float

class RateMasterDetailDto:
        pricing: List[ProductRateDetailDto]
        final_total_amount: float

 
class RateMasterSetDto(BaseModel):
        customer_number: str
        origin_fsa: str
        destination_fsa: str
        product_details: List[ProductDetail]

