# !/usr/bin/env python
import sys

from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import text

sys.path.append('../')
from src.views import json_bp, html_bp
from src.config import CONFIG

app = Sanic(__name__)
app.blueprint(json_bp)
app.blueprint(html_bp)


# @app.exception(NotFound)
# def ignore_404s(request, exception):
#     return text("Yep, I totally found the page: {}".format(request.url))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT, debug=CONFIG.DEBUG)
