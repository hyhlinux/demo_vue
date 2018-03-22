#!/usr/bin/env python
"""
 Created by hyhlinux at  18-03-21.
"""
import asyncio

from grpclib.server import Server
from grpclib.client import Channel
import grpc
import time

from concurrent import futures


try:
    from src.config import CONFIG
except ImportError:
    class CONFIG:
        # gRPC config
        GRPC_LISTEN_ADDR = "0.0.0.0:7000"
        GRPC_SERVER_SLEEP_SECONDS = 60 * 60 * 24
        GRPC_THREAD_POOLS_MAX_WORKERS = 1024
try:
    from src.grpc_service import hello_pb2, hello_pb2_grpc
except ImportError:
    import hello_pb2
    import hello_pb2_grpc
    import hello_grpc

GRPC_LISTEN_ADDR = CONFIG.GRPC_LISTEN_ADDR
GRPC_THREAD_POOLS_MAX_WORKERS = CONFIG.GRPC_THREAD_POOLS_MAX_WORKERS
GRPC_SERVER_SLEEP_SECONDS = CONFIG.GRPC_SERVER_SLEEP_SECONDS


class Hello(hello_grpc.HelloBase):
    async def hello_action(self, stream):
        request = await stream.recv_message()
        message = 'Hello, {}!'.format(request.action)
        await stream.send_message(hello_pb2.HelloResponse(message=message))


def serve():
    print("grpcs-hello:", GRPC_LISTEN_ADDR)
    loop = asyncio.get_event_loop()
    server = Server([Hello()], loop=loop)
    loop.run_until_complete(server.start(GRPC_LISTEN_ADDR.split(":")[0], int(GRPC_LISTEN_ADDR.split(":")[1])))


if __name__ == '__main__':
    serve()
