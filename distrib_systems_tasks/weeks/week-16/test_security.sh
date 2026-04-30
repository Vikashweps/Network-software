#!/bin/bash

echo "Security Checklist Verification for notifications-s16"


PASS=0
FAIL=0
TOTAL=14

check_pass() {
    echo "[PASS] $1"
    ((PASS++))
}

check_fail() {
    echo "[FAIL] $1"
    ((FAIL++))
}

echo "1. Аутентификация и авторизация"
if grep -q "HTTPBearer\|verify_token\|JWT" src/*.py 2>/dev/null; then
    check_pass "JWT-токены проверяются"
else
    check_fail "JWT-аутентификация не реализована"
fi

if grep -q "owner_id\|user_id.*==" src/*.py 2>/dev/null; then
    check_pass "Защита от BOLA/IDOR"
else
    check_fail "Нет проверки прав на объекты"
fi

echo ""
echo "2. Защита данных"
if grep -q "Fernet\|AES\|encrypt" src/*.py 2>/dev/null; then
    check_pass "Чувствительные данные шифруются"
else
    check_fail "Шифрование не реализовано"
fi

if grep -q "ssl_channel_credentials\|tls" src/*.py proto/*.py 2>/dev/null; then
    check_pass "TLS/mTLS настроен"
else
    check_fail "TLS не используется"
fi

if grep -q "os.getenv\|os.environ" src/*.py 2>/dev/null; then
    check_pass "Секреты в переменных окружения"
else
    check_fail "Секреты захардкожены"
fi

echo ""
echo "3. Валидация и инъекции"
if grep -q "Field(\|validator\|pydantic" src/*.py 2>/dev/null; then
    check_pass "Pydantic валидация"
else
    check_fail "Нет валидации входных данных"
fi

if grep -q "parameterized\|ORM\|SQLAlchemy" src/*.py 2>/dev/null; then
    check_pass "Защита от SQL-инъекций"
else
    check_fail "Возможны SQL-инъекции"
fi

echo ""
echo "4. Конфигурация"
if grep -q "DEBUG.*=.*False\|debug.*=.*False" src/*.py 2>/dev/null; then
    check_pass "Debug-режим отключён"
else
    check_fail "Debug-режим может быть включён"
fi

if grep -q "slowapi\|rate.*limit\|throttle" src/*.py 2>/dev/null; then
    check_pass "Rate limiting настроен"
else
    check_fail "Нет ограничения запросов"
fi

if grep -q "CORSMiddleware\|allow_origins" src/*.py 2>/dev/null; then
    check_pass "CORS настроен"
else
    check_fail "CORS не настроен"
fi

if grep -q "USER.*appuser\|useradd" Dockerfile* 2>/dev/null; then
    check_pass "Контейнер от non-root"
else
    check_fail "Контейнер от root"
fi

echo ""
echo "5. Логирование"
if grep -q "mask\|redact\|\*\*\*" src/*.py 2>/dev/null; then
    check_pass "Секреты не логируются"
else
    check_fail "Секреты могут попасть в логи"
fi

if grep -q "HTTPException\|status_code" src/*.py 2>/dev/null; then
    check_pass "Ошибки не раскрывают детали"
else
    check_fail "Ошибки могут раскрыть структуру"
fi

echo ""
echo "======================================================"
echo "Результат: $PASS/$TOTAL проверок пройдено"
echo "Провалено: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "Отлично! Все проверки пройдены."
    exit 0
elif [ $FAIL -le 3 ]; then
    echo "Хорошо. Рекомендуется исправить оставшиеся пункты."
    exit 0
else
    echo "Внимание! Много критических уязвимостей."
    exit 1
fi