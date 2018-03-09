#!/usr/bin/env python
import sys
import datetime
import asyncio
from jinja2 import Environment, PackageLoader, select_autoescape
from urllib.parse import parse_qs, unquote
from sanic import Blueprint
from sanic.response import html, json, text
from sanic.views import HTTPMethodView
from aiocache import cached, RedisCache
from aiocache.serializers import JsonSerializer
from pymongo import MongoClient

try:
    from ujson import dumps as json_dumps
except ImportError:
    from json import dumps as json_dumps

login_bp = Blueprint('login', url_prefix='api/login')
enable_async = sys.version_info >= (3, 6)


# jinjia2 config
env = Environment(
    loader=PackageLoader('views.register',  '../templates/login'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=enable_async)

async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return html(rendered_template)


class LoginView(HTTPMethodView):
    Client = MongoClient()
    db = Client['owllook']

    # async def get(self, request):
    #     # contants = await self.get_contanct()
    #     # return json(contants)
    #     return text('请去登陆')

    async def post(self, request):
        """
        用户登录
        :param request:
        :return:
        :   -2  用户不存在
        :   -1  用户名或密码不能为空
        :   0   用户名或密码错误
        :   1   登陆成功
        """
        login_data = None
        user_name = None
        password = None
        try:
            login_data = request.json
            user_name = login_data.get('username', '')
            password = login_data.get('password', '')
        except Exception as e:
            login_data = parse_qs(str(request.body, encoding='utf-8'))
            user_name = login_data.get('username', [None])[0]
            password = login_data.get('password', [None])[0]
        finally:
            print(login_data)
        if user_name and password:
            data = self.db.user.find_one({'username': user_name})
            if not data:
                # 先使用email字段
                data = self.db.user.find_one({'email': user_name})
            if not data:
                return json({'status': -2, "msg": "用户还不存在，请去注册"})
                # pass_first = hashlib.md5((CONFIG.WEBSITE["TOKEN"] + pwd).encode("utf-8")).hexdigest()
                # password = hashlib.md5(pass_first.encode("utf-8")).hexdigest()
            if password == data.get('password'):
                response = json({'status': 1, "msg": "用户登陆成功", "access_token": "123", "user_name": user_name})
                return response
            else:
                return json({'status': 0, "msg": "用户名或密码错误"})
        else:
            return json({'status': -1, "msg": "用户名或密码不能为空"})

    async def options(self, request):
        return text("ok")

login_bp.add_route(LoginView.as_view(), '/', methods=['POST', 'OPTIONS'])
