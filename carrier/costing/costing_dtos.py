from ast import List
from pydantic import BaseModel
from typing import List, Optional


class CostingDto(BaseModel):
        route_number: str
        product_details: list
        

