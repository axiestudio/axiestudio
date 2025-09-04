# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

################################
# FRONTEND BUILDER
# Build the React frontend
################################
FROM --platform=$BUILDPLATFORM node:lts-bookworm-slim AS frontend-builder

WORKDIR /frontend
COPY src/frontend/package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

COPY src/frontend ./
RUN --mount=type=cache,target=/root/.npm \
    NODE_OPTIONS="--max-old-space-size=8192" npm run build

################################
# BACKEND BUILDER
# Build the Python backend with dependencies
################################
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS backend-builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install system dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    build-essential \
    git \
    gcc \
    locales \
    && apt-get clean \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen

# Copy dependency files
COPY ./uv.lock ./pyproject.toml ./README.md ./
COPY ./src/backend/base/uv.lock ./src/backend/base/pyproject.toml ./src/backend/base/README.md ./src/backend/base/

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-editable --extra postgresql

# Copy source code
COPY ./src /app/src

# Copy frontend build from frontend-builder stage
COPY --from=frontend-builder /frontend/build /app/src/backend/base/axiestudio/frontend

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable --extra postgresql

################################
# RUNTIME
# Final production image
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
COPY --from=backend-builder --chown=1000 /app/.venv /app/.venv

# Set up environment
ENV PATH="/app/.venv/bin:$PATH"
ENV AXIESTUDIO_HOST=0.0.0.0
ENV AXIESTUDIO_PORT=7860
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Labels
LABEL org.opencontainers.image.title=axiestudio-fullstack
LABEL org.opencontainers.image.authors=['Axie Studio']
LABEL org.opencontainers.image.licenses=MIT
LABEL org.opencontainers.image.url=https://github.com/axiestudio/axiestudio
LABEL org.opencontainers.image.source=https://github.com/axiestudio/axiestudio
LABEL org.opencontainers.image.description="Full-stack AxieStudio application with frontend and backend"

USER user
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Expose port
EXPOSE 7860

# Start the application
CMD ["axiestudio", "run", "--host", "0.0.0.0", "--port", "7860"]
