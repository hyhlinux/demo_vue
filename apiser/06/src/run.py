# !/usr/bin/env python
import sys
import aiocache

from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import text, redirect, html
from sanic_session import RedisSessionInterface

sys.path.append('../')
from src.views import json_bp, html_bp, api_bp
from src.database.redis import RedisSession
from src.config import LOGGER, CONFIG

app = Sanic(__name__)

@app.listener('before_server_start')
def init_cache(app, loop):
    LOGGER.info("Starting aiocache")
    app.config.from_object(CONFIG)
    REDIS_DICT = CONFIG.REDIS_DICT
    aiocache.settings.set_defaults(
        class_="aiocache.RedisCache",
        endpoint=REDIS_DICT.get('REDIS_ENDPOINT', 'localhost'),
        port=REDIS_DICT.get('REDIS_PORT', 6379),
        db=REDIS_DICT.get('CACHE_DB', 0),
        password=REDIS_DICT.get('REDIS_PASSWORD', None),
        loop=loop,
    )
    LOGGER.info("Starting redis pool")
    redis_session = RedisSession()
    # redis instance for app
    app.get_redis_pool = redis_session.get_redis_pool
    # pass the getter method for the connection pool into the session
    app.session_interface = RedisSessionInterface(
        app.get_redis_pool, cookie_name="owl_sid", expiry=30 * 24 * 60 * 60)

@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    host = request.headers.get('host', None)
    user_agent = request.headers.get('user-agent', None)
    if user_agent:
        if CONFIG.VAL_HOST == 'true':
            if not host or host not in CONFIG.HOST:
                return redirect('http://localhost:8000/')
        if CONFIG.WEBSITE['IS_RUNNING']:
            await app.session_interface.open(request)
        else:
            return html("<h3>网站正在维护...</h3>")
    else:
        return html("<h3>网站正在维护...</h3>")


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    # await app.session_interface.save(request, response)
    if request.path == '/operate/login' and request['session'].get('user', None):
        await app.session_interface.save(request, response)
        import datetime
        response.cookies['owl_sid']['expires'] = datetime.datetime.now(
        ) + datetime.timedelta(days=30)
    elif request.path == '/register':
        try:
            response.cookies['reg_index'] = str(request['session']['index'][0])
        except KeyError:
            pass

app.blueprint(json_bp)
app.blueprint(html_bp)
app.blueprint(api_bp)


# @app.exception(NotFound)
# def ignore_404s(request, exception):
#     return text("Yep, I totally found the page: {}".format(request.url))


@app.route("/")
async def index(request):
    # interact with the session like a normal dict
    if not request['session'].get('foo'):
        request['session']['foo'] = 0

    request['session']['foo'] += 1

    return text(request['session']['foo'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT, debug=CONFIG.DEBUG)
