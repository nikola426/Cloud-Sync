from loguru import logger

from sys import exit
from typing import Union

import os


# Функция проверки валидности пути к локальной папке
def is_valid_path(path: str) -> None:
    if not os.path.isdir(path):
        logger.error('Указанная локальная директория не существует.\nВыполнение программы завершено')
        exit(0)


# Функция проверки валидности периода синхронизации
def is_valid_period(period: str) -> Union[int, None]:
    try:
        period = int(period)
        if period < 1:
            logger.error('Период синхронизации меньше 1. Укажите пожалуйста период больше либо равно 1.\n'
                         'Выполнение программы завершено')
            exit(0)
        return period
    except ValueError:
        logger.error('Период синхронизации не может быть дробным числом. '
                     'Укажите пожалуйста верное значение (целое число больше 0).\n'
                     'Выполнение программы завершено')
        exit(0)


# Функция проверки валидности пути к лог-файлу
def is_valid_log_file_path(log_file_path: str) -> None:
    try:
        with open(log_file_path, 'a'):
            pass
    except FileNotFoundError:
        logger.error('Указанный путь для логирования не найден.\nВыполнение программы завершено')
        exit(0)
    except PermissionError:
        logger.error('Нет прав на запись лога в указанную директорию.\nВыполнение программы завершено')
        exit(0)
    except IsADirectoryError:
        logger.error('Указанный для логирования путь является директорией, а не файлом.\nВыполнение программы завершено')
        exit(0)
    except OSError as e:
        logger.error(f'При попытке создания файла лога возникла ошибка операционной системы: {e}\n'
                     f'Выполнение программы завершено')
        exit(0)


# Функция, логирующая невалидность токена доступа и завершающая программу
def not_valid_token() -> None:
    logger.error('Отсутствует валидный токен доступа.\nВыполнение программы завершено')
    exit(0)


# Функция, логирующая невалидность пути к удалённой папке и завершающая программу
def not_valid_cloud_path() -> None:
    logger.error('Запрашиваемая удалённая директория не существует.\nВыполнение программы завершено')
    exit(0)

