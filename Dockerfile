FROM python:3.12-slim AS builder

RUN pip install uv
WORKDIR /app
COPY pyproject.toml .
RUN uv sync --no-dev --no-install-project

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

CMD ["python", "run.py"]
