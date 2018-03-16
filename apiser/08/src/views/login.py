#!/usr/bin/env python
import sys
import datetime
import asyncio
from jinja2 import Environment, PackageLoader, select_autoescape
from urllib.parse import parse_qs, unquote
from sanic import Blueprint
from sanic.response import html, json, text
from sanic.views import HTTPMethodView
from pymongo import MongoClient

try:
    from ujson import dumps as json_dumps
except ImportError:
    from json import dumps as json_dumps


from src.utils.tools import encry_pwd
from src.utils import RET, error_map

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
        """
        if not request["data"]:
            return json({'status': RET.PARAMERR, "msg": error_map[RET.PARAMERR]})

        user_name = request.get("data",{}).get('user_name', None)
        password = request.get("data",{}).get('password', None)
        if not all([user_name, password]):
            # 这种请求，前端不允许提交空数据
            return json({'status': RET.PARAMERR, "msg": error_map[RET.PARAMERR]})

        data = self.db.user.find_one({'username': user_name})
        if not data:
            return json({'status': RET.USERERR, "msg": error_map[RET.USERERR]})
        password = encry_pwd(password)
        if password == data.get('password'):
            response = json(
            {
                'status': RET.OK,
                "msg": "用户登陆成功",
                "token": str(data.get("_id")),
                "expires": datetime.datetime.now() + datetime.timedelta(days=30),
                "user_name": user_name
            })
            return response
        else:
            return json({'status': RET.PWDERR, "msg": error_map[RET.PWDERR]})

    async def options(self, request):
        return text("ok")

login_bp.add_route(LoginView.as_view(), '/', methods=['POST', 'OPTIONS'])
