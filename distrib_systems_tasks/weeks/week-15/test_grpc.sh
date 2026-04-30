#!/bin/bash
# Load test for gRPC API - items-s16

PROTO_PATH="./proto/items.proto"
CALL="items.v1.ItemsService/GetItem"
HOST="localhost:9090"

echo "=== gRPC Load Test: items-s16 ==="
echo "Service: $CALL"
echo "Host: $HOST"

for concurrency in 10 100 1000; do
    echo ""
    echo "--- Concurrency: $concurrency ---"
    ghz --proto=$PROTO_PATH \
        --call=$CALL \
        --insecure \
        -c $concurrency \
        -n 1000 \
        -d 30s \
        "$HOST"
done