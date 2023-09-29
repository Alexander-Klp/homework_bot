import os
import logging
import requests
import telegram
import time
from exceptions import (
    NoTokenTelegramException,
    NoTokenPracticumException,
    NoTelegramIdException,
    NotStatus200Exception,
)

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.DEBUG,
    filename='main.log',
)


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
    if TELEGRAM_TOKEN is None or TELEGRAM_TOKEN == '':
        raise NoTokenTelegramException('TELEGRAM_TOKEN')
    if PRACTICUM_TOKEN is None or PRACTICUM_TOKEN == '':
        raise NoTokenPracticumException('PRACTICUM_TOKEN')
    if TELEGRAM_CHAT_ID is None or TELEGRAM_CHAT_ID == '':
        raise NoTelegramIdException('TELEGRAM_CHAT_ID')


def get_api_answer(timestamp):
    """Функция делает запрос к единственному эндпоинту API-сервиса."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except Exception as error:
        logging.error(f'''Ошибка при запросе к API: '{error}' ''')
    if response.status_code != 200:
        raise NotStatus200Exception('Код ответа API: не ОК')
    response = response.json()
    return response


def check_response(response):
    """Функция проверяет ответ API на соответствие."""
    if 'homeworks' not in response:
        raise TypeError('ключа "homeworks" нет')
    if not isinstance(response['homeworks'], list):
        raise TypeError('"homeworks"не являются списком')
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
    verdict = HOMEWORK_VERDICTS[status]
    return f'Изменился статус проверки работы "{homework_name}".{verdict}'


def send_message(bot, message):
    """Этот модуль содержит классы и функции для работы с чем-то."""
    bot.send_message(TELEGRAM_CHAT_ID, message)
    logging.debug(f'''Сообщение отправлено '{message}' ''')


def main():
    """Основная логика работы программы."""
    minus_30_days = 30 * 24 * 60 * 60
    timestamp = int(time.time() - minus_30_days)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    prev_message = None
    Run = True
    try:
        check_tokens()
    except Exception as error:
        logging.critical(
            f'''Отсутствует обязательная переменная окружения: '{error}'.
Программа принудительно остановлена.'''
        )
        Run = False
    while Run:
        try:
            response = get_api_answer(timestamp)
            homework = check_response(response)
            message = parse_status(homework)
            if message != prev_message:
                send_message(bot, message)
                prev_message = message
        except Exception as error:
            logging.error(f'''Сбой в работе программы: '{error}' ''')
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
