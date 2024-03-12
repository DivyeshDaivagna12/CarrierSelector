from pydantic import BaseModel
class CustomerSurchargeDetailDto:
        service:str
        price:float
        is_active:bool
 
class CustomerSurchargeSetDto(BaseModel):
        service:str
        price:float
        is_active:bool
