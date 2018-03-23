import sys
import jwt
from sanic import Sanic
from sanic.log import logger
from sanic.response import json
from urllib.parse import parse_qs
from sanic_cors import CORS

from pymongo import MongoClient

sys.path.append('../')
from src.config import CONFIG
from src.utils import check_token, new_sec_secret
from src.views import register_bp
from src.views import login_bp, token_bp

app = Sanic()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.blueprint(register_bp)
app.blueprint(login_bp)
app.blueprint(token_bp)
 # Client = MongoClient()
 # db = Client['owllook']
app.db = dict(
    mongo=MongoClient()['sanic']
)

@app.middleware('request')
async def post_on_request(request):
    """
    处理post 中form与json数据，保存至request['data']
    :param request:
    :return:
    """
    user_info = None
    if request.path not in CONFIG.WHITE_PATH:
        token = request.headers.get('token', '') or request.args.get('token', '')
        # uid 每一个用户不同，保证jwt的secret均不同，保证安全性.
        uid = request.headers.get('uid', '') or request.args.get('uid', '')
        check, user_info = check_token(token, key=new_sec_secret(uid))
        if not check:
            return json(user_info, status=403)
    else:
        pass

    try:
        user_name = request.json.get('username', '')
        password = request.json.get('password', '')
        user_email = request.json.get('email', '')
        phone = request.json.get('phone', '')
        # 头信息获取token
    except Exception as e:
        logger.warning("Not Json {}".format(e))
        form_data = parse_qs(str(request.body, encoding='utf-8'))
        # form_data = request.parsed_form
        # todo instead  username by email
        user_name = form_data.get('username', [None])[0]
        password = form_data.get('password', [None])[0]
        user_email = form_data.get('email', [None])[0]
        phone = form_data.get('phone', [None])[0]
    finally:
        request["data"] = dict(
            user_name=user_name,
            password=password,
            user_info=user_info,
            phone=phone,
            email=user_email
        )
    logger.debug("I print when a request is received by the server:{} {}".format(request["data"], id(request.app)))

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    logger.debug('Server successfully started!')

@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    logger.error('Server shutting down!')


@app.route("/")
async def test(request):
    docs = await request.db().user.find().to_list(length=100)
    print(docs)
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT, debug=CONFIG.DEBUG)
