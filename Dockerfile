FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1

WORKDIR /

RUN groupadd -g 2000 app \
    && useradd -u 2000 -g 2000 -M -s /bin/sh app

ENV POETRY_VERSION=1.7.1

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./
COPY python_duty_bot/ /python_duty_bot/

RUN mkdir -p /python_duty_bot \
    && poetry config virtualenvs.create false \
    && poetry install --no-cache --no-interaction --no-ansi \
    && rm -rf poetry.lock pyproject.toml \
    && chmod -R a-w /python_duty_bot/* \
    && mkdir /python_duty_bot/data && chown -R app:app /python_duty_bot/data

WORKDIR /python_duty_bot
USER app
ENTRYPOINT ["python", "main.py"]
