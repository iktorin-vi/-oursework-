from abc import ABC, abstractmethod
from typing import List, TypeVar, Optional
from bll.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class AbstractRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def add(self, item: T) -> T:
        pass

    @abstractmethod
    def update(self, item_id: int, **kwargs) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass

    @abstractmethod
    def find(self, **kwargs) -> List[T]:
        pass