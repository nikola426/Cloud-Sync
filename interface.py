import importlib

import config


class SyncInterface:
    def __init__(self, module_name):
        self.__api_module = importlib.import_module(module_name)
        if module_name == 'yandex_api':
            self.__token = config.YANDEX_TOKEN
            self.__sync_folder = config.YANDEX_SYNC_FOLDER

    def scan(self):
        self.__api_module.scan_cloud(self.__token)

    def upload(self, file_name):
        self.__api_module.upload_files(file_name, self.__token, self.__sync_folder)

    def delete(self, file_name):
        self.__api_module.delete_files(file_name, self.__token)