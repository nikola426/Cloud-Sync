import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

TOKEN = os.getenv("TOKEN")
SYNC_FOLDER = os.getenv("SYNC_FOLDER")
DISK_PATH = os.getenv("DISK_PATH")
PERIOD = os.getenv("PERIOD")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")
