from loguru import logger

from sys import exit

import os


def is_valid_path(path: str) -> None:
    if not os.path.isdir(path):
        logger.error(f'Директория {path} не существует. Выполнение программы завершено')
        exit(0)

def not_valid_token():
    logger.error(f'Отсутствует валидный токен доступа. Выполнение программы завершено')
    exit(0)