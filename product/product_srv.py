from product.i_product_repo import IProductRepository
from product.product_ent import ProductEntity
from product.product_dtos import *
from product.common_methods.not_found_exce import RescourceNotFoundException


class ProductService:
    def __init__(self, repo: IProductRepository):
        self.repo = repo
 
    def create(self, dto: ProductSetDto)->None:
        enty = ProductEntity()
        enty.set(dto)
        self.repo.create(enty)
    
    def update(self, dto: ProductSetDto)->None:
        enty = ProductEntity()
        enty.set(dto)
        self.repo.save(enty)

    def get(self, id: str)->ProductDetailDto:
       enty = self.repo.get_by_id(id)
       if enty is None:raise RescourceNotFoundException(f"Product {id} not found")
       return enty.to_dto()
    
    def get_all(self)->list[ProductDetailDto]:
       list_dto = list()
       entities = self.repo.get_all()
       for enty in entities:
          try:
            list_dto .append(enty.to_dto())
          except:
           pass
       return list_dto
 