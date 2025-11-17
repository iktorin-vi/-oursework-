import unittest
import os
from bll.services.player_service import PlayerService
from bll.exceptions import PlayerNotFoundException


class TestPlayerService(unittest.TestCase):
    def setUp(self):
        self.service = PlayerService()
        self.test_filename = "players.json"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_player(self):
        player = self.service.add_player("John", "Doe", "1990-01-01", "активний", "здоровий", 1000.0)
        self.assertEqual(player.first_name, "John")
        self.assertEqual(player.last_name, "Doe")
        self.assertEqual(player.salary, 1000.0)

    def test_get_player(self):
        player = self.service.add_player("John", "Doe", "1990-01-01", "активний", "здоровий", 1000.0)
        retrieved_player = self.service.get_player(player.id)
        self.assertEqual(player.id, retrieved_player.id)

    def test_get_nonexistent_player(self):
        with self.assertRaises(PlayerNotFoundException):
            self.service.get_player(999)

    def test_update_player(self):
        player = self.service.add_player("John", "Doe", "1990-01-01", "активний", "здоровий", 1000.0)
        updated_player = self.service.update_player(player.id, first_name="Jane", salary=1500.0)
        self.assertEqual(updated_player.first_name, "Jane")
        self.assertEqual(updated_player.salary, 1500.0)

    def test_delete_player(self):
        player = self.service.add_player("John", "Doe", "1990-01-01", "активний", "здоровий", 1000.0)
        result = self.service.delete_player(player.id)
        self.assertTrue(result)
        with self.assertRaises(PlayerNotFoundException):
            self.service.get_player(player.id)

    def test_search_players(self):
        self.service.add_player("John", "Doe", "1990-01-01", "активний", "здоровий", 1000.0)
        self.service.add_player("Jane", "Smith", "1992-02-02", "активний", "здоровий", 1200.0)

        results = self.service.search_players("john")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].first_name, "John")

    def test_search_players_by_last_name(self):
        self.service.add_player("John", "Doe", "1990-01-01", "активний", "здоровий", 1000.0)
        self.service.add_player("Jane", "Smith", "1992-02-02", "активний", "здоровий", 1200.0)

        results = self.service.search_players("smi")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].last_name, "Smith")

    def test_get_all_players(self):
        self.service.add_player("John", "Doe", "1990-01-01", "активний", "здоровий", 1000.0)
        self.service.add_player("Jane", "Smith", "1992-02-02", "активний", "здоровий", 1200.0)

        players = self.service.get_all_players()
        self.assertEqual(len(players), 2)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)


if __name__ == '__main__':
    unittest.main()