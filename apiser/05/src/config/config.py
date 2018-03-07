import os

class Config(object):
    """
    Basic config for proj
    """
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = os.path.dirname(os.path.abspath(__name__))
    DBClient = None
