FROM python:3.12

RUN mkdir /web-task-manager

RUN pip install poetry

WORKDIR /web-task-manager

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install

COPY . .