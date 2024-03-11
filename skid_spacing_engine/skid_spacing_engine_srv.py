from uuid import uuid4
from domain.dtos.skid_spacing_engine_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from infrastructure.repositories.skid_spacing_repo import SkidSpacingRepository, SkidSpacingEntity
class SkidSpacingEngineService:
    def __init__(self):
        self.skidSpacingRepo = SkidSpacingRepository() 
    # def set(self, dto: SkidSpacingEngineRequestDto)->None:
    #     enty = SkidSpacingEngineEntity()
    #     if dto.id is None:
    #         dto.id = uuid4().hex
            
    #     enty.set(dto)
    #     self.repo.save(enty)

    def get_skids_count(self, dto: SkidSpacingEngineRequestDto)->SkidSpacingEngineDetailDto:
        skidSpacingEntities = self.skidSpacingRepo.get_all()
        sortedskidSpacingEntities = sorted(skidSpacingEntities, key=lambda x: x.skid_space, reverse=False)

        detail = SkidSpacingEngineDetailDto()
        detail.skid_count = 0
        for dimension in dto.dimensions:
            max = 0
            second_max = 0
            if dimension.length >= dimension.width:
                max = dimension.length
                second_max = dimension.width
            else:
                max = dimension.width
                second_max = dimension.length

            found = False
            for skidEntity in sortedskidSpacingEntities:
                if skidEntity.is_active and (max >= float(skidEntity.longest_side_min) and max <= float(skidEntity.longest_side_max)) and (second_max >= float(skidEntity.second_longest_side_min) and second_max <= float(skidEntity.second_longest_side_max)):
                    detail.skid_count += skidEntity.skid_space
                    found = True
                    break
            
            if not found:
                raise RescourceNotFoundException(f"Skid count not found for dimension - Length:'{dimension.length}', Width:'{dimension.width}'")
        
        return detail
    
    # def get_all(self)->list[SkidSpacingEngineDetailDto]:
    #    list_dto = list()
    #    entities = self.repo.get_all()
    #    for enty in entities:
    #       try:
    #         list_dto .append(enty.to_dto())
    #       except:
    #        pass
    #    return list_dto
 