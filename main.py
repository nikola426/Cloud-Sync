from loguru import logger

from time import sleep
from typing import Dict, Union, Type, Tuple
from configparser import ConfigParser

from interfaces import YandexSyncInterface
import monitor
import is_valid


# Функция сверки файлов локальной синхронизируемой папки и удалённой. Представляет собой сверку словарей с именами
# файлов в качестве ключей и md5-хэшей этих файлов в качестве значений.
def revise(local_dict: Dict, cloud_dict: Dict, inter_inst: Union[YandexSyncInterface]) -> None:
    for file_name in cloud_dict.keys():
        if file_name not in local_dict:
            inter_inst.delete(file_name)

    for file_name in local_dict.keys():
        if file_name not in cloud_dict:
            inter_inst.load(file_name)
        elif local_dict[file_name] != cloud_dict[file_name]:
            inter_inst.reload(file_name)


# функция
def infinite(sync_folder: str, inter_inst: Union[YandexSyncInterface], period: int) -> None:
    while True:
        local_files_dict = monitor.scan(sync_folder)
        cloud_files_dict = inter_inst.get_info()
        if (cloud_files_dict is not None) and (local_files_dict is not None):
            revise(local_files_dict, cloud_files_dict, inter_inst)
        sleep(period)


def data_preparation(sync_folder: str, period: str, log_file_path: str, token: str, cloud_path: str,
                     interface: Type[Union[YandexSyncInterface]]) -> Tuple[str, Union[YandexSyncInterface], int]:
    is_valid.is_valid_log_file_path(log_file_path)
    logger.add(log_file_path, rotation='1 MB', compression='zip')
    logger.info(f'Программа начала работу. Синхронизируемая папка: {sync_folder}')
    inter_inst = interface(token, cloud_path, sync_folder)
    period = is_valid.is_valid_period(period)

    return sync_folder, inter_inst, period

@logger.catch
def main(module: str) -> None:
    config = ConfigParser()
    config.read('config.ini')
    config_module = config[module]
    if module == 'YANDEX_DISK':
        infinite(*data_preparation(config_module['YANDEX_SYNC_FOLDER'],
                                   config_module['YANDEX_PERIOD'],
                                   config_module['YA_LOG_FILE_PATH'],
                                   config_module['YANDEX_TOKEN'],
                                   config_module['YANDEX_DISK_PATH'],
                                   YandexSyncInterface))

if __name__ == "__main__":
    main('YANDEX_DISK')
