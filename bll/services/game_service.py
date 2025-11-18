from typing import List, Optional
from ..models.game import Game
from dal.abstract_repo import AbstractRepository  # Імпортуємо абстракцію
from ..exceptions import GameNotFoundException, InvalidGameDataException, PlayerAlreadyInGameException

class GameService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def add_game(self, date: str, location: str, opponent_team: str,
                 spectators: int = 0, result: str = "не проведена", stadium_id: Optional[int] = None) -> Game:
        if not date or not location or not opponent_team:
            raise InvalidGameDataException("Дата, місце та команда-суперник є обов'язковими полями")

        game = Game(date=date, location=location, opponent_team=opponent_team,
                    spectators=spectators, result=result, stadium_id=stadium_id)
        return self.repository.add(game)

    def get_all_games(self) -> List[Game]:
        return self.repository.get_all()

    def get_game(self, game_id: int) -> Game:
        game = self.repository.get_by_id(game_id)
        if not game:
            raise GameNotFoundException(f"Гра з ID {game_id} не знайдена")
        return game

    def update_game(self, game_id: int, **kwargs) -> Game:
        game = self.repository.update(game_id, **kwargs)
        if not game:
            raise GameNotFoundException(f"Гра з ID {game_id} не знайдена")
        return game

    def delete_game(self, game_id: int) -> bool:
        if not self.repository.delete(game_id):
            raise GameNotFoundException(f"Гра з ID {game_id} не знайдена")
        return True

    def add_player_to_game(self, game_id: int, player_id: int):
        game = self.get_game(game_id)
        if player_id in game.players:
            raise PlayerAlreadyInGameException(f"Гравець {player_id} вже доданий до гри {game_id}")
        game.add_player(player_id)
        self.repository._save_data()

    def remove_player_from_game(self, game_id: int, player_id: int):
        game = self.get_game(game_id)
        game.remove_player(player_id)
        self.repository._save_data()

    def search_games(self, date: str = "", opponent_team: str = "") -> List[Game]:
        all_games = self.repository.get_all()
        results = all_games

        if date:
            results = [game for game in results if date in game.date]
        if opponent_team:
            results = [game for game in results if opponent_team.lower() in game.opponent_team.lower()]

        return results

    def sort_games_by_date(self) -> List[Game]:
        games = self.repository.get_all()
        return sorted(games, key=lambda x: x.date)

    def get_games_by_result(self) -> dict:
        games = self.repository.get_all()
        categorized = {
            "Виграні": [],
            "Програні": [],
            "Нічия": [],
            "Ще не проведені": []
        }

        for game in games:
            if game.result == "не проведена":
                categorized["Ще не проведені"].append(game)
            elif "перемога" in game.result.lower():
                categorized["Виграні"].append(game)
            elif "поразка" in game.result.lower():
                categorized["Програні"].append(game)
            elif "нічия" in game.result.lower():
                categorized["Нічия"].append(game)

        return categorized

    def get_games_by_stadium(self, stadium_id: int) -> List[Game]:
        """Повертає всі ігри, пов'язані з конкретним стадіоном"""
        all_games = self.repository.get_all()
        return [game for game in all_games if game.stadium_id == stadium_id]