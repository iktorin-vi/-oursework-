from typing import List, Optional
from bll.models.base import BaseModel


class Stadium(BaseModel):  # Наслідуємо від BaseModel
    def __init__(self, id: Optional[int] = None, name: str = "", capacity: int = 0,
                 price_per_seat: float = 0.0, scheduled_games: Optional[List[int]] = None):
        # Викликаємо конструктор батьківського класу
        super().__init__(id)

        self.name = name
        self.capacity = capacity
        self.price_per_seat = price_per_seat
        self.scheduled_games = scheduled_games if scheduled_games is not None else []

    def add_game(self, game_id: int):
        if game_id not in self.scheduled_games:
            self.scheduled_games.append(game_id)

    def remove_game(self, game_id: int):
        if game_id in self.scheduled_games:
            self.scheduled_games.remove(game_id)

    def __str__(self) -> str:
        return (f"Стадіон {self.id}: {self.name}, "
                f"Місць: {self.capacity}, Ціна за місце: {self.price_per_seat}, "
                f"Заплановано ігор: {len(self.scheduled_games)}")

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name,
            'capacity': self.capacity,
            'price_per_seat': self.price_per_seat,
            'scheduled_games': self.scheduled_games
        })
        return base_dict