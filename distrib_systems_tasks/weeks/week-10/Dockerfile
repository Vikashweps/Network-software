# Stage 1: Builder (сборка зависимостей)
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (финальный образ)
FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /install /usr/local
COPY app.py schemas.py .

EXPOSE 8116
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8116"]
