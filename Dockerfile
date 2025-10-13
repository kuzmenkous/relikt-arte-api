# Stage 1: Base environment setup
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

# Stage 2: Poetry setup and Python wheels building
FROM base AS builder

WORKDIR /app/temp

COPY pyproject.toml poetry.lock ./

# Install the poetry-plugin-export to enable the 'export' command
RUN poetry self add poetry-plugin-export \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root -v \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /app/temp/wheels -r requirements.txt \
    && rm requirements.txt

# Stage 3: Application and dependency installation
FROM base AS src

COPY --from=builder /app/temp/wheels /app/temp/wheels

RUN pip install --no-cache-dir /app/temp/wheels/* && rm -rf /app/temp/wheels

COPY src src
COPY alembic.ini .
COPY migrations migrations
COPY scripts/run.sh /app/run.sh
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN chmod +x /app/run.sh

ENV PYTHONPATH="/app/api/src:${PYTHONPATH}"

FROM src AS mailer

ENTRYPOINT [ "faststream", "run", "src.mailer.app:app" ]

HEALTHCHECK --start-period=5s --start-interval=1s --interval=1h CMD [ "curl", "-f", "http://localhost:8000/liveness" ]

# Stage 4: Final image for the API
FROM src AS api

ENTRYPOINT ["/app/run.sh"]
