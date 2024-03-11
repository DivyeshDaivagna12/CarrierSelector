
from ast import List
from aws_lambda_powertools.utilities.parser import parse, BaseModel, ValidationError
from typing import List, Optional


class SkidSpacingEngineDetailDto:
        skid_count: int

class Dimension(BaseModel):
        length: float
        width: float
        
class SkidSpacingEngineRequestDto(BaseModel):
        dimensions: List[Dimension]

