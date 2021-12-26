import asyncio
import logging

import grpc
from src.api import hello_pb2,hello_pb2_grpc

async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:5005') as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response = await stub.SayHello(hello_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())