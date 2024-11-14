import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
SYNC_FOLDER = os.getenv("SYNC_FOLDER")
YANDEX_DISK_PATH = os.getenv("YANDEX_DISK_PATH")
PERIOD = os.getenv("PERIOD")
YA_LOG_FILE_PATH = os.getenv("YA_LOG_FILE_PATH")
