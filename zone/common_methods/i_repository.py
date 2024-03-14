from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")
class IRepository(ABC):
    @abstractmethod
    def save(self, enty: T) -> None:
        pass
    def get(self, enty_id: str) -> T:
        pass
    def get_all(self) -> list[T]:
        pass