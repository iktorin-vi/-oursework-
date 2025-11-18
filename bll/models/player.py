from datetime import datetime
from typing import Optional
from bll.models.base import BaseModel


class Player(BaseModel):
    def __init__(self, id: Optional[int] = None, first_name: str = "", last_name: str = "",
                 birth_date: str = "", status: str = "активний",
                 health_status: str = "здоровий", salary: float = 0.0):
        super().__init__(id)

        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.status = status
        self.health_status = health_status
        self.salary = salary

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return (f"Гравець {self.id}: {self.full_name}, "
                f"Дата народження: {self.birth_date}, "
                f"Статус: {self.status}, Здоров'я: {self.health_status}, "
                f"Зарплата: {self.salary}")

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'status': self.status,
            'health_status': self.health_status,
            'salary': self.salary
        })
        return base_dict