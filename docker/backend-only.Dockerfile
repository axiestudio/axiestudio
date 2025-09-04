# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

################################
# BUILDER-BASE
# Used to build deps + create our virtual environment
################################
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install UV and system dependencies for building
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    build-essential \
    git \
    gcc \
    curl \
    locales \
    && apt-get clean \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    # Install UV package manager
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.cargo/bin/uv /usr/local/bin/uv

# Copy dependency files
COPY ./uv.lock ./pyproject.toml ./README.md ./
COPY ./src/backend/base/uv.lock ./src/backend/base/pyproject.toml ./src/backend/base/README.md ./src/backend/base/

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-editable --extra postgresql

# Copy source code
COPY ./src /app/src

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable --extra postgresql

################################
# RUNTIME
# Setup user, utilities and copy the virtual environment only
################################
FROM python:3.12.3-slim AS runtime

# Install runtime dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    curl \
    git \
    libpq5 \
    gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd user -u 1000 -g 0 --no-create-home --home-dir /app/data

# Copy virtual environment from builder
COPY --from=builder --chown=1000 /app/.venv /app/.venv

# Set up environment
ENV PATH="/app/.venv/bin:$PATH"
ENV AXIESTUDIO_HOST=0.0.0.0
ENV AXIESTUDIO_PORT=7860
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Labels
LABEL org.opencontainers.image.title=axiestudio-backend
LABEL org.opencontainers.image.authors=['Axie Studio']
LABEL org.opencontainers.image.licenses=MIT
LABEL org.opencontainers.image.url=https://github.com/axiestudio/axiestudio
LABEL org.opencontainers.image.source=https://github.com/axiestudio/axiestudio
LABEL org.opencontainers.image.description="Backend-only AxieStudio API server"

USER user
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Expose port
EXPOSE 7860

# Run backend only with API-only mode
CMD ["python", "-m", "axiestudio", "run", "--host", "0.0.0.0", "--port", "7860", "--backend-only"]
