# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

################################
# FRONTEND BUILDER
# Build the React frontend application
################################
FROM --platform=$BUILDPLATFORM node:lts-bookworm-slim AS builder

WORKDIR /frontend

# Copy package files for dependency installation
COPY src/frontend/package*.json ./

# Install dependencies with cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Copy source code
COPY src/frontend ./

# Build the application
RUN --mount=type=cache,target=/root/.npm \
    NODE_OPTIONS="--max-old-space-size=8192" npm run build

################################
# RUNTIME
# Serve the frontend with nginx
################################
FROM nginxinc/nginx-unprivileged:stable-bookworm-perl AS runtime

# Labels
LABEL org.opencontainers.image.title=axiestudio-frontend
LABEL org.opencontainers.image.authors=['Axie Studio']
LABEL org.opencontainers.image.licenses=MIT
LABEL org.opencontainers.image.url=https://github.com/axiestudio/axiestudio
LABEL org.opencontainers.image.source=https://github.com/axiestudio/axiestudio
LABEL org.opencontainers.image.description="Frontend-only AxieStudio application with nginx"

# Copy built frontend from builder stage
COPY --from=builder --chown=nginx /frontend/build /usr/share/nginx/html

# Copy nginx configuration files
COPY --chown=nginx ./docker/frontend/start-nginx.sh /start-nginx.sh
COPY --chown=nginx ./docker/frontend/default.conf.template /etc/nginx/conf.d/default.conf.template

# Make start script executable
RUN chmod +x /start-nginx.sh

# Environment variables with defaults
ENV BACKEND_URL=""
ENV FRONTEND_PORT="80"
ENV AXIEFLOW_MAX_FILE_SIZE_UPLOAD="100"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${FRONTEND_PORT}/health || curl -f http://localhost:${FRONTEND_PORT}/ || exit 1

# Expose port
EXPOSE 80

# Start nginx with environment variable substitution
ENTRYPOINT ["/start-nginx.sh"]
