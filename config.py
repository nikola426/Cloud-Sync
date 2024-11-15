import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
YANDEX_SYNC_FOLDER = os.getenv("YANDEX_SYNC_FOLDER")
YANDEX_DISK_PATH = os.getenv("YANDEX_DISK_PATH")
YANDEX_PERIOD = os.getenv("YANDEX_PERIOD")
YA_LOG_FILE_PATH = os.getenv("YA_LOG_FILE_PATH")
