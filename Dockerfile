FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

RUN pip install --no-cache-dir uv \
    && addgroup --system fastapi \
    && adduser --system --ingroup fastapi \
       --home /home/fastapi fastapi

COPY pyproject.toml uv.lock ./

# Production dependencies only; install the project separately.
RUN uv sync --frozen --no-dev --no-install-project

COPY --chown=fastapi:fastapi app/ ./app/
COPY --chown=fastapi:fastapi alembic.ini ./

# Development target: includes development dependency groups.
FROM base AS development

RUN uv sync --frozen --no-install-project

USER fastapi

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", \
     "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production target.
FROM base AS production

USER fastapi

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "app.main:app", \
     "--host", "0.0.0.0", "--port", "8000"]
