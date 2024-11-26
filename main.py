from loguru import logger

from time import sleep
from typing import Dict, Union, Type, Tuple

from interfaces import YandexSyncInterface
import monitor
import is_valid


# Функция сверки файлов локальной синхронизируемой папки и удалённой.
# Входные словари имеют вид: {<имя_файла>: <md5-хеш файла>}
def revise(local_dict: Dict, cloud_dict: Dict, inter_inst: Union[YandexSyncInterface]) -> None:

    # Проходимся циклом по "списку" файлов из удалённой папки и проверяем, присутствует ли имя файла из удалённой
    # папки среди имён в локальной. Если нет, то удаляем файл.
    for file_name in cloud_dict.keys():
        if file_name not in local_dict:
            inter_inst.delete(file_name)

    # Проходимся циклом по "списку" файлов в локальной папке и проверяем, присутствует ли имя файла из локальной папки
    # в удалённой. Если нет, то загружаем файл в удалённую папку.
    for file_name in local_dict.keys():
        if file_name not in cloud_dict:
            inter_inst.load(file_name)

        # Иначе проверяем, сходятся ли md5-хеши файлов. Если нет, то переписываем файл в удалённой папке.
        elif local_dict[file_name] != cloud_dict[file_name]:
            inter_inst.reload(file_name)


# функция бесконечного мониторинга
def infinite(sync_folder: str, inter_inst: Union[YandexSyncInterface], period: int) -> None:
    while True:
        # Сканируем локальную папку и создаём словарь вида: {<имя_файла>: <md5-хеш файла>}
        # Функция может вернуть None
        local_files_dict = monitor.scan(sync_folder)

        # Сканируем удалённую папку и создаём такой же словарь
        # Функция может вернуть None
        cloud_files_dict = inter_inst.get_info()

        #После проверки на None передаём эти словари в качестве аргументов в функцию сверки
        if (cloud_files_dict is not None) and (local_files_dict is not None):
            revise(local_files_dict, cloud_files_dict, inter_inst)

        #Ждём отведённое время
        sleep(period)


# Функция подготовки перед началом бесконечного мониторинга
def data_preparation(interface: Type[Union[YandexSyncInterface]], sync_folder: str, period: str, log_file_path: str,
                     token: str, cloud_path: str) -> Tuple[str, Union[YandexSyncInterface], int]:

    # Проверяем на валидность путь к лог-файлу. В случае невалидного пути программа завершится с соответствующим
    # сообщением
    is_valid.is_valid_log_file_path(log_file_path)

    # Создаём лог-файл с максимальным размером в 1 МБ и с компрессией в zip при заполнении.
    logger.add(log_file_path, rotation='1 MB', compression='zip')

    # Сигнализируем о начале работы программы.
    # Все логи автоматически записываются в лог-файл.
    logger.info(f'Программа начала работу. Синхронизируемая папка: {sync_folder}')

    # Создаём объект интерфейса взаимодействия с API облачного сервиса
    inter_inst = interface(token, cloud_path, sync_folder)

    # Проверяем период синхронизации на валидность. В случае невалидного периода программа завершится с соответствующим
    # сообщением
    period = is_valid.is_valid_period(period)

    return sync_folder, inter_inst, period


# Основная функция, в которой происходит выбор, подготовка к запуску и, непосредственно, запуск нужного сервиса
@logger.catch
def main(service_name: str) -> None:

    # Запускаем нужный сервис. Передаём входные данные на предварительную подготовку в функцию data_preparation.
    # Затем функция бесконечного мониторинга infinite принимает от неё новые входные данные для начала работы.
    if service_name == 'YANDEX_DISK':
        param_names = ('YANDEX_SYNC_FOLDER',
                       'YANDEX_PERIOD',
                       'YA_LOG_FILE_PATH',
                       'YANDEX_TOKEN',
                       'YANDEX_DISK_PATH')

        # Передаём адрес конфигурационного файла, имя сервиса и список имён входных параметров в функцию проверки
        # валидности конфигурационного файла. В случае валидности файла она возвращает список значений входных
        # параметров, иначе программа завершается с соответствующим сообщением.
        config_data = is_valid.is_valid_config('config.ini', service_name, param_names)

        # Передаём интерфейс и распакованный список данных из конфигурационного файла в функцию подготовки перед
        # бесконечным мониторингом. Затем готовые данные из этой функции распаковываем и передаём в функцию бесконечного
        # мониторинга
        infinite(*data_preparation(YandexSyncInterface, *config_data))

if __name__ == "__main__":
    main('YANDEX_DISK')
