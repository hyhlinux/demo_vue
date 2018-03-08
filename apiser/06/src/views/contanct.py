#!/usr/bin/env python
import sys
from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer, JsonSerializer
try:
    from ujson import loads as json_loads
except ImportError:
    from json import loads as json_loads
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint
from sanic.response import html, json
from sanic.views import HTTPMethodView
from urllib.parse import parse_qs, unquote

from src.database.mongodb import MotorBase
from src.fetcher.function import get_time
from src.utils import get_real_answer
from src.config import CONFIG, LOGGER

try:
    from ujson import dumps as json_dumps
except ImportError:
    from json import dumps as json_dumps

contanct_bp = Blueprint('contanct', url_prefix='api/contanct')

# @contanct_bp.listener('before_server_start')
# def setup_db(operate_bp, loop):
#     global motor_base
#     motor_base = MotorBase()


@contanct_bp.listener('after_server_stop')
def close_connection(operate_bp, loop):
    motor_base = None


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

def new_contant(num=10):
    ret = []
    for i in range(num):
        people = {
            'customerId': '{}'.format(i),
            'companyName': 'apk_{}'.format(i),
            'contactName': 'n_{}'.format(i),
            'phone': 'p:{}'.format(i)
        }
        ret.append(people)
    return ret

class ContantView(HTTPMethodView):
    db = MotorBase().get_db()

    async def get(self, request):
        # data = await self.get_contanct()
        data = await self.db.user.find_one()
        return json(data)

    async def post(self, request):
        doc = request.json
        self.db.user.save(doc)
        return json({"code": 0})

    # @cached(ttl=1000, cache=RedisCache, key="contanct", serializer=JsonSerializer(), port=6379, namespace="main")
    async def get_contanct(self):
        print('1th, sleep 1')
        import asyncio
        await asyncio.sleep(1)
        data = await self.db.user.find().to_list()
        if data:
            print(data)
        else:
            data = new_contant()
        print(data)
        return data


contanct_bp.add_route(ContantView.as_view(), '/', methods=['GET', 'POST'])
