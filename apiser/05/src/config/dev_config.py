from .config import Config
import asyncio_redis

class DevConfig(Config):
    DEBUG = True
    PORT = 8000
