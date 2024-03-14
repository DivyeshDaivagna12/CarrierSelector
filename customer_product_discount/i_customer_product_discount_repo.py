from abc import abstractmethod
from customer_product_discount.customer_product_discount_ent import CustomerProductDiscountEntity
from common_methods.i_repository import IRepository

class ICustomerProductDiscountRepository(IRepository):
      abstractmethod
      def get(self, customer: str,product:str,rate_code:str):
            pass
      def create(self, enty:CustomerProductDiscountEntity) -> None:
            pass
