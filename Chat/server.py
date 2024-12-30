# server.py
import asyncio
import websockets

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    print(f"New client connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Received: {message}")
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except websockets.ConnectionClosed:
        print(f"Client {websocket.remote_address} disconnected")
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8080):
        print("Server started on ws://localhost:8080")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
