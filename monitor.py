from loguru import logger

import os
import hashlib


def calculate_md5(filepath):
    # Создаем объект MD5
    md5_hash = hashlib.md5()

    # Открываем файл в бинарном режиме
    with open(filepath, "rb") as file:

        # Читаем файл по частям для экономии памяти
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)

    # Возвращаем шестнадцатеричное представление хеша
    return md5_hash.hexdigest()


def scan():
    try:
        files_dict = {file_name: calculate_md5(file_name) for file_name in os.listdir()}
    except Exception as e:
        logger.error(f'При попытке отсканировать локальную папку возникло исключение: {e}')
    else:
        logger.info('Локальная папка успешно отсканирована.')
        return files_dict
