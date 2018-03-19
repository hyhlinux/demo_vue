import sys
import jwt
from sanic import Sanic
from sanic.response import json
from urllib.parse import parse_qs
from sanic_cors import CORS

from pymongo import MongoClient

sys.path.append('../')
from src.config import CONFIG
from src.views import contanct_bp
from src.views import register_bp
from src.views import login_bp
from src.utils import check_jwt



app = Sanic()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.blueprint(contanct_bp)
app.blueprint(register_bp)
app.blueprint(login_bp)


@app.middleware('request')
async def post_on_request(request):
    """
    处理post 中form与json数据，保存至request['data']
    :param request:
    :return:
    """
    token = request.headers.get('token', '') or request.args.get('token', '')
    check_token, user_info = check_jwt(token)
    if not check_token and request.path not in ('/api/register', '/api/login'):
        return json({}, status=403)

    try:
        user_name = request.json.get('username', '')
        password = request.json.get('password', '')
        user_email = request.json.get('email', '')
        # 头信息获取token
    except Exception as e:
        form_data = parse_qs(str(request.body, encoding='utf-8'))
        user_name = form_data.get('username', [None])[0]
        password = form_data.get('password', [None])[0]
        user_email = form_data.get('email', [None])[0]
    finally:
        request["data"] = dict(
            user_name=user_name,
            password=password,
            user_info=user_info,
            user_email=user_email)
    print("I print when a request is received by the server:", request["data"])

@app.middleware('response')
async def print_on_response(request, response):
    print("I print when a response is returned by the server", response)

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started!')

@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down!')


@app.route("/")
async def test(request):
    docs = await request.db().user.find().to_list(length=100)
    print(docs)
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT, debug=CONFIG.DEBUG)
