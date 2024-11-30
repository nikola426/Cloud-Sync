<h1 align="center">Сервис бэкапа локальных файлов в облачное хранилище</h1>

<h3>1. Предназначение</h3>

Сервис предназначен для фонового периодического бэкапа файлов из локальной папки в удалённую.

<h3>2. Описание</h3>

Сервис написан на языке Python версии 3.12 c использованием библиотек 
<a href='https://loguru.readthedocs.io/en/stable/index.html'>loguru</a> и 
 <a href='https://requests.readthedocs.io/en/latest/'>requests</a>. Графического интерфейса не имеет.

Он сканирует указанную локальную папку и отправляет в удалённое хранилище добавленные или 
изменённые файлы. Если файл удалён, то он будет удалён и из хранилища. Синхронизация файлов 
происходит в одностороннем порядке, т.е. бэкап. **Сервис работает только с файлами!**

Данная версия сервиса работает только с <a href='https://yandex.ru/dev/disk/rest'>API Яндекс Диска</a>.
Однако в него можно достаточно легко добавить другие API для их параллельной работы, так как 
основная логика работы, прописанная в main.py, универсальна и может быть использована при расширении
практически без изменений.

<h3>2. Как запустить</h3>

**2.1. Ввод начальных данных**  

- Скопируйте проект себе на локальный носитель.  
- В файле config.ini укажите OAuth-токен доступа к Яндекс Диску (параметр YANDEX_TOKEN). Получить
токен можно <a href ='https://yandex.ru/dev/disk-api/doc/ru/concepts/quickstart#oauth'>здесь</a>.  
- Укажите абсолютный путь к синхронизируемой папке на локальном носителе (параметр YANDEX_SYNC_FOLDER). 

Параметр YANDEX_DISK_PATH хранит абсолютный путь к папке на Яндекс Диске (в URL-формате), куда будут бэкапиться файлы.  
Параметр YANDEX_PERIOD хранит период синхронизации сервиса Яндекса.  
Параметр YA_LOG_FILE_PATH хранит **относительный** путь к файлу лога сервиса Яндекса на локальном носителе.  
При добавлении нового сервиса (например, Google Drive или OneDrive) придётся указать новый блок входных данных по 
примеру блока YANDEX_DISK.

**2.2. Установка Python**  
Перед тем как запустить его, убедитесь, что Python установлен на вашем 
компьютере. Для установки:
   - **Windows**. Скачайте установщик с <a href='https://www.python.org/'>официального сайта Python</a>
и следуйте инструкциям. Обязательно отметьте опцию "Add Python to PATH".
   - **Linux**. Обычно Python предустановлен. Если нет, установите его с помощью команды:
`sudo apt-get install python3
`
   - **macOS**: Установите Python через Homebrew:
`brew install python
`

**2.3. Создание виртуального окружения (рекомендуется)**  
Для управления зависимостями проекта создайте виртуальное окружение: 
`python3 -m venv myenv
`  
Активируйте его:  
   - **Windows:** `myenv\Scripts\activate`
   - **Linux/macOS:** `source myenv/bin/activate`  

**2.4. Установка зависимостей**  
Установите зависимости командой: `pip install -r requirements.txt`  

**2.5. Запуск скрипта**  
Теперь Вы готовы запустить проект.  
Перейдите в директорию со скриптом: `cd /path/to/your/project`.  
Запустите скрипт с помощью команды: `python3 your_script.py`