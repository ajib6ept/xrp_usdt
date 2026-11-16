FROM python:3.9.15-slim-buster

WORKDIR /code

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.3.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version


COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY . /code

CMD ["make", "xrp-usdt"]
