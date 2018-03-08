#!/usr/bin/env python
import sys
from feedparser import parse
from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer
from sanic import Blueprint
from sanic.response import json
try:
    from ujson import loads as json_loads
except ImportError:
    from json import loads as json_loads

from src.config import CONFIG
from src.utils import auth_params


enable_async = sys.version_info >= (3, 6)

api_bp = Blueprint('rss_api', url_prefix='v1')
api_bp.static('/statics/api_json', CONFIG.BASE_DIR + '/statics/rss_json')


@api_bp.route("/")
async def index(request):
    return json({"msg": "hello api"})


@cached(ttl=1000, cache=RedisCache, key="rss_json", serializer=PickleSerializer(), port=6379, namespace="main")
async def get_rss():
    print('1th, sleep 1')
    import asyncio
    await asyncio.sleep(1)
    url = "http://blog.howie6879.cn/atom.xml"
    feed = parse(url)
    articles = feed['entries']
    data = []
    for article in articles:
        data.append({"title": article["title_detail"]["value"], "link": article["link"]})
    return data


@api_bp.route("/get/rss/<param>")
async def rss_json(request, param):
    if param == 'howie6879':
        result = {}
        data = await get_rss()
        result['info'] = data
        result['status'] = 1
        return json(result)
    else:
        return json({'info': 'http://localhost:8000/v1/get/rss/howie6879'})


@api_bp.route("/post/rss/<param>", methods=['POST'])
@auth_params('name')
async def post_rss_json(request, **kwargs):
    post_data = json_loads(str(request.body, encoding='utf-8'))
    name = post_data.get('name')
    if name == 'howie6879':
        result = {}
        data = await get_rss()
        result['info'] = data
        result['status'] = 1
        return json(result)
    else:
        return json({'info': '参数错误'})
