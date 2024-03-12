from rate_master.common_methods.i_repository import IRepository
from abc import abstractmethod


class ICustomerRepository(IRepository):
      @abstractmethod
      def create(self) -> None:
            pass