import os
import sys
from src.api import hello_pb2,hello_pb2_grpc
import grpc
import time
from concurrent import futures
import asyncio
import logging

class Greeter(hello_pb2_grpc.GreeterServicer):

    async def SayHello(
            self, request: hello_pb2.HelloRequest,
            context: grpc.aio.ServicerContext) -> hello_pb2.HelloReply:
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)


async def serve() -> None:
    server = grpc.aio.server()
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = '[::]:5005'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())