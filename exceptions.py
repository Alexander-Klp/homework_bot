
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
