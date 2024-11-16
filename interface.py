import config
import yandex_api


class YandexSyncInterface:
    def __init__(self):
        self.__token = config.YANDEX_TOKEN
        self.__sync_folder = config.YANDEX_SYNC_FOLDER

    def get_info(self):
        yandex_api.scan_cloud(self.__token)

    def load(self, file_name):
        yandex_api.upload_files(file_name, self.__token, self.__sync_folder)

    def reload(self, file_name):
        yandex_api.upload_files(file_name, self.__token, self.__sync_folder)

    def delete(self, file_name):
        yandex_api.delete_files(file_name, self.__token)