import config
import yandex_api

from typing import Union, Dict


class YandexSyncInterface:
    def __init__(self):
        self.__token: str = config.YANDEX_TOKEN
        self.__sync_folder: str = config.YANDEX_SYNC_FOLDER

    def get_info(self) -> Union[Dict[str: str], None]:
        return yandex_api.scan_cloud(self.__token)

    def load(self, file_name: str) -> None:
        upload_url = yandex_api.get_upload_link(file_name, self.__token)
        return yandex_api.upload_file(self.__sync_folder, file_name, upload_url)

    def reload(self, file_name: str) -> None:
        return self.load(file_name)

    def delete(self, file_name: str) -> None:
        return yandex_api.delete_files(file_name, self.__token)