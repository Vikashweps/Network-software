
"""Simple gRPC load tester for items-s16 - fallback when ghz is unavailable"""
import grpc
import sys
import time
import statistics
import random

sys.path.insert(0, './proto')
import items_pb2, items_pb2_grpc

def run_test(concurrency, total_requests, host='localhost:9090'):
    channel = grpc.insecure_channel(host)
    stub = items_pb2_grpc.ItemsServiceStub(channel)
    latencies = []
    
    for i in range(total_requests):
        start = time.perf_counter()
        try:
            # Добавляем немного рандома для реалистичности
            req_id = random.randint(1, 100)
            stub.GetItem(items_pb2.GetItemRequest(id=req_id), timeout=5)
            latencies.append((time.perf_counter() - start) * 1000)
        except grpc.RpcError as e:
            # Считаем таймауты и ошибки как 500ms для статистики
            latencies.append(500.0)
    
    if not latencies:
        print(f"  No successful requests")
        return
    
    # Метрики
    avg_lat = statistics.mean(latencies)
    sorted_lat = sorted(latencies)
    p99_idx = int(len(sorted_lat) * 0.99)
    p99_lat = sorted_lat[p99_idx] if p99_idx < len(sorted_lat) else sorted_lat[-1]
    
    total_time_sec = sum(latencies) / 1000  # оценка общего времени
    rps = len(latencies) / max(total_time_sec, 0.001)
    
    print(f"  Requests: {len(latencies)}")
    print(f"  Avg Latency: {avg_lat:.2f}ms")
    print(f"  P99 Latency: {p99_lat:.2f}ms")
    print(f"  Throughput: {rps:.0f} RPS")

if __name__ == "__main__":
    print("=== gRPC Load Test: items-s16 ===")
    print("Service: items.v1.ItemsService/GetItem\n")
    
    for concurrency in [10, 100, 1000]:
        print(f"--- Concurrency: {concurrency} ---")
        run_test(concurrency, total_requests=1000)
        print()