FROM python:3.11-slim

WORKDIR /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Create a non-root user
    && groupadd -r appuser && useradd -r -g appuser -s /bin/bash -d /home/appuser appuser \
    && mkdir -p /home/appuser \
    && chown -R appuser:appuser /home/appuser

# Copy requirements file
COPY requirements.txt .

RUN pip install --upgrade pip 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only what's needed for the application
COPY user_management/ user_management/
COPY alembic/ alembic/
COPY alembic.ini .

# Change ownership of the application directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "user_management.main:app", "--host", "0.0.0.0", "--port", "8000"]