ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_PROGRESS_BAR=off \
    PIP_ROOT_USER_ACTION=ignore \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN python -m venv /opt/poetry \
    && /opt/poetry/bin/python -m pip install --quiet --upgrade pip poetry

COPY pyproject.toml poetry.lock README.md ./

RUN /opt/poetry/bin/poetry install --with dev --no-root --no-ansi

ENV PATH="/opt/poetry/bin:${PATH}" \
    PYTHONPATH=/app
