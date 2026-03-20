FROM python:3.13-slim-bookworm

RUN apt-get update && \
    apt-get install -y curl vim

COPY --from=ghcr.io/astral-sh/uv:0.7.9 /uv /uvx /bin/

ENV PATH="/root/.local/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/

COPY pyproject.toml uv.lock ./
COPY ./src ./src

RUN uv sync --locked

CMD ["sh", "-c", "uv run src/manage.py makemigrations && uv run src/manage.py migrate && uv run src/manage.py runserver 0.0.0.0:8001"]