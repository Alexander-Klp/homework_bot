
class NoTokenTelegramException(Exception):
    """Нет токена телеграм."""

    pass


class NoTokenPracticumException(Exception):
    """Нет токена практикума."""

    pass


class NoTelegramIdException(Exception):
    """Нет ID чата телеграмм."""

    pass


class NotStatus200Exception(Exception):
    """Статус не ОК."""

    pass


class SendMessageException(Exception):
    """SendMessageException."""

    pass


class NoJsonException(Exception):
    """не является JSON."""

    pass


class HTTPErrorException(Exception):
    """Ошибка HTTP."""

    pass


class TimeoutException(Exception):
    """Время ожидания запроса истекло."""

    pass


class ConnectionErrorException(Exception):
    """Ошибка соединения."""

    pass


class ApiRequestException(Exception):
    """Произошла ошибка при выполнении запроса."""

    pass
