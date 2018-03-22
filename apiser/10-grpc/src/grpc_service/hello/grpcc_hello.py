#!/usr/bin/env python

import asyncio

from grpclib.client import Channel

try:
    from src.config import CONFIG
except ImportError:
    class CONFIG:
        # gRPC config
        GRPC_LISTEN_ADDR = "0.0.0.0:7000"
        GRPC_SERVER_SLEEP_SECONDS = 60 * 60 * 24
        GRPC_THREAD_POOLS_MAX_WORKERS = 1024
try:
    from src.grpc_service import hello_pb2, hello_grpc
except ImportError:
    import hello_pb2
    import hello_grpc
    from hello_pb2 import HelloRequest
    from hello_grpc import HelloStub


def stub_hello():
    host, port = CONFIG.GRPC_LISTEN_ADDR.split(':')
    channel = Channel(host=host, port=port, loop=asyncio.get_event_loop())
    return HelloStub(channel)

stub = stub_hello()

async def main():
    resp = await stub.hello_action(HelloRequest(action="hello"))
    print(resp.message)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
