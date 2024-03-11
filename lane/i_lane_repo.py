from domain.interfaces.i_repository import IRepository
from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")
class ILaneRepository(IRepository):
      @abstractmethod
      def create(self) -> None:
            pass
      def get_by_carrierId(self, carrierId: str) -> list[T]:
            pass
      