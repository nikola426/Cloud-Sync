from loguru import logger

import os
import hashlib


def calculate_md5(sync_folder, file_name):
    # Создаем объект MD5
    md5_hash = hashlib.md5()

    #Объединяем путь к папке с именем файла
    local_file_path = os.path.join(sync_folder, file_name)

    # Открываем файл в бинарном режиме
    with open(local_file_path, "rb") as file:

        # Читаем файл по частям для экономии памяти
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)

    # Возвращаем шестнадцатеричное представление хеша
    return md5_hash.hexdigest()


def scan(sync_folder):
    try:
        files_dict = {file_name: calculate_md5(sync_folder, file_name) for file_name in os.listdir(sync_folder)}
    except Exception as e:
        logger.error(f'При попытке отсканировать локальную папку возникло исключение: {e}')
    else:
        logger.info('Синхронизируемая папка успешно отсканирована.')
        return files_dict
