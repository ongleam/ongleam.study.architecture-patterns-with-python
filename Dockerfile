FROM python:3.11-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir -p /app
WORKDIR /app

COPY pyproject.toml /app/
COPY src/ /app/src/
RUN uv sync --extra dev

COPY tests/ /app/tests/

ENV FLASK_APP=allocation/entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD uv run flask run --host=0.0.0.0 --port=80
