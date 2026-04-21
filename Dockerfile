FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /uvx /bin/

COPY pyproject.toml ./
RUN uv sync --no-dev

COPY app app
COPY alembic alembic
COPY alembic.ini .

EXPOSE 8000
EXPOSE 9090

CMD ["/root/.local/bin/uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
