from loguru import logger

from time import sleep
from typing import Dict, Union, Type, Tuple

from interfaces import YandexSyncInterface
import monitor
import config


def revise(local_dict: Dict[str: str], cloud_dict: Dict[str: str], inter_inst: Union[YandexSyncInterface]) -> None:
    for file_name in cloud_dict.keys():
        if file_name not in local_dict:
            inter_inst.delete(file_name)

    for file_name in local_dict.keys():
        if file_name not in cloud_dict:
            inter_inst.load(file_name)
        elif local_dict[file_name] != cloud_dict[file_name]:
            inter_inst.reload(file_name)


def infinite(sync_folder: str, inter_inst: Union[YandexSyncInterface], period: int) -> None:
    while True:
        local_files_dict = monitor.scan(sync_folder)
        cloud_files_dict = inter_inst.get_info()
        if (cloud_files_dict is not None) and (local_files_dict is not None):
            revise(local_files_dict, cloud_files_dict, inter_inst)
        sleep(period)


def data_preparation(sync_folder: str, period: str, log_file_path: str, interface: Type[Union[YandexSyncInterface]]) -> Tuple[
    str, Union[YandexSyncInterface], int
]:
    logger.add(log_file_path, rotation='1 MB', compression='zip')
    logger.info(f'Программа начала работу. Синхронизируемая папка: {sync_folder}')
    inter_inst = interface()
    period = int(period)

    return sync_folder, inter_inst, period

@logger.catch
def main(module: str) -> None:
    if module == 'Yandex Disk':
        infinite(*data_preparation(config.YANDEX_SYNC_FOLDER,
                                   config.YANDEX_PERIOD,
                                   config.YA_LOG_FILE_PATH,
                                   YandexSyncInterface))

main('Yandex Disk')
