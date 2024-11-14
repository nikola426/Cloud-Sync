from loguru import logger

import os
import hashlib

from config import SYNC_FOLDER


#os.chdir(SYNC_FOLDER)

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


@logger.catch
def scan():
    data_list = []
    for file_name in os.listdir():
        data_dict = {}
        data_dict['name'] = file_name
        data_dict['md5'] = calculate_md5(file_name)
        data_list.append(data_dict)

    return data_list

print(scan())