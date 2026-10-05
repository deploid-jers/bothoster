class ServiceException(Exception):
    """Базовое исключение для ошибок бизнес-логики"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundException(ServiceException):
    """Ошибка: не наден ресурс"""
    pass

class InvalidDataForLoginException(ServiceException):
    """Неправильные логин или пароль"""
    pass

class UserAlreadyExistsException(ServiceException):
    """Пользователь с таким логином или email уже существует"""
    pass

class UnauthorizedException(ServiceException):
    """Ошибка при неправильных данных"""
    pass

class DatabaseException(ServiceException):
    """Ошибка при работе с базод данных"""
    pass

class ServerErrorException(ServiceException):
    """Ошибка в работе сервера"""
    pass

class ServerBadGetwayException(ServiceException):
    """Ошибка при взаимодейсвии с другими сервисами"""

# ==== Rate limit

class RateLimitExceeded(ServiceException):
    """Лимит запросов"""
    def __init__(self, message: str = "Too Many Requests!", retry_after: int = 0):
        self.message = message
        self.retry_after = retry_after

        super().__init__(self.message)

class RateLimiterUnavailable(ServiceException):
    """Ошибка при работе rate limit"""
    pass