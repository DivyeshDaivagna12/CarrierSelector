from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class CostingDto(BaseModel):
        route_number: str
        product_details: list
        

