import os
from bll.services.player_service import PlayerService
from bll.services.game_service import GameService
from bll.services.stadium_service import StadiumService
from .validators import Validators
from bll.exceptions import *

class ConsoleUI:
    def __init__(self):
        self.player_service = PlayerService()
        self.game_service = GameService()
        # Передаємо game_service в stadium_service
        self.stadium_service = StadiumService(self.game_service)

    # ... решта коду залишається без змін ...

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        print("\n" + "=" * 50)
        print("СИСТЕМА УПРАВЛІННЯ ФУТБОЛЬНИМИ МАТЧАМИ")
        print("=" * 50)
        print("1. Управління гравцями")
        print("2. Управління іграми")
        print("3. Управління стадіонами")
        print("4. Пошук")
        print("0. Вихід")
        print("=" * 50)

    def display_player_menu(self):
        print("\n--- Управління гравцями ---")
        print("1. Додати гравця")
        print("2. Переглянути всіх гравців")
        print("3. Переглянути інформацію про гравця")
        print("4. Змінити дані гравця")
        print("5. Видалити гравця")
        print("0. Назад")

    def display_game_menu(self):
        print("\n--- Управління іграми ---")
        print("1. Додати гру")
        print("2. Переглянути всі ігри")
        print("3. Переглянути інформацію про гру")
        print("4. Змінити дані гри")
        print("5. Видалити гру")
        print("6. Додати гравця до гри")
        print("7. Видалити гравця з гри")
        print("8. Сортування ігор за датою")
        print("9. Сортування ігор за результатом")
        print("0. Назад")

    def display_stadium_menu(self):
        print("\n--- Управління стадіонами ---")
        print("1. Додати стадіон")
        print("2. Переглянути всі стадіони")
        print("3. Переглянути інформацію про стадіон")
        print("4. Змінити дані стадіону")
        print("5. Видалити стадіон")
        print("0. Назад")

    def display_search_menu(self):
        print("\n--- Пошук ---")
        print("1. Пошук гравця за ім'ям або прізвищем")
        print("2. Пошук гри за датою та командою-суперником")
        print("3. Пошук стадіону за назвою")
        print("0. Назад")

    def input_player_data(self):
        print("\nВведіть дані гравця:")
        first_name = input("Ім'я: ")
        while not Validators.validate_name(first_name):
            print("Некоректне ім'я! Мінімум 2 символи.")
            first_name = input("Ім'я: ")

        last_name = input("Прізвище: ")
        while not Validators.validate_name(last_name):
            print("Некоректне прізвище! Мінімум 2 символи.")
            last_name = input("Прізвище: ")

        birth_date = input("Дата народження (РРРР-ММ-ДД): ")
        while not Validators.validate_date(birth_date):
            print("Некоректна дата! Використовуйте формат РРРР-ММ-ДД.")
            birth_date = input("Дата народження (РРРР-ММ-ДД): ")

        status = input("Статус (активний/неактивний): ") or "активний"
        health_status = input("Статус здоров'я: ") or "здоровий"

        salary = input("Зарплата: ")
        while not Validators.validate_salary(salary):
            print("Некоректна зарплата! Введіть додатнє число.")
            salary = input("Зарплата: ")

        return first_name, last_name, birth_date, status, health_status, float(salary)

    def input_game_data(self):
        print("\nВведіть дані гри:")
        date = input("Дата проведення (РРРР-ММ-ДД): ")
        while not Validators.validate_date(date):
            print("Некоректна дата! Використовуйте формат РРРР-ММ-ДД.")
            date = input("Дата проведення (РРРР-ММ-ДД): ")

        location = input("Місце проведення: ")
        while not location.strip():
            print("Місце проведення не може бути порожнім!")
            location = input("Місце проведення: ")

        opponent_team = input("Команда-суперник: ")
        while not opponent_team.strip():
            print("Команда-суперник не може бути порожньою!")
            opponent_team = input("Команда-суперник: ")

        spectators = input("Кількість глядачів: ") or "0"
        while not Validators.validate_spectators(spectators):
            print("Некоректна кількість глядачів!")
            spectators = input("Кількість глядачів: ") or "0"

        result = input("Результат (залишити порожнім якщо гра ще не проведена): ") or "не проведена"

        return date, location, opponent_team, int(spectators), result

    def input_stadium_data(self):
        print("\nВведіть дані стадіону:")
        name = input("Назва: ")
        while not name.strip():
            print("Назва не може бути порожньою!")
            name = input("Назва: ")

        capacity = input("Місткість: ")
        while not Validators.validate_capacity(capacity):
            print("Некоректна місткість! Введіть додатнє ціле число.")
            capacity = input("Місткість: ")

        price_per_seat = input("Ціна за місце: ")
        while not Validators.validate_price(price_per_seat):
            print("Некоректна ціна! Введіть додатнє число.")
            price_per_seat = input("Ціна за місце: ")

        return name, int(capacity), float(price_per_seat)

    def manage_players(self):
        while True:
            self.display_player_menu()
            choice = input("Виберіть опцію: ")

            if choice == "1":
                self.add_player()
            elif choice == "2":
                self.show_all_players()
            elif choice == "3":
                self.show_player()
            elif choice == "4":
                self.update_player()
            elif choice == "5":
                self.delete_player()
            elif choice == "0":
                break
            else:
                print("Некоректний вибір!")

    def add_player(self):
        try:
            data = self.input_player_data()
            player = self.player_service.add_player(*data)
            print(f"Гравця {player.full_name} успішно додано!")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def show_all_players(self):
        try:
            players = self.player_service.get_all_players()
            if not players:
                print("Гравців не знайдено.")
                return

            print("\nСписок всіх гравців:")
            for player in players:
                print(player)
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def show_player(self):
        player_id = input("Введіть ID гравця: ")
        if not Validators.validate_id(player_id):
            print("Некоректний ID!")
            return

        try:
            player = self.player_service.get_player(int(player_id))
            print(f"\nІнформація про гравця:")
            print(player)
        except PlayerNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def update_player(self):
        player_id = input("Введіть ID гравця для зміни: ")
        if not Validators.validate_id(player_id):
            print("Некоректний ID!")
            return

        print("\nВведіть нові дані (залишити порожнім для збереження поточного значення):")

        updates = {}
        first_name = input("Ім'я: ")
        if first_name and Validators.validate_name(first_name):
            updates['first_name'] = first_name

        last_name = input("Прізвище: ")
        if last_name and Validators.validate_name(last_name):
            updates['last_name'] = last_name

        birth_date = input("Дата народження (РРРР-ММ-ДД): ")
        if birth_date and Validators.validate_date(birth_date):
            updates['birth_date'] = birth_date

        status = input("Статус: ")
        if status:
            updates['status'] = status

        health_status = input("Статус здоров'я: ")
        if health_status:
            updates['health_status'] = health_status

        salary = input("Зарплата: ")
        if salary and Validators.validate_salary(salary):
            updates['salary'] = float(salary)

        try:
            if updates:
                player = self.player_service.update_player(int(player_id), **updates)
                print(f"Дані гравця {player.full_name} успішно оновлено!")
            else:
                print("Немає даних для оновлення.")
        except PlayerNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def delete_player(self):
        player_id = input("Введіть ID гравця для видалення: ")
        if not Validators.validate_id(player_id):
            print("Некоректний ID!")
            return

        try:
            self.player_service.delete_player(int(player_id))
            print("Гравця успішно видалено!")
        except PlayerNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def manage_games(self):
        while True:
            self.display_game_menu()
            choice = input("Виберіть опцію: ")

            if choice == "1":
                self.add_game()
            elif choice == "2":
                self.show_all_games()
            elif choice == "3":
                self.show_game()
            elif choice == "4":
                self.update_game()
            elif choice == "5":
                self.delete_game()
            elif choice == "6":
                self.add_player_to_game()
            elif choice == "7":
                self.remove_player_from_game()
            elif choice == "8":
                self.sort_games_by_date()
            elif choice == "9":
                self.sort_games_by_result()
            elif choice == "0":
                break
            else:
                print("Некоректний вибір!")

    def add_game(self):
        try:
            data = self.input_game_data()
            game = self.game_service.add_game(*data)
            print(f"Гру проти {game.opponent_team} успішно додано!")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def show_all_games(self):
        try:
            games = self.game_service.get_all_games()
            if not games:
                print("Ігор не знайдено.")
                return

            print("\nСписок всіх ігор:")
            for game in games:
                print(game)
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def show_game(self):
        game_id = input("Введіть ID гри: ")
        if not Validators.validate_id(game_id):
            print("Некоректний ID!")
            return

        try:
            game = self.game_service.get_game(int(game_id))
            print(f"\nІнформація про гру:")
            print(game)
            if game.players:
                print("Гравці в грі:", game.players)
        except GameNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def update_game(self):
        game_id = input("Введіть ID гри для зміни: ")
        if not Validators.validate_id(game_id):
            print("Некоректний ID!")
            return

        print("\nВведіть нові дані (залишити порожнім для збереження поточного значення):")

        updates = {}
        date = input("Дата проведення (РРРР-ММ-ДД): ")
        if date and Validators.validate_date(date):
            updates['date'] = date

        location = input("Місце проведення: ")
        if location:
            updates['location'] = location

        opponent_team = input("Команда-суперник: ")
        if opponent_team:
            updates['opponent_team'] = opponent_team

        spectators = input("Кількість глядачів: ")
        if spectators and Validators.validate_spectators(spectators):
            updates['spectators'] = int(spectators)

        result = input("Результат: ")
        if result:
            updates['result'] = result

        try:
            if updates:
                game = self.game_service.update_game(int(game_id), **updates)
                print(f"Дані гри проти {game.opponent_team} успішно оновлено!")
            else:
                print("Немає даних для оновлення.")
        except GameNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def delete_game(self):
        game_id = input("Введіть ID гри для видалення: ")
        if not Validators.validate_id(game_id):
            print("Некоректний ID!")
            return

        try:
            self.game_service.delete_game(int(game_id))
            print("Гру успішно видалено!")
        except GameNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def add_player_to_game(self):
        game_id = input("Введіть ID гри: ")
        player_id = input("Введіть ID гравця: ")

        if not Validators.validate_id(game_id) or not Validators.validate_id(player_id):
            print("Некоректний ID!")
            return

        try:
            self.game_service.add_player_to_game(int(game_id), int(player_id))
            print("Гравця успішно додано до гри!")
        except (GameNotFoundException, PlayerAlreadyInGameException) as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def remove_player_from_game(self):
        game_id = input("Введіть ID гри: ")
        player_id = input("Введіть ID гравця: ")

        if not Validators.validate_id(game_id) or not Validators.validate_id(player_id):
            print("Некоректний ID!")
            return

        try:
            self.game_service.remove_player_from_game(int(game_id), int(player_id))
            print("Гравця успішно видалено з гри!")
        except GameNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def sort_games_by_date(self):
        try:
            sorted_games = self.game_service.sort_games_by_date()
            print("\nІгри відсортовані за датою:")
            for game in sorted_games:
                print(game)
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def sort_games_by_result(self):
        try:
            categorized = self.game_service.get_games_by_result()
            for category, games in categorized.items():
                print(f"\n{category}:")
                for game in games:
                    print(f"  {game}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def manage_stadiums(self):
        while True:
            self.display_stadium_menu()
            choice = input("Виберіть опцію: ")

            if choice == "1":
                self.add_stadium()
            elif choice == "2":
                self.show_all_stadiums()
            elif choice == "3":
                self.show_stadium()
            elif choice == "4":
                self.update_stadium()
            elif choice == "5":
                self.delete_stadium()
            elif choice == "0":
                break
            else:
                print("Некоректний вибір!")

    def add_stadium(self):
        try:
            data = self.input_stadium_data()
            stadium = self.stadium_service.add_stadium(*data)
            print(f"Стадіон {stadium.name} успішно додано!")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def show_all_stadiums(self):
        try:
            stadiums = self.stadium_service.get_all_stadiums()
            if not stadiums:
                print("Стадіонів не знайдено.")
                return

            print("\nСписок всіх стадіонів:")
            for stadium in stadiums:
                print(stadium)
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def show_stadium(self):
        stadium_id = input("Введіть ID стадіону: ")
        if not Validators.validate_id(stadium_id):
            print("Некоректний ID!")
            return

        try:
            stadium = self.stadium_service.get_stadium(int(stadium_id))
            print(f"\nІнформація про стадіон:")
            print(stadium)
            if stadium.scheduled_games:
                print("Заплановані ігри:", stadium.scheduled_games)
        except StadiumNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def update_stadium(self):
        stadium_id = input("Введіть ID стадіону для зміни: ")
        if not Validators.validate_id(stadium_id):
            print("Некоректний ID!")
            return

        print("\nВведіть нові дані (залишити порожнім для збереження поточного значення):")

        updates = {}
        name = input("Назва: ")
        if name:
            updates['name'] = name

        capacity = input("Місткість: ")
        if capacity and Validators.validate_capacity(capacity):
            updates['capacity'] = int(capacity)

        price_per_seat = input("Ціна за місце: ")
        if price_per_seat and Validators.validate_price(price_per_seat):
            updates['price_per_seat'] = float(price_per_seat)

        try:
            if updates:
                stadium = self.stadium_service.update_stadium(int(stadium_id), **updates)
                print(f"Дані стадіону {stadium.name} успішно оновлено!")
            else:
                print("Немає даних для оновлення.")
        except StadiumNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def delete_stadium(self):
        stadium_id = input("Введіть ID стадіону для видалення: ")
        if not Validators.validate_id(stadium_id):
            print("Некоректний ID!")
            return

        try:
            self.stadium_service.delete_stadium(int(stadium_id))
            print("Стадіон успішно видалено!")
        except StadiumNotFoundException as e:
            print(f"Помилка: {str(e)}")
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def search_data(self):
        while True:
            self.display_search_menu()
            choice = input("Виберіть опцію: ")

            if choice == "1":
                self.search_players()
            elif choice == "2":
                self.search_games()
            elif choice == "3":
                self.search_stadiums()
            elif choice == "0":
                break
            else:
                print("Некоректний вибір!")

    def search_players(self):
        search_term = input("Введіть ім'я або прізвище для пошуку: ")
        if not search_term.strip():
            print("Пошуковий запит не може бути порожнім!")
            return

        try:
            players = self.player_service.search_players(search_term)
            if not players:
                print("Гравців не знайдено.")
                return

            print(f"\nРезультати пошуку для '{search_term}':")
            for player in players:
                print(player)
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def search_games(self):
        date = input("Введіть дату для пошуку (залишити порожнім для пропуску): ")
        opponent_team = input("Введіть команду-суперника для пошуку (залишити порожнім для пропуску): ")

        if not date and not opponent_team:
            print("Введіть хоча б один критерій пошуку!")
            return

        try:
            games = self.game_service.search_games(date, opponent_team)
            if not games:
                print("Ігор не знайдено.")
                return

            print(f"\nРезультати пошуку:")
            for game in games:
                print(game)
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def search_stadiums(self):
        name = input("Введіть назву стадіону для пошуку: ")
        if not name.strip():
            print("Пошуковий запит не може бути порожнім!")
            return

        try:
            stadiums = self.stadium_service.search_stadiums(name)
            if not stadiums:
                print("Стадіонів не знайдено.")
                return

            print(f"\nРезультати пошуку для '{name}':")
            for stadium in stadiums:
                print(stadium)
        except Exception as e:
            print(f"Помилка: {str(e)}")

    def run(self):
        while True:
            self.clear_screen()
            self.display_menu()
            choice = input("Виберіть опцію: ")

            if choice == "1":
                self.manage_players()
            elif choice == "2":
                self.manage_games()
            elif choice == "3":
                self.manage_stadiums()
            elif choice == "4":
                self.search_data()
            elif choice == "0":
                print("Дякуємо за використання системи!")
                break
            else:
                print("Некоректний вибір! Спробуйте ще раз.")

            input("\nНатисніть Enter для продовження...")