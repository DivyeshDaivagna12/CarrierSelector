import datetime
from uuid import uuid4
from offering.offering_ent import OfferingEntity
from carrier_offering.carrier_offering_ent import CarrierOfferingEntity
from offering.offering_dtos import *
from common_methods.already_exist_exce import AlreadyExistException
from common_methods.bad_request_exce import BadRequestException
from i_offering_repo import IOfferingRepository
from carrier_offering.carrier_offering_repo import CarrierOfferingRepository
from product.product_repo import ProductRepository
from domain.constants import  loss_packaging_id, skid_packaging_id
from datetime import date
import json

class OfferingService:
    def __init__(self, repo: IOfferingRepository):
        self.repo = repo
        self.coRepo = CarrierOfferingRepository()
        self.productRepo = ProductRepository()

 
    def set(self, dto: OfferingSetDto)->None:
        enty = OfferingEntity()
        createFlag = False
        if dto.id is None:
            createFlag = True
            dto.id = uuid4().hex

        self.packaging_and_cost_validation(dto)

        versions = self.repo.get_by_id(dto.id)
        
        # check for more than one future released version
        today = int(date.today().strftime('%Y%m%d'))
        if today < dto.valid_from and dto.status == "RELEASED":
            for version in versions:
               if version.version != dto.version:
                  if today < version.valid_from and version.status == "RELEASED":
                     raise AlreadyExistException(f"More than one Future Released version not allowed. Future released version exists in version '{version.version}'")

           

        for version in versions:
           if dto.version != version.version:
              
              if dto.status == "PLANNING" and version.status == "PLANNING" :
                 raise AlreadyExistException(f"More than one Planning version not allowed. Planning version exists in version '{version.version}'")
              
              if dto.status == "RELEASED" and version.status == "PLANNING" and version.version == (dto.version-1):
                 raise AlreadyExistException(f"Already Planning version exits at top. You cannot release a version.")
              
              if dto.status == "PLANNING" and version.version > dto.version and version.status == "RELEASED":
                 raise AlreadyExistException(f"Planning version cannot be in between.")
              
              if dto.status == "RELEASED" and version.status == "RELEASED" and version.version == (dto.version-1) and dto.valid_from <= version.valid_from:
                 raise AlreadyExistException(f"Valid from cannot be less-than or equal-to to the valid from of previous version")
              
              if dto.status == "RELEASED" and version.status == "RELEASED" and version.version == (dto.version+1) and dto.valid_to >= version.valid_from:
                 raise AlreadyExistException(f"Valid-to is overlapping with next version i.e version '{version.version}'")
            #   if dto.status == "RELEASED" and version.status == "RELEASED":
            #      if dto.valid_from == version.valid_from:
            #         raise AlreadyExistException(f"Valid-From date already exist in offering version '{version.version}'")
        
                   
        enty.set(dto)
        self.repo.save(enty)
        coEnty = CarrierOfferingEntity()
        coEnty.carrier = dto.carrier
        coEnty.offering = dto.id
        coEnty.description = dto.description
        coEnty.is_active = dto.is_active
        self.coRepo.save(coEnty)
        
        #TODO: add with transcation
        if dto.version > 1 and dto.status == "RELEASED" :
           previousVersion = self.repo.get_by_version(dto.id,dto.version-1)
           end_dt = self.int_to_date(dto.valid_from)
           end_dt = end_dt - datetime.timedelta(days=1)
           end_dt_int = int(f'{end_dt:%Y%m%d}')
           previousVersion.valid_to = end_dt_int
           self.repo.save(previousVersion)
           

        # if coFlag:
        #    coEnty = CarrierOfferingEntity()
        #    coEnty.carrier = dto.carrier
        #    coEnty.offering = dto.id
        #    coEnty.description = dto.description
        #    coEnty.is_active = True
        #    self.coRepo.save(coEnty)
        # else:
        #    coEnty = CarrierOfferingEntity()
        #    coEnty.carrier = dto.carrier
        #    coEnty.offering = dto.id
        #    coEnty.description = dto.description
        #    coEnty.is_active = True
        #    self.coRepo.save(coEnty)
    def packaging_and_cost_validation(self, dto: OfferingSetDto):
         product_entity = self.productRepo.get_by_id(dto.product)
         if product_entity is None:
            raise BadRequestException(f"Product with id '{dto.product}' doesnt exist")
         else:
            if product_entity.packaging not in [loss_packaging_id, skid_packaging_id]:
               raise BadRequestException(f"Packaging type 'SKID' and 'LOOSE' is only supported. Product '{product_entity.description}' is not of packaging type 'SKID' or 'LOOSE'")
            elif dto.cost.method == "SCALE":
               if product_entity.packaging == skid_packaging_id and dto.cost.attribute == "PIECES":
                  raise BadRequestException(f"Product packaging type is 'SKID'. Please provide skids costing or fixed costing.")
               if product_entity.packaging == loss_packaging_id and dto.cost.attribute == "SKIDS":
                  raise BadRequestException(f"Product packaging type is 'LOOSE'. Please provide loose(PIECES) costing or fixed costing.")
            
    def get_by_id(self, id: str, filter: str)->List[OfferingDetailDto]:
       list_dto = list()
       today = int(date.today().strftime('%Y%m%d'))

       
       if filter == "all":
         entities = self.repo.get_by_id(id)
         for enty in entities:
            try:
               if enty.is_active:
                  pass
            except:
               enty.is_active = True
                
            try:
               list_dto .append(enty.to_dto())
            except:
               enty.cost = json.dumps(enty.cost)
               try:
                  list_dto .append(enty.to_dto())
               except:
                pass

         return list_dto
       elif filter == "future":
          entities = self.repo.get_by_id(id)
          for enty in entities:
            try:
               if enty.is_active:
                  pass
            except:
               enty.is_active = True
            try:
               if today < enty.valid_from and enty.status == "RELEASED":
                  list_dto .append(enty.to_dto())
            except:
               try:
                  enty.cost = json.dumps(enty.cost)
                  if today < enty.valid_from and enty.status == "RELEASED":
                     list_dto .append(enty.to_dto())
               except:
                  pass 

          return list_dto
       elif filter == "expired":
          entities = self.repo.get_by_id(id)
          for enty in entities:
            try:
               if enty.is_active:
                  pass
            except:
               enty.is_active = True
            try:
               if today > enty.valid_to and enty.status == "RELEASED":
                  list_dto .append(enty.to_dto())
            except:
               try:
                  enty.cost = json.dumps(enty.cost)
                  if today > enty.valid_to and enty.status == "RELEASED":
                     list_dto .append(enty.to_dto())
               except:
                  pass
          return list_dto
       elif filter == "planned":
          entities = self.repo.get_by_id(id)
          for enty in entities:
            try:
               if enty.is_active:
                  pass
            except:
               enty.is_active = True
            try:
               if enty.status == "PLANNING":
                  list_dto .append(enty.to_dto())
            except:
               try:
                  enty.cost = json.dumps(enty.cost)
                  if enty.status == "PLANNING":
                     list_dto .append(enty.to_dto())
               except:
                  pass
          return list_dto  
          
    
    def get_by_carrierId(self, carrierId: str)->List[OfferingDetailDto]:
    
       today = int(date.today().strftime('%Y%m%d'))

       co_entities = self.coRepo.get_by_carrierId(carrierId)

       offering_entities = self.repo.get_all()
       res_dict = dict()

       for offering_entity in offering_entities:
         #  if not (offering_entity.id in res_dict):
         try:
           if offering_entity.is_active:
              pass
         except:
              offering_entity.is_active = True  
         if today >= offering_entity.valid_from and today <= offering_entity.valid_to and offering_entity.status == "RELEASED":
            if not (offering_entity.id in res_dict):
               res_dict[offering_entity.id] = [offering_entity,0,0,0]
            else:
               res_dict[offering_entity.id][0] = offering_entity
         elif today < offering_entity.valid_from and offering_entity.status == "RELEASED":
            if not (offering_entity.id in res_dict):
               res_dict[offering_entity.id] = [None,1,0,0]
            else:
               res_dict[offering_entity.id][1] += 1
         elif today > offering_entity.valid_to and offering_entity.status == "RELEASED":
            if not (offering_entity.id in res_dict):
               res_dict[offering_entity.id] = [None,0,1,0]
            else:
               res_dict[offering_entity.id][2] += 1
         elif offering_entity.status == "PLANNING":
            if not (offering_entity.id in res_dict):
               res_dict[offering_entity.id] = [None,0,0,1]
            else:
               res_dict[offering_entity.id][3] += 1

       res_dto = list()
       for co_entity in co_entities:
          try:
            if co_entity.is_active:
                pass
          except:
              co_entity.is_active = True  
          if co_entity.offering in res_dict and (res_dict[co_entity.offering][0] is not None):
             try:
               dto: OfferingDetailDto = res_dict[co_entity.offering][0].to_dto()
               dto.future = res_dict[co_entity.offering][1]
               dto.expired = res_dict[co_entity.offering][2]
               dto.planned = res_dict[co_entity.offering][3]
               res_dto.append(dto)
             except:
               pass
          else:
             blankOfferingDto = OfferingDetailDto()
             blankOfferingDto.id = co_entity.offering
             blankOfferingDto.description = co_entity.description
             blankOfferingDto.is_active = co_entity.is_active
             if co_entity.offering in res_dict:
               blankOfferingDto.future = res_dict[co_entity.offering][1]
               blankOfferingDto.expired = res_dict[co_entity.offering][2]
               blankOfferingDto.planned = res_dict[co_entity.offering][3]
             else:
               blankOfferingDto.future = 0
               blankOfferingDto.expired = 0
               blankOfferingDto.planned = 0
             res_dto.append(blankOfferingDto)
      
      #  print(res_dto)
       return res_dto
       
       
    #    res_dto = list()
    #    for co_entity in co_entities:
    #         foundFlag = False
    #         entities = self.repo.get_by_id(co_entity.offering)
    #         for enty in entities:
    #             if today >= enty.valid_from and today <= enty.valid_to:
    #                 try:
    #                     res_dto .append(enty.to_dto())
    #                     foundFlag = True
    #                 except:
    #                     pass
    #             if foundFlag:
    #                break
    #         if not foundFlag and len(entities) > 0:
    #            blankOfferingDto = OfferingDetailDto()
    #            blankOfferingDto.id = entities[0].id
    #            blankOfferingDto.description = entities[0].description
    #            res_dto .append(blankOfferingDto)
        
    #    return res_dto
               
    def int_to_date(self, dt:str)->datetime.datetime:
        valid_from = str(dt)
        y = int(valid_from[0:4])
        m = int(valid_from[4:6])
        d = int( valid_from[6:8])
        return datetime.datetime(y, m, d)
    
   
       
                
            
    # def get_all(self)->list[OfferingDetailDto]:
    #    list_dto = list()
    #    entities = self.repo.get_all()
    #    for enty in entities:
    #       try:
    #         list_dto .append(enty.to_dto())
    #       except:
    #        pass
    #    return list_dto
 
