import os

class Config(object):
    """
    Basic config for proj
    """
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = os.path.dirname(os.path.abspath(__name__))
    DBClient = None
    MONGO_URI = "mongodb://{host}:{port}/{database}".format( database='test', port=27017, host='localhost' )
    # Application config
    DEBUG = False
    VAL_HOST = os.getenv('VAL_HOST', 'true')
    HOST = ['localhost:8000', '0.0.0.0:8000', '127.0.0.1:8001', '0.0.0.0:8001', '127.0.0.1:8002', '0.0.0.0:8002']
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    WEBSITE = dict(
        IS_RUNNING=True,
        TOKEN='',
        AUTHOR_LATEST_COUNT=5,
    )

    # Engine config
    URL_PHONE = 'https://m.baidu.com/s'
    URL_PC = 'http://www.baidu.com/s'
    BAIDU_RN = 15
    SO_URL = "https://www.so.com/s"
    BY_URL = "https://www.bing.com/search"
    DUCKGO_URL = "https://duckduckgo.com/html"
