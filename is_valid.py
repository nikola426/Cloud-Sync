from configparser import ConfigParser

from loguru import logger

from sys import exit
from typing import Union, Tuple

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


# Функция валидации конфигурационного файла.
@logger.catch
def is_valid_config(config_file_path: str, service_name: str, param_names: Tuple):

    # Проверяем наличие конфигурационного файла. В случае его отсутствия завершаем программу с соответствующим
    # сообщением
    if not os.path.isfile(config_file_path):
        logger.error(
            f'Отсутствует конфигурационный файл {config_file_path}.\n'
            'Выполнение программы завершено')
        exit(0)

    # Создаём объект парсера конфигурационного файла и читаем этот файл
    config = ConfigParser()
    config.read(config_file_path)

    # Проверяем наличие блока входных данных конкретного сервиса. В случае его отсутствия завершаем программу с
    # соответствующим сообщением
    try:
        config = config[service_name]
    except KeyError:
        logger.error(
            f'В конфигурационном файле {config_file_path} отсутствует блок входных данных сервиса {service_name}\n'
            'Выполнение программы завершено')
        exit(0)

    # Проходим по списку имён входных параметров и проверяем их наличие в блоке входных данных. В случае успеха
    # добавляем значение параметра в список, иначе - завершаем программу с соответствующим сообщением.
    params_list = []
    for param_name in param_names:
        if config.get(param_name, '') == '':
            logger.error(f'В конфигурационном файле {config_file_path} отсутствует параметр {param_name}.\n'
                         'Выполнение программы завершено')
            exit(0)
        else:
            params_list.append(config[param_name])

    return params_list


# Функция, логирующая невалидность токена доступа и завершающая программу
def not_valid_token() -> None:
    logger.error('Отсутствует валидный токен доступа.\nВыполнение программы завершено')
    exit(0)


# Функция, логирующая невалидность пути к удалённой папке и завершающая программу
def not_valid_cloud_path() -> None:
    logger.error('Запрашиваемая удалённая директория не существует.\nВыполнение программы завершено')
    exit(0)
