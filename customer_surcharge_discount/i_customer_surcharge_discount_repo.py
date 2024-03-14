from abc import abstractmethod
from customer_surcharge_discount.customer_surcharge_discount_ent import CustomerSurchargeDiscountEntity
from common_methods.i_repository import IRepository

class ICustomerSurchargeDiscountRepository(IRepository):
      abstractmethod
      def get(self, customer: str,surcharge:str):
            pass
      def create(self, enty:CustomerSurchargeDiscountEntity) -> None:
            pass
