from typing import List, Optional
from bll.models.base import BaseModel

class Game(BaseModel):
    def __init__(self, id: Optional[int] = None, date: str = "", location: str = "",
                 opponent_team: str = "", spectators: int = 0, result: str = "не проведена",
                 players: Optional[List[int]] = None, stadium_id: Optional[int] = None):
        super().__init__(id)

        self.date = date
        self.location = location
        self.opponent_team = opponent_team
        self.spectators = spectators
        self.result = result
        self.players = players if players is not None else []
        self.stadium_id = stadium_id

    def add_player(self, player_id: int):
        if player_id not in self.players:
            self.players.append(player_id)

    def remove_player(self, player_id: int):
        if player_id in self.players:
            self.players.remove(player_id)

    def __str__(self) -> str:
        stadium_info = f", Стадіон ID: {self.stadium_id}" if self.stadium_id else ""
        return (f"Гра {self.id}: {self.date} проти {self.opponent_team}, "
                f"Місце: {self.location}, Глядачі: {self.spectators}, "
                f"Результат: {self.result}, Гравців: {len(self.players)}{stadium_info}")

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            'date': self.date,
            'location': self.location,
            'opponent_team': self.opponent_team,
            'spectators': self.spectators,
            'result': self.result,
            'players': self.players,
            'stadium_id': self.stadium_id
        })
        return base_dict