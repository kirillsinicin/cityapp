FROM python:3.12.3

WORKDIR /cityapp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /cityapp/

RUN POETRY_VIRTUALENVS_CREATE=false poetry install

COPY ./app /cityapp/app

CMD ["fastapi", "run", "--port", "80"]