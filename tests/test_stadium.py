import unittest
import os
from bll.services.stadium_service import StadiumService
from bll.services.game_service import GameService
from bll.exceptions import StadiumNotFoundException


class TestStadiumService(unittest.TestCase):
    def setUp(self):
        # Спочатку створюємо GameService
        self.game_service = GameService()
        # Потім передаємо його в StadiumService
        self.stadium_service = StadiumService(self.game_service)

        self.stadium_filename = "stadiums.json"
        self.game_filename = "games.json"

        # Очищаємо тестові файли
        for filename in [self.stadium_filename, self.game_filename]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_add_stadium(self):
        stadium = self.stadium_service.add_stadium("Стадіон", 50000, 100.0)
        self.assertEqual(stadium.name, "Стадіон")
        self.assertEqual(stadium.capacity, 50000)
        self.assertEqual(stadium.price_per_seat, 100.0)

    def test_get_stadium(self):
        stadium = self.stadium_service.add_stadium("Стадіон", 50000, 100.0)
        retrieved_stadium = self.stadium_service.get_stadium(stadium.id)
        self.assertEqual(stadium.id, retrieved_stadium.id)

    def test_get_nonexistent_stadium(self):
        with self.assertRaises(StadiumNotFoundException):
            self.stadium_service.get_stadium(999)

    def test_update_stadium(self):
        stadium = self.stadium_service.add_stadium("Стадіон", 50000, 100.0)
        updated_stadium = self.stadium_service.update_stadium(stadium.id, name="Новий Стадіон", capacity=60000)
        self.assertEqual(updated_stadium.name, "Новий Стадіон")
        self.assertEqual(updated_stadium.capacity, 60000)

    def test_delete_stadium(self):
        stadium = self.stadium_service.add_stadium("Стадіон", 50000, 100.0)
        result = self.stadium_service.delete_stadium(stadium.id)
        self.assertTrue(result)
        with self.assertRaises(StadiumNotFoundException):
            self.stadium_service.get_stadium(stadium.id)

    def test_search_stadiums(self):
        self.stadium_service.add_stadium("Національний стадіон", 70000, 150.0)
        self.stadium_service.add_stadium("Міський стадіон", 25000, 50.0)

        results = self.stadium_service.search_stadiums("Національний")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Національний стадіон")

    def test_search_stadiums_partial_match(self):
        self.stadium_service.add_stadium("Національний стадіон", 70000, 150.0)
        self.stadium_service.add_stadium("Олімпійський стадіон", 80000, 200.0)

        results = self.stadium_service.search_stadiums("стадіон")
        self.assertEqual(len(results), 2)

    def test_get_all_stadiums(self):
        self.stadium_service.add_stadium("Стадіон 1", 50000, 100.0)
        self.stadium_service.add_stadium("Стадіон 2", 60000, 120.0)

        stadiums = self.stadium_service.get_all_stadiums()
        self.assertEqual(len(stadiums), 2)

    def test_get_stadium_games_info(self):
        # Створюємо стадіон
        stadium = self.stadium_service.add_stadium("Тестовий стадіон", 50000, 100.0)

        # Створюємо ігри на цьому стадіоні
        self.game_service.add_game("2024-05-01", "Стадіон 1", "Команда А", 1000, "перемога", stadium.id)
        self.game_service.add_game("2024-06-01", "Стадіон 1", "Команда Б", 2000, "поразка", stadium.id)

        # Переконуємося, що ігри створені
        all_games = self.game_service.get_all_games()
        self.assertEqual(len(all_games), 2)

        # Тестуємо отримання інформації про ігри на стадіоні
        games_info = self.stadium_service.get_stadium_games_info(stadium.id)
        self.assertEqual(len(games_info), 2)
        self.assertEqual(games_info[0]['opponent_team'], "Команда А")
        self.assertEqual(games_info[1]['opponent_team'], "Команда Б")

    def test_get_stadium_with_games_info(self):
        # Створюємо стадіон
        stadium = self.stadium_service.add_stadium("Тестовий стадіон", 50000, 100.0)

        # Створюємо гру на цьому стадіоні
        self.game_service.add_game("2024-05-01", "Стадіон 1", "Команда А", 1000, "перемога", stadium.id)

        # Переконуємося, що гра створена
        all_games = self.game_service.get_all_games()
        self.assertEqual(len(all_games), 1)

        stadium_info = self.stadium_service.get_stadium_with_games_info(stadium.id)
        self.assertEqual(stadium_info['stadium'].id, stadium.id)
        self.assertEqual(len(stadium_info['games']), 1)
        self.assertEqual(stadium_info['games'][0]['opponent_team'], "Команда А")

    def test_get_stadium_games_info_no_games(self):
        # Створюємо стадіон без ігор
        stadium = self.stadium_service.add_stadium("Пустий стадіон", 50000, 100.0)

        games_info = self.stadium_service.get_stadium_games_info(stadium.id)
        self.assertEqual(len(games_info), 0)

    def test_get_stadium_games_info_nonexistent_stadium(self):
        games_info = self.stadium_service.get_stadium_games_info(999)
        self.assertEqual(len(games_info), 0)

    def test_get_stadium_schedule(self):
        """Тест для вимоги 3.4.3"""
        # Створюємо стадіон
        stadium = self.stadium_service.add_stadium("Тестовий стадіон", 5000, 100.0)

        # Створюємо ігри для цього стадіону
        self.game_service.add_game("2024-05-01", "Стадіон А", "Команда А", 1000, "перемога", stadium.id)
        self.game_service.add_game("2024-05-02", "Стадіон Б", "Команда Б", 2000, "поразка")  # Без стадіону

        # Перевіряємо розклад
        schedule = self.stadium_service.get_stadium_schedule(stadium.id)
        self.assertEqual(len(schedule), 1)
        self.assertEqual(schedule[0]['opponent_team'], "Команда А")
        self.assertEqual(schedule[0]['date'], "2024-05-01")

    def tearDown(self):
        # Очищаємо тестові файли
        for filename in [self.stadium_filename, self.game_filename]:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == '__main__':
    unittest.main()