from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")
class IZoneRepository(ABC):
    @abstractmethod
    def get_all_zones(self) -> list[T]:
        pass
    def get_zones_status(self) -> list[U]:
        pass
    def get_zones_for_coordinates(self, address: str) -> list[T]:
        pass
    def update_table_operation(self) -> None:
        pass