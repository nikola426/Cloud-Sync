import yandex_api

from typing import Union, Dict


class YandexSyncInterface:
    def __init__(self, token, disk_path, sync_folder):
        self.__token: str = token
        self.__sync_folder: str = sync_folder
        self.__disk_path: str = disk_path

    def get_info(self) -> Union[Dict, None]:
        return yandex_api.scan_cloud(self.__token, self.__disk_path)

    def load(self, file_name: str) -> None:
        upload_url = yandex_api.get_upload_link(file_name, self.__token, self.__disk_path)
        return yandex_api.upload_file(self.__sync_folder, file_name, upload_url)

    def reload(self, file_name: str) -> None:
        return self.load(file_name)

    def delete(self, file_name: str) -> None:
        return yandex_api.delete_files(file_name, self.__token, self.__disk_path)