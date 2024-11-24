from loguru import logger

from sys import exit

import os


def is_valid_path(path: str) -> None:
    if not os.path.isdir(path):
        logger.error(f'Директория {path} не существует.')
        exit(0)
