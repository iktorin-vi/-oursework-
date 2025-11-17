import re
from datetime import datetime

class Validators:
    @staticmethod
    def validate_name(name: str) -> bool:
        return bool(name and name.strip() and len(name) >= 2)

    @staticmethod
    def validate_date(date_string: str) -> bool:
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_salary(salary: str) -> bool:
        try:
            value = float(salary)
            return value >= 0
        except ValueError:
            return False

    @staticmethod
    def validate_capacity(capacity: str) -> bool:
        try:
            value = int(capacity)
            return value > 0
        except ValueError:
            return False

    @staticmethod
    def validate_price(price: str) -> bool:
        try:
            value = float(price)
            return value >= 0
        except ValueError:
            return False

    @staticmethod
    def validate_spectators(spectators: str) -> bool:
        try:
            value = int(spectators)
            return value >= 0
        except ValueError:
            return False

    @staticmethod
    def validate_id(item_id: str) -> bool:
        try:
            value = int(item_id)
            return value > 0
        except ValueError:
            return False