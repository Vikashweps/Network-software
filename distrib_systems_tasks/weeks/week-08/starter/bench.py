import sys
import os
# Добавляем корень проекта в PYTHONPATH, чтобы видеть service_pb2
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import requests
import grpc
import service_pb2 as pb2
import service_pb2_grpc as pb2_grpc

REST_URL = "http://localhost:8000/likes"
GRPC_ADDR = "localhost:50051"
N = 1000

def bench_rest():
    print(" Запуск REST benchmark...")
    t0 = time.time()
    for _ in range(N):
        requests.get(REST_URL)
    t1 = time.time()
    dur = t1 - t0
    print(f"REST: {dur:.4f} сек | {N/dur:.1f} RPS")
    return dur

def bench_grpc():
    print(" Запуск gRPC benchmark...")
    channel = grpc.insecure_channel(GRPC_ADDR)
    stub = pb2_grpc.LikesServiceStub(channel)
    
    t0 = time.time()
    for _ in range(N):
        stub.ListLikes(pb2.ListLikesRequest())
    t1 = time.time()
    
    channel.close()
    dur = t1 - t0
    print(f" gRPC: {dur:.4f} сек | {N/dur:.1f} RPS")
    return dur

if __name__ == "__main__":
    print(f" Тест: {N} запросов к каждому сервису\n")
    rest_t = bench_rest()
    grpc_t = bench_grpc()
    
    ratio = rest_t / grpc_t
    print("\n ИТОГ:")
    if grpc_t < rest_t:
        print(f"   gRPC быстрее REST в {ratio:.2f}x")
    else:
        print(f"   REST быстрее gRPC в {1/ratio:.2f}x")