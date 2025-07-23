FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

WORKDIR  /app

COPY pyproject.toml uv.lock /app/

ARG ENV

RUN if [ "$ENV" = "only_main" ]; then \
      uv sync --no-dev --no-cache --compile-bytecode --frozen; \
    else \
      uv sync --all-groups --no-cache --compile-bytecode --frozen; \
    fi


COPY . /app

ENV PATH="/app/.venv/bin:$PATH"