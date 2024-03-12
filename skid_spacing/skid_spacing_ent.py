
from skid_spacing.skid_spacing_dtos import SkidSpacingDetailDto


class SkidSpacingEntity():
    id:str
    skid_space:int
    longest_side_min:str
    longest_side_max:str
    second_longest_side_min:str
    second_longest_side_max:str
    is_active:bool
  
    def __init__(self,prop_dict=None):
        if prop_dict != None:
            self.__dict__ = prop_dict
    
    def to_dto(self)->SkidSpacingDetailDto:
        dto = SkidSpacingDetailDto()
        dto.id = self.id
        dto.skid_space = self.skid_space
        dto.longest_side_min = self.longest_side_min
        dto.longest_side_max = self.longest_side_max
        dto.second_longest_side_min = self.second_longest_side_min
        dto.second_longest_side_max = self.second_longest_side_max
        dto.is_active = self.is_active
        return dto
    
    def set(self, dto:SkidSpacingSetDto):
        self.id = dto.id
        self.skid_space = dto.skid_space
        self.longest_side_min = dto.longest_side_min
        self.longest_side_max = dto.longest_side_max
        self.second_longest_side_min = dto.second_longest_side_min
        self.second_longest_side_max = dto.second_longest_side_max
        self.is_active = dto.is_active
        return self
