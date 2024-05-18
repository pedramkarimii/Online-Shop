# Use a slim Python image as the base
FROM python:3.10-slim AS builder

# Set build-time variables
ARG POETRY_VERSION="1.1.11"

# Install system dependencies required for building Python packages and Poetry
RUN apk update \
    && apk add --no-cache --virtual .build-deps \
        build-base \
        libffi-dev \
        postgresql-dev \
    && apk add --no-cache \
        postgresql-client \
    && pip install --no-cache-dir "poetry==$POETRY_VERSION" \
    && apk del .build-deps

# Set the working directory inside the container
WORKDIR /code

# Copy only the dependency files to leverage Docker cache
COPY pyproject.toml poetry.lock* /code/

# Install project dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Stage 2: Runtime stage
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

# Install runtime dependencies
RUN apk update \
    && apk add --no-cache \
        libpq \
    && rm -rf /var/cache/apk/*

# Create a non-root user and switch to it
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -D appuser
USER appuser

# Set the working directory inside the container
WORKDIR /code

# Copy the project code
COPY --chown=appuser:appgroup . /code/

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4"]
