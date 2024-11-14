import requests
from loguru import logger

from config import YANDEX_DISK_PATH


def headers(token):
    head = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    return head

@logger.catch
def upload_files(file_list, token, sync_folder):
    for file_name in file_list:
        response = requests.get(f'{YANDEX_DISK_PATH}{file_name}&fields=href&overwrite=true',
                                headers=headers(token))
        if response.status_code == 200:
            response = response.json()
            with open('/'.join((sync_folder, file_name)), 'rb') as f:
                try:
                    requests.put(response['href'], files={'file': f})
                except Exception as e:
                    logger.error(f'При попытке отправить файл {file_name} возникло исключение:\n{e}.')
                else:
                    logger.info(f'Файл {file_name} успешно отправлен.')
        elif response.status_code == 401:
            logger.error(f'Возможно, у Вас неправильный токен доступа. Авторизуйтесь для отправки файла {file_name}.')
        else:
            logger.error(f'При попытке получить ссылку для загрузки файла {file_name} сервер прислал ответ с HTTP-кодом: {response.status_code}.')
    return

@logger.catch
def delete_files(file_list, token):
    for file_name in file_list:
        response = requests.delete(f'{YANDEX_DISK_PATH}{file_name}', headers=headers(token))
        if response.status_code == 204:
            logger.info(f'Файл {file_name} в облачном хранилище успешно удалён.')
        elif response.status_code == 401:
            logger.error(f'Возможно, у Вас неправильный токен доступа. Авторизуйтесь для удаления файла {file_name}.')
        else:
            logger.error(f'При попытке удалить файл {file_name} сервер прислал ответ с HTTP-кодом: {response.status_code}.')
    return
