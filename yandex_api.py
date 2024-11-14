from loguru import logger
import requests

from config import YANDEX_DISK_PATH


def headers(token):
    head = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    return head


def resp_filter(resp):
    data_list = []
    for file_data in resp['_embedded']['items']:
        data_dict = {
            'name': file_data['name'],
            'modified': file_data['modified']
        }
        data_list.append(data_dict)

    return data_list


@logger.catch
def scan_cloud(token):
    response = requests.get(f'https://cloud-api.yandex.net/v1/disk/resources?path={YANDEX_DISK_PATH}', headers=headers(token))
    if response.status_code == 200:
        logger.info('Папка в облачном хранилище успешно отсканирована. Данные получены.')
        response = response.json()
        return resp_filter(response)

    elif response.status_code == 401:
        logger.error('Возможно, у Вас неправильный токен доступа. Авторизуйтесь для сканирования')
    else:
        logger.error(f'При попытке отсканировать папку в облачном хранилище сервер прислал ответ с HTTP-кодом: {response.status_code}.')


@logger.catch
def upload_files(file_list, token, sync_folder):
    for file_name in file_list:
        response = requests.get(f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={YANDEX_DISK_PATH}{file_name}&fields=href&overwrite=true',
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
        response = requests.delete(f'https://cloud-api.yandex.net/v1/disk/resources?path={YANDEX_DISK_PATH}{file_name}', headers=headers(token))
        if response.status_code == 204:
            logger.info(f'Файл {file_name} в облачном хранилище успешно удалён.')
        elif response.status_code == 401:
            logger.error(f'Возможно, у Вас неправильный токен доступа. Авторизуйтесь для удаления файла {file_name}.')
        else:
            logger.error(f'При попытке удалить файл {file_name} сервер прислал ответ с HTTP-кодом: {response.status_code}.')
    return
