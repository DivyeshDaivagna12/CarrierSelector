
from ast import List
from typing import List, Optional
#from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError

class CustomerPricingDetailDto:
        packing_type:str 
        product:str
        rate_code:str
        one_to_two_skid_space:float
        three_to_four_skid_space:float
        five_to_six_skid_space:float
        first_loose_piece:float
        additional_loose_piece_percentage:float
        is_active:bool
 
class CustomerPricingSetDto:
        packing_type:str 
        product:str
        rate_code:str
        one_to_two_skid_space:float
        three_to_four_skid_space:float
        five_to_six_skid_space:float
        first_loose_piece:float
        additional_loose_piece_percentage:float
        is_active:bool





        

