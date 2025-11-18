from typing import List, TypeVar, Type, Optional
from .serializers import DataSerializer
from .abstract_repo import AbstractRepository
from bll.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class JsonRepository(AbstractRepository):

    def __init__(self, data_class: Type[T], filename: str):
        self.data_class = data_class
        self.filename = filename
        self._data = self._load_data()

    def _load_data(self) -> List[T]:
        return DataSerializer.load_from_file(self.data_class, self.filename)

    def _save_data(self):
        DataSerializer.save_to_file(self._data, self.filename)

    def get_all(self) -> List[T]:
        return self._data.copy()

    def get_by_id(self, item_id: int) -> Optional[T]:
        for item in self._data:
            if item.id == item_id:
                return item
        return None

    def add(self, item: T) -> T:
        if not self._data:
            item.id = 1
        else:
            max_id = max(item.id for item in self._data if item.id is not None)
            item.id = max_id + 1
        self._data.append(item)
        self._save_data()
        return item

    def update(self, item_id: int, **kwargs) -> Optional[T]:
        item = self.get_by_id(item_id)
        if item:
            for key, value in kwargs.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            self._save_data()
        return item

    def delete(self, item_id: int) -> bool:
        item = self.get_by_id(item_id)
        if item:
            self._data.remove(item)
            self._save_data()
            return True
        return False

    def find(self, **kwargs) -> List[T]:
        results = self._data
        for key, value in kwargs.items():
            results = [item for item in results if hasattr(item, key) and getattr(item, key) == value]
        return results