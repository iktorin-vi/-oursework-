from typing import List, Dict, Any
from ..models.stadium import Stadium
from dal.repositories import Repository
from ..exceptions import StadiumNotFoundException


class StadiumService:
    def __init__(self, game_service=None):
        self.repository = Repository(Stadium, "stadiums.json")
        self.game_service = game_service

    def add_stadium(self, name: str, capacity: int, price_per_seat: float) -> Stadium:
        stadium = Stadium(name=name, capacity=capacity, price_per_seat=price_per_seat)
        return self.repository.add(stadium)

    def get_all_stadiums(self) -> List[Stadium]:
        return self.repository.get_all()

    def get_stadium(self, stadium_id: int) -> Stadium:
        stadium = self.repository.get_by_id(stadium_id)
        if not stadium:
            raise StadiumNotFoundException(f"Стадіон з ID {stadium_id} не знайдений")
        return stadium

    def update_stadium(self, stadium_id: int, **kwargs) -> Stadium:
        stadium = self.repository.update(stadium_id, **kwargs)
        if not stadium:
            raise StadiumNotFoundException(f"Стадіон з ID {stadium_id} не знайдений")
        return stadium

    def delete_stadium(self, stadium_id: int) -> bool:
        if not self.repository.delete(stadium_id):
            raise StadiumNotFoundException(f"Стадіон з ID {stadium_id} не знайдений")
        return True

    def search_stadiums(self, name: str) -> List[Stadium]:
        all_stadiums = self.repository.get_all()
        return [stadium for stadium in all_stadiums if name.lower() in stadium.name.lower()]

    def get_stadium_games_info(self, stadium_id: int) -> List[Dict[str, Any]]:
        """Повертає інформацію про ігри, заплановані на стадіоні"""
        # Перевіряємо, чи існує стадіон
        try:
            self.get_stadium(stadium_id)
        except StadiumNotFoundException:
            return []

        if not self.game_service:
            return []

        stadium_games = self.game_service.get_games_by_stadium(stadium_id)
        games_info = []

        for game in stadium_games:
            games_info.append({
                'game_id': game.id,
                'date': game.date,
                'opponent_team': game.opponent_team,
                'result': game.result,
                'spectators': game.spectators,
                'location': game.location
            })

        return games_info

    def get_stadium_with_games_info(self, stadium_id: int) -> Dict[str, Any]:
        """Повертає повну інформацію про стадіон разом з іграми"""
        stadium = self.get_stadium(stadium_id)
        games_info = self.get_stadium_games_info(stadium_id)

        return {
            'stadium': stadium,
            'games': games_info
        }