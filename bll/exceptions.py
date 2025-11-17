class BusinessLogicException(Exception):
    """Базовий клас для винятків бізнес-логіки"""
    pass

class PlayerNotFoundException(BusinessLogicException):
    """Виняток для ситуації, коли гравець не знайдений"""
    pass

class GameNotFoundException(BusinessLogicException):
    """Виняток для ситуації, коли гра не знайдена"""
    pass

class StadiumNotFoundException(BusinessLogicException):
    """Виняток для ситуації, коли стадіон не знайдений"""
    pass

class InvalidGameDataException(BusinessLogicException):
    """Виняток для некоректних даних гри"""
    pass

class PlayerAlreadyInGameException(BusinessLogicException):
    """Виняток, коли гравець вже доданий до гри"""
    pass