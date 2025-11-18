from typing import List
from ..models.player import Player
from dal.repositories import AbstractRepository
from ..exceptions import PlayerNotFoundException

class PlayerService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def add_player(self, first_name: str, last_name: str, birth_date: str,
                   status: str, health_status: str, salary: float) -> Player:
        player = Player(first_name=first_name, last_name=last_name,
                       birth_date=birth_date, status=status,
                       health_status=health_status, salary=salary)
        return self.repository.add(player)

    def get_all_players(self) -> List[Player]:
        return self.repository.get_all()

    def get_player(self, player_id: int) -> Player:
        player = self.repository.get_by_id(player_id)
        if not player:
            raise PlayerNotFoundException(f"Гравець з ID {player_id} не знайдений")
        return player

    def update_player(self, player_id: int, **kwargs) -> Player:
        player = self.repository.update(player_id, **kwargs)
        if not player:
            raise PlayerNotFoundException(f"Гравець з ID {player_id} не знайдений")
        return player

    def delete_player(self, player_id: int) -> bool:
        if not self.repository.delete(player_id):
            raise PlayerNotFoundException(f"Гравець з ID {player_id} не знайдений")
        return True

    def search_players(self, search_term: str) -> List[Player]:
        all_players = self.repository.get_all()
        return [player for player in all_players
                if search_term.lower() in player.first_name.lower()
                or search_term.lower() in player.last_name.lower()]