#!/usr/bin/env python

import asyncio

from grpclib.client import Channel

from src.config import CONFIG
from src.grpc_service.aws_email_pb2 import EmailRequest
from src.grpc_service.aws_email_grpc import EmailServiceStub

data = """
{
    "id": 1
}
"""


async def main():
    host, port = CONFIG.GRPC_LISTEN_ADDR.split(':')
    channel = Channel(host=host, port=port, loop=asyncio.get_event_loop())
    stub = HelloStub(channel)
    print(await stub.hello_action(HelloRequest(action=data)))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
