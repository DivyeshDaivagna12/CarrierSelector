
from typing import Optional


class SkidSpacingDetailDto:
        id:str
        skid_space:int
        longest_side_min:str
        longest_side_max:str
        second_longest_side_min:str
        second_longest_side_max:str
        is_active:bool
 
class SkidSpacingSetDto:
        id:Optional[str]
        skid_space:int
        longest_side_min:str
        longest_side_max:str
        second_longest_side_min:str
        second_longest_side_max:str
        is_active:bool

