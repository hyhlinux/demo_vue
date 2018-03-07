import os
import sys

from sanic import Sanic
from sanic.response import json, text, html
from sanic.exceptions import NotFound
from sanic import Blueprint
from feedparser import parse
from jinja2 import Environment, PackageLoader, select_autoescape

from src.config import CONFIG

# https://github.com/channelcat/sanic/blob/5bb640ca1706a42a012109dc3d811925d7453217/examples/jinja_example/jinja_example.py
# 开启异步特性  要求3.6+
enable_async = sys.version_info >= (3, 6)

html_bp = Blueprint("rss_html", url_prefix='html')
current_directory = os.path.dirname(os.path.abspath(__name__))
# app.static('/statics', os.path.join(current_directory, 'statics'))
html_bp.static('/statics', os.path.join(CONFIG.BASE_DIR, './statics/rss_html'))

# jinjia2 config
env = Environment(
    loader=PackageLoader('views.rss_json',  '../templates/rss_html'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=enable_async)


async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return html(rendered_template)



@html_bp.route("/")
async def index(request):
    return await template('index.html', title="html")


@html_bp.route("/index")
async def rss_html(request):
    url = "http://blog.howie6879.cn/atom.xml"
    feed = parse(url)
    articles = feed['entries']
    data = []
    for article in articles:
        data.append({
            "title": article["title_detail"]["value"],
            "link": article["link"],
            "published": article["published"]
        })
    return await template('rss.html', articles=data, static='/html/statics')
