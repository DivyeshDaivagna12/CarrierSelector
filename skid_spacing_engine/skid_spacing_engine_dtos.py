
from ast import List
from pydantic import BaseModel
from typing import List


class SkidSpacingEngineDetailDto:
        skid_count: int

class Dimension(BaseModel):
        length: float
        width: float
        
class SkidSpacingEngineRequestDto(BaseModel):
        dimensions: List[Dimension]

