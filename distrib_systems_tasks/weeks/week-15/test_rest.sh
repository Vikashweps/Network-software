#!/bin/bash
# Load test for REST API - items-s16

BASE_URL="http://localhost:8281/api/items"

echo "=== REST API Load Test: items-s16 ==="
echo "Endpoint: $BASE_URL"

for concurrency in 10 100 1000; do
    echo ""
    echo "--- Concurrency: $concurrency ---"
    wrk -t4 -c$concurrency -d30s --latency "$BASE_URL"
done