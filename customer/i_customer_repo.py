from domain.interfaces.i_repository import IRepository
from abc import ABC, abstractmethod


class ICustomerRepository(IRepository):
      @abstractmethod
      def create(self) -> None:
            pass