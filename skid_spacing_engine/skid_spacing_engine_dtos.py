
from ast import List
from typing import List


class SkidSpacingEngineDetailDto:
        skid_count: int

class Dimension:
        length: float
        width: float
        
class SkidSpacingEngineRequestDto:
        dimensions: List[Dimension]

