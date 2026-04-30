import grpc
from concurrent import futures
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'proto'))

import notifications_pb2
import notifications_pb2_grpc

notifications_db = []
id_counter = 1

class NotificationsServicer(notifications_pb2_grpc.NotificationsServiceServicer):
    def CreateNotification(self, request, context):
        global id_counter
        notification = notifications_pb2.Notification(
            id=id_counter,
            message=request.message,
            channel=request.channel,
            recipient=request.recipient,
            created_at=int(time.time()),
            status="sent"
        )
        notifications_db.append(notification)
        id_counter += 1
        return notification

    def GetNotification(self, request, context):
        for notif in notifications_db:
            if notif.id == request.id:
                return notif
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Notification not found")
        return notifications_pb2.Notification()

    def ListNotifications(self, request, context):
        filtered = notifications_db
        if request.channel:
            filtered = [n for n in filtered if n.channel == request.channel]
        
        start = (request.page - 1) * request.page_size
        end = start + request.page_size
        
        return notifications_pb2.ListNotificationsResponse(
            notifications=filtered[start:end],
            total=len(filtered)
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notifications_pb2_grpc.add_NotificationsServiceServicer_to_server(
        NotificationsServicer(), server
    )
    server.add_insecure_port('[::]:9090')
    server.start()
    print("gRPC server started on [::]:9090")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()