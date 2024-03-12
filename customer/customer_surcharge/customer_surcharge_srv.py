from uuid import uuid4
from customer_surcharge_ent import CustomerSurchargeEntity
from customer_surcharge_dtos import *
from domain.exceptions.bad_request_exce import BadRequestException
from domain.exceptions.not_found_exce import RescourceNotFoundException
from i_customer_surcharge_repo import ICustomerSurchargeRepository
from domain.constants import excessive_skid_id,excessive_skid_desc

class CustomerSurchargeService:
    def __init__(self, repo: ICustomerSurchargeRepository):
        self.repo = repo

    def create(self, dto: CustomerSurchargeSetDto)->None:
        enty = CustomerSurchargeEntity()           
        enty.set(dto)
        self.repo.create(enty)
 
    def set(self, dto: CustomerSurchargeSetDto)->None:
        if dto.service == excessive_skid_id and dto.is_active == False:
            raise BadRequestException(f"{excessive_skid_desc} can not be deactivated")

        enty = CustomerSurchargeEntity()           
        enty.set(dto)
        self.repo.save(enty)

    def get(self, service: str)->CustomerSurchargeDetailDto:
       enty = self.repo.get_by_service(service)
       if enty is None:raise RescourceNotFoundException(f"CustomerSurcharge {service} not found")
       return enty.to_dto()
    
    def add_system_surcharges(self)->None:
        enty = CustomerSurchargeEntity()
        enty.service = excessive_skid_id
        enty.price = "0"
        enty.is_active = True
        self.repo.save(enty)
    
    def get_all(self)->list[CustomerSurchargeDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 