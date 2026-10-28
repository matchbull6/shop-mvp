FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /bin/

WORKDIR /app
ENV UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY app/ ./app/

ENV PATH="/app/.venv/bin:$PATH" \
    PORT=8000
EXPOSE 8000
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
