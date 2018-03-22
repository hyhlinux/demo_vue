#!/usr/bin/env python
import sys
import datetime
import asyncio
import jwt
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


from src.utils import RET, encry_pwd, error_map, new_token
from src.config import CONFIG
from src.model import User

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
    # Client = MongoClient()
    # db = Client['owllook']
    async def post(self, request):
        """
        用户登录
        :param request:
        :return:
        """
        body = await self.user_auth(request)
        return json(body)

    @classmethod
    async def user_auth(cls, request):
        def set_body(status=RET.OK, token=None, uid=None):
            body = dict()
            body['status'] = status
            body['msg'] = error_map.get(status, 'status not found')
            if status == RET.OK:
                # jwt token playload 包含用户信息
                body['token'] = token
                expires = int((datetime.datetime.now() + datetime.timedelta(minutes=1)).timestamp()*1000)
                body['expires'] = expires
                body['user_email'] = request.get('data', {}).get('email', None)
                body['uid'] = uid
            return body

        if not request["data"]:
            return set_body(RET.PARAMERR)
        client_data = request.get("data", {})
        # user_name = data.get('user_name', None)
        # 使用uid来查询.
        user_email = client_data.get('user_email', None)
        password = client_data.get('password', None)
        if not all([user_email, password]):
            # 这种请求，前端不允许提交空数据
            return set_body(RET.PARAMERR)

        # data = self.db.user.find_one({'username': user_name})
        user = User.objects.filter(email=user_email)
        if not user:
            return set_body(RET.USERERR)

        password = encry_pwd(password)
        if password != user.password:
            return set_body(RET.PWDERR)

        payload = dict(user_id=str(user.id))
        token = new_token(payload=payload)
        return set_body(RET.OK, token=token)

    @classmethod
    async def options(cls, request):
        return text("ok")


login_bp.add_route(LoginView.as_view(), '/', methods=['POST', 'OPTIONS'])
