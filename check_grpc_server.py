import os
import sys

from nacos.usage import host_ip
from src.api import hello_pb2,hello_pb2_grpc
import grpc
import time
from concurrent import futures
import asyncio
import logging
import nacos
NACOS_SERVER_ADDRESSES = "112.74.87.26:8848"
NACOS_NAMESPACE = "passjava"
nacos_client = nacos.NacosClient(NACOS_SERVER_ADDRESSES,namespace=NACOS_NAMESPACE)
server_name = "python-check-grpc"
cluster_name = "cluster-1"
host_ip = "0.0.0.0"
rpc_port = "5005"

def nacos_register():
    try:
        success = nacos_client.add_naming_instance(server_name,
        host_ip,rpc_port,cluster_name,1,"{}",True,True)
        return success
    except Exception as e:
        return False

def nacos_send_heartbeat():
    while True:
        try:
            time.sleep(5)
            interval = nacos_client.send_heartbeat(server_name,
                    host_ip,rpc_port,cluster_name,1,"{}")
            code = interval['code']
        except Exception as e:
            print(e)

class Greeter(hello_pb2_grpc.GreeterServicer):

    async def SayHello(
            self, request: hello_pb2.HelloRequest,
            context: grpc.aio.ServicerContext) -> hello_pb2.HelloReply:
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)

async def serve() -> None:
    server = grpc.aio.server()
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = '[::]:'+rpc_port
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    register_success = nacos_register()
    if not register_success:
        print("xxxx")
    asyncio.run(serve())