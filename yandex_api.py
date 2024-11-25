from loguru import logger
import requests

import os
import json
from typing import Dict, Union

import is_valid


# Функция оформления заголовка HTTP-запроса
def headers(token: str) -> Dict:
    head = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    return head


# Функция извлечения нужных данных из тела ответа от сервера
def resp_filter(resp: requests.Response) -> Union[Dict, None]:
    # Формируем словарь из имён файлов из удалённой папки и их md5-хешей: {<имя_файла>: <md5-хеш файла>}
    try:
        cloud_files_data = {file_data['name']: file_data['md5'] for file_data in resp['_embedded']['items']}
    except Exception as e:
        logger.error(f'При попытке извлечь данные из ответа сервера возникло исключение: {e}')
    else:
        return cloud_files_data


# Функция сканирования удалённой папки
def scan_cloud(token: str, disk_path: str) -> Union[Dict, None]:
    # Пытаемся получить метаданные файлов в удалённой папке и обрабатываем ошибки и исключения
    try:
        response = requests.get(f'https://cloud-api.yandex.net/v1/disk/resources?path={disk_path}', headers=headers(token))
        deserial_response = response.json()
        response.raise_for_status()

    # Обрабатываем исключения, переданные в ответе от сервера
    except requests.exceptions.HTTPError:

        # В случае получения статус-кода 401 проверяем токен доступа на валидность. В случае невалидности токена
        # программа завершается с соответствующим сообщением
        if response.status_code == 401:
            is_valid.not_valid_token()

        # В случае получения статус-кода 404 проверяем путь к удалённой папке на валидность. В случае невалидности пути
        # программа завершается с соответствующим сообщением
        elif response.status_code == 404:
            is_valid.not_valid_cloud_path()

        # Обрабатываем остальные 400-е и 500-е HTTP-коды
        logger.error(f'При попытке отсканировать папку в облачном хранилище сервер прислал ответ:\n'
                     f'HTTP-код: {response.status_code}\n'
                     f'{json.dumps(deserial_response, indent=4, ensure_ascii=False)}')

    # Обрабатываем исключения, не являющиеся HTTP-кодами
    except requests.exceptions.RequestException as e:
        logger.error(f'При попытке отсканировать папку в облачном хранилище произошла ошибка: {e}')
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f'После сканирования папки в облачном хранилище возникла ошибка при декодировании полученного JSON: {e}')
    except Exception as e:
        logger.error(f'При попытке обработать ответ от сервера возникло исключение: {e}')
    else:
        logger.info('Папка в облачном хранилище успешно отсканирована.')

        # Передаём десериализованный ответ на извлечение нужных данных и возвращаем словарь с этими данными
        return resp_filter(deserial_response)


# Функция получения ссылки на загрузку файла в удалённую папку. Подробное описание аналогично описанию функции scan_cloud
def get_upload_link(file_name: str, token: str, disk_path: str) -> Union[Dict, None]:
    try:
        response = requests.get(f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={disk_path}%2F{file_name}&fields=href&overwrite=true',
                                    headers=headers(token))
        deserial_response = response.json()
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.error(f'При попытке получить ссылку на загрузку файла {file_name} сервер прислал ответ:\n'
                     f'HTTP-код: {response.status_code}\n'
                     f'{json.dumps(deserial_response, indent=4, ensure_ascii=False)}')
    except requests.exceptions.RequestException as e:
        logger.error(f'При попытке получить ссылку на загрузку файла {file_name} произошла ошибка: {e}')
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f'После получения ссылки на загрузку файла {file_name} возникла ошибка при декодировании JSON: {e}')
    except Exception as e:
        logger.error(f'При попытке получить ссылку на загрузку файла {file_name} возникло исключение: {e}')
    else:
        logger.info(f'Ссылка на загрузку файла {file_name} успешно получена.')

        # Возвращаем ссылку на загрузку файла
        return deserial_response['href']


# Функция загрузки файла в удалённую папку
def upload_file(sync_folder: str, file_name: str, upload_link: str) -> None:
    # Пытаемся открыть и отправить файл в удалённую папку
    with open(os.path.join(sync_folder, file_name), 'rb') as f:
        try:
            response = requests.put(upload_link, files={'file': f})
            response.raise_for_status()

        # Обрабатываем исключения, переданные в ответе от сервера
        except requests.exceptions.HTTPError:
            logger.error(f'При попытке отправить файл {file_name} сервер прислал ответ:\n'
                         f'HTTP-код: {response.status_code}\n'
                         f'{json.dumps(response.json(), indent=4, ensure_ascii=False)}')

        # Обрабатываем исключения, не являющиеся HTTP-кодами
        except requests.exceptions.RequestException as e:
            logger.error(f'При попытке отправить файл {file_name} произошла ошибка: {e}')
        except Exception as e:
            logger.error(f'При попытке отправить файл {file_name} возникло исключение: {e}')
        else:
            logger.info(f'Файл {file_name} успешно отправлен.')


# Функция удаления файла из удалённой папки
def delete_files(file_name: str, token: str, disk_path) -> None:

    # Пытаемся удалить файл из удалённой папки
    try:
        response = requests.delete(f'https://cloud-api.yandex.net/v1/disk/resources?path={disk_path}%2F{file_name}',
                                        headers=headers(token))
        response.raise_for_status()

    # Обрабатываем исключения, переданные в ответе от сервера
    except requests.exceptions.HTTPError:
        logger.error(f'При попытке удалить файл {file_name} сервер прислал ответ:\n'
                     f'HTTP-код: {response.status_code}\n'
                     f'{json.dumps(response.json(), indent=4, ensure_ascii=False)}')

    # Обрабатываем исключения, не являющиеся HTTP-кодами
    except requests.exceptions.RequestException as e:
        logger.error(f'При попытке удалить файл {file_name} произошла ошибка: {e}')
    except Exception as e:
        logger.error(f'При попытке отправить файл {file_name} возникло исключение: {e}')
    else:
        logger.info(f'Файл {file_name} в облачном хранилище успешно удалён.')

