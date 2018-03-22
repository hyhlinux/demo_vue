import os

class Config(object):
    """
    Basic config for proj
    """
    TIMEZONE = 'Asia/Shanghai'
    WEBSITE = dict(
        TOKEN='owllook',
    )
    BASE_DIR = os.path.dirname(os.path.abspath(__name__))
    DB_CONF = {
        "mongo": "mongodb://{host}:{port}/{database}".format( database='test', port=27017, host='localhost' )
    }
    # Application config
    DEBUG = False
    JWT = {
        "salt": "+-*/.",
        "sercret": 'tplinux',
        "algorithm": "HS256",
        "payload_pre": "++",
        "payload_end": "--",
    }
    WHITE_PATH = {
        "/api/register": True,
        "/api/login": True,
    }
    GRPC_EMAIL_LISTEN_ADDR = "0.0.0.0:5005"
    GRPC_SERVER_SLEEP_SECONDS = 60 * 60 * 24
    GRPC_THREAD_POOLS_MAX_WORKERS = 1024
