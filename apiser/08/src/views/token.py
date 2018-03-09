#!/usr/bin/env python
import sys
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint
from sanic.response import html, json, text
from sanic.views import HTTPMethodView
from pymongo import MongoClient

try:
    from ujson import dumps as json_dumps
except ImportError:
    from json import dumps as json_dumps

token_bp = Blueprint('token', url_prefix='api/token')
enable_async = sys.version_info >= (3, 6)


# jinjia2 config
env = Environment(
    loader=PackageLoader('views.token',  '../templates/token'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=enable_async)

async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return html(rendered_template)


class TokenView(HTTPMethodView):
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
        login_data = request.json
        print(login_data)
        # login_data = parse_qs(str(request.body, encoding='utf-8'))
        user = login_data.get('user', '')
        pwd = login_data.get('pwd', '')
        if user and pwd:
            data = self.db.user.find_one({'user': user})
            if not data:
                # 先使用email字段
                data = self.db.user.find_one({'email': user})
            if not data:
                return json({'status': -2, "msg": "用户还不存在，请去注册"})
                # pass_first = hashlib.md5((CONFIG.WEBSITE["TOKEN"] + pwd).encode("utf-8")).hexdigest()
                # password = hashlib.md5(pass_first.encode("utf-8")).hexdigest()
            if pwd == data.get('password'):
                response = json({'status': 1, "msg": "用户登陆成功"})
                # 将session_id存于cokies
                # date = datetime.datetime.now()
                # response.cookies['owl_sid'] = request['session'].sid
                # response.cookies['owl_sid']['expires'] = date + datetime.timedelta(days=30)
                # response.cookies['owl_sid']['httponly'] = True
                # 此处设置存于服务器session的user值
                # request['session']['user'] = user
                return response
            else:
                return json({'status': 0, "msg": "用户名或密码错误"})
        else:
            return json({'status': -1, "msg": "用户名或密码不能为空"})

    async def options(self, request):
        return text("ok")

token_bp.add_route(TokenView.as_view(), '/', methods=['GET', 'POST', 'OPTIONS'])
