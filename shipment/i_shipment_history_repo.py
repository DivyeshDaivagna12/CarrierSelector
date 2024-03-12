from shipment.common_methods.i_repository import IRepository
from typing import TypeVar

T = TypeVar("T")

class IShipmentHistoryRepository(IRepository):
      def get_by_shipment_date_and_customer(self, shipment_date: int, customer: str) -> list[T]:
        pass
      def get_by_customer(self, customer: str) -> list[T]:
        pass
      def get_by_shipment_date(self, shipment_date: int) -> list[T]:
        pass
      pass