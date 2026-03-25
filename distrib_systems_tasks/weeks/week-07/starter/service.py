import grpc
from concurrent import futures
import sys
import os

# Добавляем путь к сгенерированным файлам
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'generated'))

# Импортируем сгенерированные модули (имена согласно package users.v1)
import service_pb2
import service_pb2_grpc

# Простая база данных в памяти
users_db = {}
next_id = 1


class UsersServiceServicer(service_pb2_grpc.UsersServiceServicer):
    """Реализация сервиса UsersService"""
    
    def CreateUser(self, request, context):
        """Unary RPC: создание нового пользователя"""
        global next_id
        
        user_id = next_id
        next_id += 1
        
        # Сохраняем пользователя
        users_db[user_id] = {
            'id': user_id,
            'name': request.name,
            'email': request.email
        }
        
        # Возвращаем ответ
        return users_pb2.CreateUserResponse(
            id=user_id,
            name=request.name,
            email=request.email
        )
    
    def GetUser(self, request, context):
        """Unary RPC: получение пользователя по ID"""
        user = users_db.get(request.id)
        
        if not user:
            # Если пользователь не найден — возвращаем ошибку gRPC
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with id {request.id} not found")
            return users_pb2.GetUserResponse()
        
        return users_pb2.GetUserResponse(
            id=user['id'],
            name=user['name'],
            email=user['email']
        )
    
    def GetUsers(self, request, context):
        """Unary RPC: получение списка всех пользователей"""
        # Формируем список пользователей
        users = [
            users_pb2.User(
                id=u['id'],
                name=u['name'],
                email=u['email']
            )
            for u in users_db.values()
        ]
        
        return service_pb2.GetUsersResponse(users=users)


def serve():
    """Запуск gRPC сервера"""
    # Создаём сервер с пулом потоков
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Регистрируем наш сервис
    service_pb2_grpc.add_UsersServiceServicer_to_server(
        UsersServiceServicer(), server
    )
    
    # Слушаем порт 50051 (стандартный для gRPC)
    server.add_insecure_port('[::]:50051')
    
    # Запускаем сервер
    server.start()
    print(" gRPC сервер запущен на порту 50051")
    
    # Ждём завершения (блокирующий вызов)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()