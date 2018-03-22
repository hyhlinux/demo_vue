#!/usr/bin/env python
"""
 Created by howie.hu at  17-10-16.
"""
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
    # from .hello_pb2 import HelloResponse
    # from .hello_pb2_grpc import HelloServicer, HelloStub, add_HelloServicer_to_server


GRPC_LISTEN_ADDR = CONFIG.GRPC_LISTEN_ADDR
GRPC_THREAD_POOLS_MAX_WORKERS = CONFIG.GRPC_THREAD_POOLS_MAX_WORKERS
GRPC_SERVER_SLEEP_SECONDS = CONFIG.GRPC_SERVER_SLEEP_SECONDS


class Hello(hello_pb2_grpc.HelloServicer):
    def hello_action(self, request, context):
        data = request.action
        ip = context.peer()
        print(data, ip)
        reply = hello_pb2.HelloResponse(message=data)
        print(reply)
        return reply


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=GRPC_THREAD_POOLS_MAX_WORKERS))
    hello_pb2_grpc.add_HelloServicer_to_server(Hello(), server)
    print("grpcs-hello:", GRPC_LISTEN_ADDR)
    server.add_insecure_port(GRPC_LISTEN_ADDR)
    server.start()
    try:
        while True:
            time.sleep(GRPC_SERVER_SLEEP_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
