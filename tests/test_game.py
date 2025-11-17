import unittest
import os
from bll.services.game_service import GameService
from bll.exceptions import GameNotFoundException, InvalidGameDataException


class TestGameService(unittest.TestCase):
    def setUp(self):
        self.service = GameService()
        self.test_filename = "games.json"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_game(self):
        game = self.service.add_game("2024-05-01", "Стадіон", "Команда А", 1000, "перемога")
        self.assertEqual(game.date, "2024-05-01")
        self.assertEqual(game.opponent_team, "Команда А")

    def test_add_game_with_stadium(self):
        game = self.service.add_game("2024-05-01", "Стадіон", "Команда А", 1000, "перемога", 1)
        self.assertEqual(game.date, "2024-05-01")
        self.assertEqual(game.opponent_team, "Команда А")
        self.assertEqual(game.stadium_id, 1)

    def test_add_game_invalid_data(self):
        with self.assertRaises(InvalidGameDataException):
            self.service.add_game("", "Стадіон", "Команда А", 1000, "перемога")

    def test_get_game(self):
        game = self.service.add_game("2024-05-01", "Стадіон", "Команда А", 1000, "перемога")
        retrieved_game = self.service.get_game(game.id)
        self.assertEqual(game.id, retrieved_game.id)

    def test_get_nonexistent_game(self):
        with self.assertRaises(GameNotFoundException):
            self.service.get_game(999)

    def test_search_games(self):
        self.service.add_game("2024-05-01", "Стадіон 1", "УнікальнаКомандаА", 1000, "перемога")
        self.service.add_game("2024-06-01", "Стадіон 2", "УнікальнаКомандаБ", 2000, "поразка")

        results = self.service.search_games(opponent_team="УнікальнаКомандаА")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].opponent_team, "УнікальнаКомандаА")

    def test_search_games_by_date(self):
        self.service.add_game("2024-05-01", "Стадіон 1", "Команда А", 1000, "перемога")
        self.service.add_game("2024-06-01", "Стадіон 2", "Команда Б", 2000, "поразка")

        results = self.service.search_games(date="2024-05-01")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].date, "2024-05-01")

    def test_search_games_empty_result(self):
        self.service.add_game("2024-05-01", "Стадіон 1", "Команда А", 1000, "перемога")

        results = self.service.search_games(opponent_team="НеіснуючаКоманда")
        self.assertEqual(len(results), 0)

    def test_sort_games_by_date(self):
        self.service.add_game("2024-06-01", "Стадіон 2", "Команда Б", 2000, "поразка")
        self.service.add_game("2024-05-01", "Стадіон 1", "Команда А", 1000, "перемога")

        sorted_games = self.service.sort_games_by_date()
        self.assertEqual(sorted_games[0].date, "2024-05-01")
        self.assertEqual(sorted_games[1].date, "2024-06-01")

    def test_get_games_by_result(self):
        self.service.add_game("2024-05-01", "Стадіон 1", "Команда А", 1000, "перемога")
        self.service.add_game("2024-06-01", "Стадіон 2", "Команда Б", 2000, "поразка")
        self.service.add_game("2024-07-01", "Стадіон 3", "Команда В", 1500, "нічия")
        self.service.add_game("2024-08-01", "Стадіон 4", "Команда Г", 0, "не проведена")

        categorized = self.service.get_games_by_result()
        self.assertEqual(len(categorized["Виграні"]), 1)
        self.assertEqual(len(categorized["Програні"]), 1)
        self.assertEqual(len(categorized["Нічия"]), 1)
        self.assertEqual(len(categorized["Ще не проведені"]), 1)

    def test_update_game(self):
        game = self.service.add_game("2024-05-01", "Стадіон", "Команда А", 1000, "перемога")
        updated_game = self.service.update_game(game.id, result="нова перемога", spectators=1500)
        self.assertEqual(updated_game.result, "нова перемога")
        self.assertEqual(updated_game.spectators, 1500)

    def test_delete_game(self):
        game = self.service.add_game("2024-05-01", "Стадіон", "Команда А", 1000, "перемога")
        result = self.service.delete_game(game.id)
        self.assertTrue(result)
        with self.assertRaises(GameNotFoundException):
            self.service.get_game(game.id)

    def test_add_player_to_game(self):
        game = self.service.add_game("2024-05-01", "Стадіон", "Команда А", 1000, "перемога")
        self.service.add_player_to_game(game.id, 1)
        game = self.service.get_game(game.id)
        self.assertIn(1, game.players)

    def test_remove_player_from_game(self):
        game = self.service.add_game("2024-05-01", "Стадіон", "Команда А", 1000, "перемога")
        self.service.add_player_to_game(game.id, 1)
        self.service.remove_player_from_game(game.id, 1)
        game = self.service.get_game(game.id)
        self.assertNotIn(1, game.players)

    def test_get_games_by_stadium(self):
        self.service.add_game("2024-05-01", "Стадіон 1", "Команда А", 1000, "перемога", 1)
        self.service.add_game("2024-06-01", "Стадіон 2", "Команда Б", 2000, "поразка", 2)
        self.service.add_game("2024-07-01", "Стадіон 1", "Команда В", 1500, "нічия", 1)

        stadium_1_games = self.service.get_games_by_stadium(1)
        self.assertEqual(len(stadium_1_games), 2)
        self.assertEqual(stadium_1_games[0].opponent_team, "Команда А")
        self.assertEqual(stadium_1_games[1].opponent_team, "Команда В")

    def test_get_games_by_stadium_nonexistent(self):
        # Перевіряємо пошук ігор для неіснуючого стадіону
        self.service.add_game("2024-05-01", "Стадіон 1", "Команда А", 1000, "перемога", 1)

        stadium_999_games = self.service.get_games_by_stadium(999)
        self.assertEqual(len(stadium_999_games), 0)

    def test_game_serialization_with_stadium(self):
        # Створюємо гру з stadium_id
        game = self.service.add_game("2024-05-01", "Стадіон", "Команда А", 1000, "перемога", 5)

        # Перезавантажуємо дані
        new_service = GameService()
        reloaded_game = new_service.get_game(game.id)

        self.assertEqual(reloaded_game.stadium_id, 5)
        self.assertEqual(reloaded_game.date, "2024-05-01")
        self.assertEqual(reloaded_game.opponent_team, "Команда А")

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)


if __name__ == '__main__':
    unittest.main()