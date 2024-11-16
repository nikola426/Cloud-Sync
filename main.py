from loguru import logger

import os
from time import sleep

from interface import YandexSyncInterface
import monitor
import config


def revise(local_dict, cloud_dict, inter):
    for file_name in local_dict.keys():
        if md5 := cloud_dict.get(file_name) is None:
            inter.load(file_name)
        elif md5 != local_dict(file_name):
            inter.reload(file_name)

    for file_name in cloud_dict.keys():
        if local_dict.get(file_name) is None:
            inter.delete(file_name)


@logger.catch
def main(module):
    if module == 'Yandex Disk':
        logger.add(config.YA_LOG_FILE_PATH, rotation='1 MB', compression='zip')
        logger.info('Программа начала работу.')
        os.chdir(config.YANDEX_SYNC_FOLDER)
        ya_inter = YandexSyncInterface()
        period = int(config.YANDEX_PERIOD)

        while True:
            local_files_dict = monitor.scan()
            cloud_files_dict = ya_inter.get_info()
            if cloud_files_dict is not None:
                revise(local_files_dict, cloud_files_dict, ya_inter)
            sleep(period)
            continue

main('Yandex Disk')
