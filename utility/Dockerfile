# Use a slim Python image as the base
FROM python:3.10-slim AS builder

# Set build-time variables
ARG POETRY_VERSION="1.1.11"

# Install system dependencies required for building Python packages and Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential libffi-dev libpq-dev && \
    pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

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
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev && \
    pip install "celery"

# Create a non-root user and switch to it
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser

# Set the working directory inside the container
WORKDIR /code

# Copy the project code
COPY --chown=appuser:appgroup . /code/

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4"]
