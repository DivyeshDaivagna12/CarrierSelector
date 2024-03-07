from uuid import uuid4
from  domain.entities.customer_ent import CustomerEntity
from domain.dtos.customer_dtos import *
from domain.exceptions.not_found_exce import RescourceNotFoundException
from domain.interfaces.i_customer_repo import ICustomerRepository

class CustomerService:
    def __init__(self, repo: ICustomerRepository):
        self.repo = repo
 
    def create(self, dto: CustomerSetDto)->None:
        enty = CustomerEntity()
        enty.set(dto)
        self.repo.create(enty)
    
    def update(self, dto: CustomerSetDto)->None:
        enty = CustomerEntity()
        enty.set(dto)
        self.repo.save(enty)
  
    def get(self, id: str)->CustomerDetailDto:
       enty = self.repo.get_by_id(id)
       if enty is None:raise RescourceNotFoundException(f"Customer {id} not found")
       return enty.to_dto()
    
    def get_all(self)->list[CustomerDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 