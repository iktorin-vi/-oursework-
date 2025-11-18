from typing import Optional


class BaseModel:

    def __init__(self, id: Optional[int] = None):
        self.id = id

    def to_dict(self) -> dict:
        return {
            'id': self.id
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ID: {self.id}"