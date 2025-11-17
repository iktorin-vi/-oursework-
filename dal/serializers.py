import json
import os
from typing import List, TypeVar, Type

T = TypeVar('T')


class DataSerializer:
    @staticmethod
    def save_to_file(data: List[object], filename: str):
        """Збереження даних у JSON файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json_data = [item.__dict__ for item in data]
                json.dump(json_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"Помилка збереження даних: {str(e)}")

    @staticmethod
    def load_from_file(cls: Type[T], filename: str) -> List[T]:
        """Завантаження даних з JSON файлу"""
        try:
            if not os.path.exists(filename):
                return []

            with open(filename, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                return [cls(**item) for item in json_data]
        except Exception as e:
            raise Exception(f"Помилка завантаження даних: {str(e)}")