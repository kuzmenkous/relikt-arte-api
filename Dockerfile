FROM python:3.13-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/api

RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    procps \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root -v \
    && rm -rf /root/.cache/pypoetry

COPY src src
COPY alembic.ini .
COPY migrations migrations
COPY scripts/run.sh /app/run.sh
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN chmod +x /app/run.sh

ENV PYTHONPATH="/app/api/src:${PYTHONPATH}"

FROM base AS api

ENTRYPOINT ["/app/run.sh"]
