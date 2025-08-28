# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

ARG AXIESTUDIO_IMAGE
FROM $AXIESTUDIO_IMAGE

RUN rm -rf /app/.venv/axiestudio/frontend

CMD ["python", "-m", "axiestudio", "run", "--host", "0.0.0.0", "--port", "7860", "--backend-only"]
