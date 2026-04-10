FROM python:3.11-slim AS builder
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app/ ./app/
ENV PATH=/usr/local/bin:$PATH
EXPOSE 8107
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8107"]