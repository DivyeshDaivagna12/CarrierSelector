from abc import abstractmethod
from domain.entities.customer_surcharge_discount_ent import CustomerSurchargeDiscountEntity
from domain.interfaces.i_repository import IRepository

class ICustomerSurchargeDiscountRepository(IRepository):
      abstractmethod
      def get(self, customer: str,surcharge:str):
            pass
      def create(self, enty:CustomerSurchargeDiscountEntity) -> None:
            pass
