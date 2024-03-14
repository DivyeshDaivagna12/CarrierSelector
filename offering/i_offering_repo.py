from offering.offering_ent import OfferingEntity
from common_methods.i_repository import IRepository
from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")
class IOfferingRepository(IRepository):
      @abstractmethod
      def get_by_id(self, id: str) -> list[OfferingEntity]:
            pass
      def get_by_version(self, id: str, version: int) -> OfferingEntity:
            pass
