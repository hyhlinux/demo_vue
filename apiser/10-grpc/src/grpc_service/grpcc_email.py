#!/usr/bin/env python

import asyncio

from grpclib.client import Channel

try:
    from src.config import CONFIG
except ImportError:
    class CONFIG:
        # gRPC config
        GRPC_EMAIL_LISTEN_ADDR = "0.0.0.0:5005"
        GRPC_SERVER_SLEEP_SECONDS = 60 * 60 * 24
        GRPC_THREAD_POOLS_MAX_WORKERS = 1024
try:
    from src.grpc_service import EmailRequest, EmailServiceStub
except ImportError as e:
    print("ImportError {}".format(e))
    from lib import EmailRequest, EmailServiceStub
    # from aws_email_grpc import EmailServiceStub

def stub_email():
    host, port = CONFIG.GRPC_EMAIL_LISTEN_ADDR.split(':')
    channel = Channel(host=host, port=port, loop=asyncio.get_event_loop())
    return EmailServiceStub(channel)

stub = stub_email()


async def SendMail(to, body):
    req = EmailRequest()
    req.to = to
    req.htmlBody = body
    return await stub.SendMail(req)

async def main():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI1YWIzNzI4OGM0Y2Q3NDMyM2E3NjBjNGEiLCJleHAiOjE1MjE3MDk4MjR9.K7iIpm_WeLS-Xr9rcjvzfNxYPdRGk0o440ZE2NbXm7U"
    htmlBody = """
    Welcome Apkpure:
         <a href="http://192.168.0.96:8000/api/token?token={}">请激活</a>>
    """""
    htmlBody = htmlBody.format(token)
    resp = await SendMail("hyhlinux@163.com", body=htmlBody)
    print(resp)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
