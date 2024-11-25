import yandex_api

from typing import Union, Dict


class YandexSyncInterface:
    """
    Класс, являющийся интерфейсом взаимодействия с API Яндекс Диска.

    Args:
        token (str): Токен доступа к Яндекс Диску
        disk_path (str): Путь к синхронизируемой папке в Яндекс Диске
        sync_folder (str): Путь к локальной синхронизируемой папке
    """
    def __init__(self, token, disk_path, sync_folder):
        self.__token: str = token
        self.__sync_folder: str = sync_folder
        self.__disk_path: str = disk_path

    def get_info(self) -> Union[Dict, None]:
        """
        Метод получения списка файлов из удалённой папки.

        :return: Список файлов в виде словаря, в котором ключи - это имена файлов, а их значения - это их md5-хеши
        :rtype: dict
        """
        return yandex_api.scan_cloud(self.__token, self.__disk_path)

    def load(self, file_name: str) -> None:
        """
        Метод получения ссылки на загрузку файла, а также самой загрузки.

        :param file_name: Имя загружаемого файла
        :type file_name: str
        """
        if upload_url := yandex_api.get_upload_link(file_name, self.__token, self.__disk_path):
            yandex_api.upload_file(self.__sync_folder, file_name, upload_url)

    def reload(self, file_name: str) -> None:
        """
        Метод перезаписи файла в удалённой папке. Вызывает метод загрузки, так как логика загрузки предусматривает перезапись файла.

        :param file_name: Имя загружаемого файла
        :type file_name: str
        """
        self.load(file_name)

    def delete(self, file_name: str) -> None:
        """
        Метод удаления файла из удалённой папки.

        :param file_name: Имя удаляемого файла
        :type file_name: str
        """
        yandex_api.delete_files(file_name, self.__token, self.__disk_path)