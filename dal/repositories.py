from typing import List, TypeVar, Type
from .serializers import DataSerializer

T = TypeVar('T')

class Repository:
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

    def get_by_id(self, item_id: int) -> T:
        for item in self._data:
            if getattr(item, 'id', None) == item_id:
                return item
        return None

    def add(self, item: T) -> T:
        if not self._data:
            item.id = 1
        else:
            max_id = max(getattr(i, 'id', 0) for i in self._data)
            item.id = max_id + 1
        self._data.append(item)
        self._save_data()
        return item

    def update(self, item_id: int, **kwargs) -> T:
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