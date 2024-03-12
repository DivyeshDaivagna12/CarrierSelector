from uuid import uuid4
from skid_spacing.i_skid_spacing_repo import ISkidSpacingRepository
from skid_spacing.common_methods.not_found_exce import RescourceNotFoundException
from skid_spacing.skid_spacing_dtos import SkidSpacingDetailDto, SkidSpacingSetDto
from skid_spacing.skid_spacing_ent import SkidSpacingEntity

class SkidSpacingService:
    def __init__(self, repo: ISkidSpacingRepository):
        self.repo = repo
 
    def set(self, dto: SkidSpacingSetDto)->None:
        enty = SkidSpacingEntity()
        if dto.id is None:
            dto.id = uuid4().hex
        enty.set(dto)
        self.repo.save(enty)

    def get(self, id: str)->SkidSpacingDetailDto:
       enty = self.repo.get_by_id(id)
       if enty is None:raise RescourceNotFoundException(f"SkidSpacing {id} not found")
       return enty.to_dto()
    
    def get_all(self)->list[SkidSpacingDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 