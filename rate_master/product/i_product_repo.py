from abc import abstractmethod
from rate_master.common_methods.i_repository import IRepository

class IProductRepository(IRepository):
      abstractmethod
      def create(self) -> None:
            pass