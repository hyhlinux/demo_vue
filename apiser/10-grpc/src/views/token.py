#!/usr/bin/env python
import datetime
from sanic import Blueprint
from sanic.response import json, text
from sanic.log import logger
from sanic.views import HTTPMethodView

try:
    from ujson import dumps as json_dumps
except ImportError:
    from json import dumps as json_dumps

from src.utils import RET, encry_pwd, new_token, error_map, new_sec_secret
from src.model import User
# 激活用户
token_bp = Blueprint('token', url_prefix='api/token')


class TokenView(HTTPMethodView):

    async def get(self, request):
        body = await self.user_active(request)
        return json(body)

    async def post(self, request):
        body = await self.user_active(request)
        return json(body)

    @classmethod
    async def user_active(cls, request):
        def set_body(status=RET.OK, token=None, uid=None):
            body = dict()
            body['status'] = status
            body['msg'] = error_map.get(status, 'status not def')
            if status == RET.OK:
                body['token'] = token
                expires = int((datetime.datetime.now() + datetime.timedelta(minutes=1)).timestamp()*1000)
                body['expires'] = expires
                body['user_email'] = request.get('data', {}).get('email', None)
                body['uid'] = uid
            return body

        if not request["data"]:
            return set_body(RET.PARAMERR)

        client_data = request.get("data", {})
        uid = client_data.get("user_info").get("uid", None)
        if not uid:
            # 这种请求，前端不允许提交空数据
            return set_body(RET.PARAMERR)
        # 检查该邮箱是否已经存在
        try:
            user = User.objects.filter(id=uid)[0]
            if user:
                user.active = True
                user.save()
            payload = dict(uid=uid)
            token = new_token(payload, new_sec_secret(uid))
            print("发送激活成功邮件")
            return set_body(RET.OK, token, uid=str(user.id))
        except Exception as e:
            logger.warning(e)
            except_body = set_body(RET.SERVERERR)
            except_body["msg"] = "查无此用户， {} excpetion:{}".format(except_body.get("msg", ""), e)
            return except_body

    @classmethod
    async def options(cls, request):
        return text("ok")

token_bp.add_route(TokenView.as_view(), '/', methods=['GET', 'POST', 'OPTIONS'])
