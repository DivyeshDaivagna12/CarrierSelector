from abc import abstractmethod
from domain.interfaces.i_repository import IRepository

class IProductRepository(IRepository):
      abstractmethod
      def create(self) -> None:
            pass