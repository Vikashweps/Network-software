import grpc
from concurrent import futures
import service_pb2 as pb2
import service_pb2_grpc as pb2_grpc

likes_db = []
next_id = 1

class LikesService(pb2_grpc.LikesServiceServicer):
    
    def CreateLike(self, request, context):
        global next_id
        like = pb2.Like(
            id=next_id,
            author=request.author,
            target=request.target,
            created_at=0  
        )
        likes_db.append(like)
        next_id += 1
        return like

    def GetLike(self, request, context):
        for like in likes_db:
            if like.id == request.id:
                return like
        context.set_code(grpc.StatusCode.NOT_FOUND)
        return pb2.Like()

    def ListLikes(self, request, context):
        return pb2.ListLikesResponse(likes=likes_db)

    def StreamLikes(self, request, context):
        sent = 0
        for like in likes_db:
            if request.target_filter and like.target != request.target_filter:
                continue
            yield like
            sent += 1
            if request.count > 0 and sent >= request.count:
                break

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_LikesServiceServicer_to_server(LikesService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()