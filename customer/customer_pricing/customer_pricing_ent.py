from ast import List
import json
from uuid import UUID
# from domain.custom_encoder import CustomeEncoder
# from domain.dtos.customer_pricing_dtos import *
from customer_pricing.customer_pricing_dtos import CustomerPricingDetailDto, CustomerPricingSetDto


class CustomerPricingEntity():

    packing_type:str 
    product:str
    rate_code:str
    one_to_two_skid_space:float
    three_to_four_skid_space:float
    five_to_six_skid_space:float
    first_loose_piece:float
    additional_loose_piece_percentage:float
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->CustomerPricingDetailDto:
        dto = CustomerPricingDetailDto()
        dto.packing_type = self.packing_type
        dto.product = self.product
        dto.rate_code = self.rate_code
        dto.one_to_two_skid_space = float(self.one_to_two_skid_space)
        dto.three_to_four_skid_space = float(self.three_to_four_skid_space)
        dto.five_to_six_skid_space = float(self.five_to_six_skid_space)
        dto.first_loose_piece = float(self.first_loose_piece)
        dto.additional_loose_piece_percentage = float(self.additional_loose_piece_percentage)    
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:CustomerPricingSetDto):
        self.packing_type = dto.packing_type
        self.product = dto.product
        self.rate_code = dto.rate_code
        self.one_to_two_skid_space = str(dto.one_to_two_skid_space)
        self.three_to_four_skid_space = str(dto.three_to_four_skid_space)
        self.five_to_six_skid_space = str(dto.five_to_six_skid_space)
        self.first_loose_piece = str(dto.first_loose_piece)
        self.additional_loose_piece_percentage = str(dto.additional_loose_piece_percentage)
        self.is_active = dto.is_active
        return self
