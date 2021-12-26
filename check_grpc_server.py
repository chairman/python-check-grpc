import os
import sys

from nacos.usage import host_ip
from src.api import hello_pb2,hello_pb2_grpc
import grpc
import time
import _thread
from concurrent import futures
import asyncio
import json
import logging.config

def configure_logging(configure_file_path="LogConfigure.json", default_level=logging.INFO, env_key="LOG_CFG"):
    path = configure_file_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

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
            logging.info("nacos_send_heartbeat server on %s", code)
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

def set_log_info():
    logging.info("Let's start to log some information.")
    # logging.error("There are so many errors.")

if __name__ == '__main__':
    configure_logging("LogConfigure.json")
    set_log_info()
    logging.basicConfig(level=logging.INFO)
    register_success = nacos_register()
    if not register_success:
        print("注册失败")
    _thread.start_new_thread(nacos_send_heartbeat,())
    logging.info("init grpc finish ....")
    asyncio.run(serve())