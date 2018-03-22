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

from src.model import User
from src.utils import RET, encry_pwd, new_token, error_map, new_sec_secret
from src.grpc_service import SendMail

register_bp = Blueprint('register', url_prefix='api/register')

class RegisterView(HTTPMethodView):

    async def post(self, request):
        body = await self.user_register(request)
        return json(body)

    @classmethod
    async def user_register(cls, request):
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
        user_email = client_data.get('email', None)
        password = client_data.get('password', None)
        phone = client_data.get('phone', None)
        if not all([user_email, password]):
            # 这种请求，前端不允许提交空数据
            return set_body(RET.PARAMERR)
        # 检查该邮箱是否已经存在
        user = User.objects.filter(email=user_email)
        if user:
            return set_body(RET.DATAEXIST)
        user = User(
            email=user_email,
            password=encry_pwd(password),
            phone=phone
        )
        try:
            user.save()
            uid = str(user.id)
            payload = dict(uid=uid)
            token = new_token(payload, new_sec_secret(uid))
            #send
            # ret = await SendMail(to=user_email, body='<a href="www.baidu.com">请激活</a>')
            print("发送激活邮件")
            return set_body(RET.OK, token, uid=str(user.id))
        except Exception as e:
            logger.warning(e)
            except_body = set_body(RET.SERVERERR)
            except_body["msg"] = "{} excpetion:{}".format(except_body.get("msg", ""), e)
            return except_body

    @classmethod
    async def options(cls, request):
        return text("ok")

register_bp.add_route(RegisterView.as_view(), '/', methods=['GET', 'POST', 'OPTIONS'])
