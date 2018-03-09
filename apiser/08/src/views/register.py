#!/usr/bin/env python
import sys
import asyncio
from jinja2 import Environment, PackageLoader, select_autoescape
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

register_bp = Blueprint('register', url_prefix='api/register')
enable_async = sys.version_info >= (3, 6)


# jinjia2 config
env = Environment(
    loader=PackageLoader('views.register',  '../templates/register'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=enable_async)

async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return html(rendered_template)


class RegisterView(HTTPMethodView):
    Client = MongoClient()
    db = Client['owllook']

    async def get(self, request):
        # contants = await self.get_contanct()
        # return json(contants)
        return text('请去注册')

    async def post(self, request):
        doc = request.json
        if not doc:
            return json({"msg": "请求数据为空"}, status=400)

        new_user = {
            "email": doc.get('email', ''),
            "username": doc.get('username', ''),
            "password": doc.get('password', ''), #todo hash
        }
        self.db.user.save(new_user)
        return json({"_id": "{}".format(new_user.get('_id', -1))})

    async def options(self, request):
        return text("ok")

register_bp.add_route(RegisterView.as_view(), '/', methods=['GET', 'POST', 'OPTIONS'])
