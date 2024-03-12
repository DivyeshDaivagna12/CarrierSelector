from domain.interfaces.i_repository import IRepository
from typing import TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")
class ICarrierOfferingRepository(IRepository):
      @abstractmethod
      def get_by_carrierId(self, carrierId: str) -> list[T]:
            pass
      