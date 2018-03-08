#!/usr/bin/env python
import sys
import asyncio
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint
from sanic.response import html, json
from sanic.views import HTTPMethodView
from aiocache import cached, RedisCache
from aiocache.serializers import JsonSerializer
from pymongo import MongoClient
# from src.database.mongodb import MotorBase

try:
    from ujson import dumps as json_dumps
except ImportError:
    from json import dumps as json_dumps

contanct_bp = Blueprint('contanct', url_prefix='api/contanct')
enable_async = sys.version_info >= (3, 6)


# jinjia2 config
env = Environment(
    loader=PackageLoader('views.contanct',  '../templates/operate'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=enable_async)

async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return html(rendered_template)

class ContantView(HTTPMethodView):
    Client = MongoClient()
    db = Client['owllook']

    async def get(self, request):
        contants = await self.get_contanct()
        return json(contants)

    async def post(self, request):
        doc = request.json
        self.db.user.save(doc)
        return json({"_id": "{}".format(doc.get('_id', -1))})

    @cached(ttl=1000, cache=RedisCache, key="contanct", serializer=JsonSerializer(), port=6379, namespace="main")
    async def get_contanct(self):
        await asyncio.sleep(1)
        # 通过查询
        docs = self.db.user.find({},{"_id":0})
        contants = []
        for doc in docs:
            contants.append(doc)
        # data = await MotorBase().get_db().user.find().to_list(length=10)
        return contants

contanct_bp.add_route(ContantView.as_view(), '/', methods=['GET', 'POST'])
