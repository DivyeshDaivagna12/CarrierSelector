from abc import abstractmethod
from rate_master.common_methods.i_repository import IRepository
from rate_master.customer_surcharge_discount.customer_surcharge_discount_ent import CustomerSurchargeDiscountEntity

class ICustomerSurchargeDiscountRepository(IRepository):
      abstractmethod
      def get(self, customer: str,surcharge:str):
            pass
      def create(self, enty:CustomerSurchargeDiscountEntity) -> None:
            pass
