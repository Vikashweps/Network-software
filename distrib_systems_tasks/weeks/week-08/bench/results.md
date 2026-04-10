# Результаты замеров

## Результаты

| Метрика | REST | gRPC |
|---------|------|------|
| Время выполнения (сек) | 2.3698 | 0.6201 |
| RPS (запросов/сек) | 422.0 | 1612.6 |
| **Относительная скорость** | 1.00x | **3.82x** |


## 🛠️ Настройка и запуск

**1. Окружение и зависимости:**
```bash
cd ~/Desktop/Network-software/distrib_systems_tasks
python3 -m venv venv
source venv/bin/activate
pip install grpcio grpcio-tools fastapi uvicorn requests
```

| Терминал | Команда | Порт |
|----------|---------|------|
| **1. gRPC-сервер** | `python server.py` | `50051` |
| **2. REST-сервер** | `python rest_server.py` | `8000` |
| **3. Бенчмарк** | `python starter/bench.py` | — |

**project_code**: `likes-s16` 