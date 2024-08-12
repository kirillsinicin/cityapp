## Запуск проекта
1. git clone git@github.com:kirillsinicin/cityapp.git
2. python3 -m venv .venv
3. . .venv/bin/activate
4. pip install poetry
5. poetry install ?package-mode = False into pyproject.toml
6. Добавить файл .env в корень проекта и ввести следующее значение:
   DATABASE_URL="postgresql+psycopg2://kiruha:kiruha@localhost:8988/kiruha"
7. docker compose up
8. fastapi dev
