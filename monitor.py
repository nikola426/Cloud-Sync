from loguru import logger

import os
import hashlib
from sys import exit
from typing import Dict, Union

from is_valid import is_valid_path


# Функция подсчёта md5-хеша файла
def calculate_md5(sync_folder: str, file_name: str) -> str:

    # Создаем объект md5
    md5_hash = hashlib.md5()

    # Объединяем путь к папке с именем файла
    local_file_path = os.path.join(sync_folder, file_name)

    # Открываем файл в бинарном режиме
    with open(local_file_path, "rb") as file:

        # Читаем файл по частям для экономии памяти
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)

    # Возвращаем шестнадцатеричное представление хеша
    return md5_hash.hexdigest()


# Функция сканирования локальной синхронизируемой папки
def scan(sync_folder: str) -> Union[Dict, None]:
    try:
        # Проверяем путь к локальной папке на валидность. В случае невалидного пути программа завершается с
        # соответствующим сообщением
        is_valid_path(sync_folder)

        # Формируем словарь из имён файлов из локальной папки и их md5-хешей: {<имя_файла>: <md5-хеш файла>}
        files_dict = {file_name: calculate_md5(sync_folder, file_name) for file_name in os.listdir(sync_folder)}
    except Exception as e:
        logger.error(f'При попытке отсканировать локальную папку возникло исключение: {e}')
        exit(0)
    else:
        logger.info('Синхронизируемая папка успешно отсканирована.')
        return files_dict
