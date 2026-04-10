FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
# Копируем код из папки app/ (структура week-12)
COPY app/ ./app/
ENV PATH=/usr/local/bin:$PATH
EXPOSE 8230
# Путь к модулю: app.app:app (папка app, файл app.py, объект app)
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8230"]