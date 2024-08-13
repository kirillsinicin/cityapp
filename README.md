## Установка проекта
### 1. Клонировать репозиторий по SSH
```console
git clone git@github.com:kirillsinicin/cityapp.git
```
### или URL
```console
git clone https://github.com/kirillsinicin/linkapp.git
```
### 2. Настроить виртуальное окружение
```console
python3 -m venv .venv
```
```console
. .venv/bin/activate
```
### 3. Установить зависимости
```console
pip install poetry
```
```console
poetry install
```
## Запуск сервера
### 1. Добавить файл .env в корень проекта и ввести следующее значение:
```console
DATABASE_URL="postgresql+psycopg2://kiruha:kiruha@localhost:8988/kiruha"
```
### 2. Запустить docker-контейнеры
```console
docker compose up
```
### 3. Запустить сервер
```console
fastapi dev
```
## Тестирование
### Для запуска тестов достаточно выполнить команду
```console
pytest
```
### Чтобы узнать процент покрытия тестами
```console
pytest --cov=app --cov-report html
```
> В таком случае в каталоге появится директория htmlcov, где находится файл index.html, открыв который можно получить более детальный вид.
