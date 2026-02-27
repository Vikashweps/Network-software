FROM ubuntu:24.04

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

ENV PATH="/home/appuser/venv/bin:$PATH"
COPY --chown=appuser:appuser requirement.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    && useradd -m -s /bin/bash appuser \
    && mkdir -p /app \
    && chown appuser:appuser /app \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /home/appuser/venv \
    && pip install --no-cache-dir -r requirement.txt


COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser schemas.py .


EXPOSE 8223

USER appuser
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8223"]