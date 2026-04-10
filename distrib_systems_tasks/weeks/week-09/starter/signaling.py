# signaling.py
import asyncio
import websockets
import json

# Храним подключения: { "user1": websocket, "user2": websocket }
clients = {}

async def handler(websocket):
    client_id = None
    try:
        async for raw_msg in websocket:
            msg = json.loads(raw_msg)
            msg_type = msg.get("type")

            # 1. Регистрация клиента по ID
            if msg_type == "join":
                client_id = msg.get("id")
                clients[client_id] = websocket
                print(f" Peer {client_id} подключён")
                continue

            # 2. Пересылка сообщения КОНКРЕТНОМУ собеседнику
            target = msg.get("target")
            if target and target in clients:
                await clients[target].send(raw_msg)
            else:
                print(f" Целевой peer {target} не найден или не указан")

    except websockets.ConnectionClosed:
        pass
    finally:
        if client_id:
            clients.pop(client_id, None)
        print(f" Peer {client_id} отключён")

async def main():
    print(" Signaling server запущен на ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())