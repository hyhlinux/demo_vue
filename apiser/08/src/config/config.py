import os

class Config(object):
    """
    Basic config for proj
    """
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = os.path.dirname(os.path.abspath(__name__))
    DB_CONF = {
        "mongo": "mongodb://{host}:{port}/{database}".format( database='test', port=27017, host='localhost' )
    }
    # Application config
    DEBUG = False
