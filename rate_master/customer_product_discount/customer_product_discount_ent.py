
from rate_master.customer_product_discount.customer_product_discount_dtos import CustomerProductDiscountDetailDto, CustomerProductDiscountSetDto


class CustomerProductDiscountEntity():
    customer:str
    product:str
    rate_code:str
    discount:str
    is_active:bool
    additional_piece_discount:str
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->CustomerProductDiscountDetailDto:
        dto = CustomerProductDiscountDetailDto()
        dto.product = self.product
        dto.customer = self.customer
        dto.rate_code = self.rate_code
        dto.discount = self.discount
        dto.is_active = self.is_active
        dto.additional_piece_discount = self.additional_piece_discount
        return dto
    
    def set(self, dto:CustomerProductDiscountSetDto):
        self.product = dto.product
        self.customer = dto.customer
        self.rate_code = dto.rate_code
        self.discount = dto.discount
        self.is_active = dto.is_active
        self.additional_piece_discount = dto.additional_piece_discount
        return self
