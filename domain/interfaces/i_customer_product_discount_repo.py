from abc import abstractmethod
from domain.entities.customer_product_discount_ent import CustomerProductDiscountEntity
from domain.interfaces.i_repository import IRepository

class ICustomerProductDiscountRepository(IRepository):
      abstractmethod
      def get(self, customer: str,product:str,rate_code:str):
            pass
      def create(self, enty:CustomerProductDiscountEntity) -> None:
            pass
