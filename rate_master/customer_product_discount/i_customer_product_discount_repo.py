from abc import abstractmethod
from rate_master.common_methods.i_repository import IRepository
from rate_master.customer_product_discount.customer_product_discount_ent import CustomerProductDiscountEntity

class ICustomerProductDiscountRepository(IRepository):
      abstractmethod
      def get(self, customer: str,product:str,rate_code:str):
            pass
      def create(self, enty:CustomerProductDiscountEntity) -> None:
            pass
