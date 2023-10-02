import json
import logging
import logging.config
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv
from telegram.error import TelegramError

from exceptions import (
    NoJsonException,
    NoTelegramIdException,
    NoTokenPracticumException,
    NoTokenTelegramException,
    NotStatus200Exception,
    SendMessageException,
    HTTPErrorException,
    TimeoutException,
    ConnectionErrorException,
    ApiRequestException,

)


load_dotenv()

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Функция проверяет доступность переменных окружения."""
    if not TELEGRAM_TOKEN:
        raise NoTokenTelegramException('TELEGRAM_TOKEN')
    if not PRACTICUM_TOKEN:
        raise NoTokenPracticumException('PRACTICUM_TOKEN')
    if not TELEGRAM_CHAT_ID:
        raise NoTelegramIdException('TELEGRAM_CHAT_ID')


def get_api_answer(timestamp):
    """Функция делает запрос к единственному эндпоинту API-сервиса."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except requests.exceptions.HTTPError as http_error:
        raise HTTPErrorException(
            f'''Ошибка HTTP: '{http_error}' '''
        )
    except requests.exceptions.Timeout as timeout_error:
        raise TimeoutException(
            f'''Время ожидания запроса истекло: '{timeout_error}' '''
        )
    except requests.exceptions.ConnectionError as connection_error:
        raise ConnectionErrorException(
            f'''Ошибка соединения: '{connection_error}' '''
        )
    except requests.exceptions.RequestException as error:
        raise ApiRequestException(
            f'''Произошла ошибка при выполнении запроса: '{error}' '''
        )
    if response.status_code != HTTPStatus.OK:
        raise NotStatus200Exception('Код ответа API: не ОК')
    try:
        response = response.json()
    except json.decoder.JSONDecodeError:
        raise NoJsonException('Не является JSON')
    return response


def check_response(response):
    """Функция проверяет ответ API на соответствие."""
    if 'current_date' not in response:
        raise TypeError('ключа "current_date" нет')
    if 'homeworks' not in response:
        raise TypeError('ключа "homeworks" нет')
    if not isinstance(response['homeworks'], list):
        raise TypeError('"homeworks"не являются списком')
    if not response['homeworks']:
        raise TypeError('в списке домашки нет, проверь время')
    return response['homeworks'][0]


def parse_status(homework):
    """
    Функция извлекает из.
    информации о конкретной домашней работе статус этой работы.
    """
    if 'homework_name' not in homework:
        raise TypeError('Нет названия домашки')
    if 'status' not in homework or homework['status'] == 'unknown':
        raise TypeError('Нет статуса или статус неизвестен')
    homework_name = homework['homework_name']
    status = homework['status']
    try:
        verdict = HOMEWORK_VERDICTS[status]
    except KeyError:
        verdict = 'Неизвестный статус'
    return f'Изменился статус проверки работы "{homework_name}".{verdict}'


def send_message(bot, message):
    """Отправка сообщений в телеграмм."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except TelegramError:
        raise SendMessageException('Ошибка при отправке сообщения')
    logger.debug(f'''Сообщение отправлено '{message}' ''')


def main():
    """Основная логика работы программы."""
    minus_30_days = 30 * 24 * 60 * 60
    timestamp = int(time.time() - minus_30_days)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    prev_message = None
    try:
        check_tokens()
    except Exception as error:
        logger.critical(
            f'''Отсутствует обязательная переменная окружения: '{error}'.
Программа принудительно остановлена.'''
        )
        sys.exit(1)  # Прерываем выполнение программы
    while True:
        try:
            response = get_api_answer(timestamp)
            homework = check_response(response)
            current_date = response['current_date']
            timestamp = int(current_date) - minus_30_days
            message = parse_status(homework)
            if message != prev_message:
                send_message(bot, message)
                prev_message = message
        except Exception as error:
            logger.error(f'''Сбой в работе программы: '{error}' ''')
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
