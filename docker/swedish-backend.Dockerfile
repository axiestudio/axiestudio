# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

################################
# BUILDER-BASE
# Used to build deps + create our virtual environment
################################

# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Set UTF-8 encoding for build stage
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    # deps for building python deps
    build-essential \
    git \
    # gcc
    gcc \
    # locale support for UTF-8
    locales \
    && apt-get clean \
    # Generate UTF-8 locale
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen

# Copy necessary files for dependency installation
COPY ./uv.lock ./pyproject.toml ./README.md ./
COPY ./src/backend/base/uv.lock ./src/backend/base/pyproject.toml ./src/backend/base/README.md ./src/backend/base/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-editable --extra postgresql

COPY ./src /app/src

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable --extra postgresql

################################
# RUNTIME
# Setup user, utilities and copy the virtual environment only
################################
FROM python:3.12.3-slim AS runtime

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y curl git libpq5 gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd user -u 1000 -g 0 --no-create-home --home-dir /app/data

COPY --from=builder --chown=1000 /app/.venv /app/.venv

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

LABEL org.opencontainers.image.title=axiestudio-swedish-backend
LABEL org.opencontainers.image.authors=['Axie Studio']
LABEL org.opencontainers.image.licenses=MIT
LABEL org.opencontainers.image.url=https://github.com/axiestudio/backend
LABEL org.opencontainers.image.source=https://github.com/axiestudio/backend

USER user
WORKDIR /app

ENV AXIESTUDIO_HOST=0.0.0.0
ENV AXIESTUDIO_PORT=7860

# Set UTF-8 encoding to handle emojis properly in Docker
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Run backend only
CMD ["python", "-m", "axiestudio", "run", "--host", "0.0.0.0", "--port", "7860", "--backend-only"]
