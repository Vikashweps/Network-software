FROM python:3.12-slim


WORKDIR /app 

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY app.py .
COPY schemas.py .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]