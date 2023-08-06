import asyncio
import websockets
from core.kafkaUtil import general_listener


async def hello(websocket, path):
    # name = await websocket.recv()
    # print(f"< {name}")
    # greeting = f"Hello {name}!"

    # await websocket.send(greeting)
    # print(f"> {greeting}")
    await websockets.send(general_listener("testTopic","127.0.0.1:9092"))

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
