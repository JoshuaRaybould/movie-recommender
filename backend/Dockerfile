FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim
WORKDIR /app
COPY . /app

ENV UV_NO_DEV=1
RUN uv sync --locked
CMD ["/app/.venv/bin/fastapi", "run", "/app/src/backend/main.py", "--port", "8000"]
