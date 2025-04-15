FROM python:3.11-slim

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini .

RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add security options
EXPOSE 8000
ENV PORT=8000



CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]