import sys
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
from sanic_openapi import swagger_blueprint, openapi_blueprint

sys.path.append('../')
from src.config import CONFIG
from src.views import car_bp
# from src.views import driver_bp
# from src.views import garage_bp
# from src.views import manufacturer_bp

app = Sanic()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)
app.blueprint(car_bp)
# app.blueprint(register_bp)
# app.blueprint(login_bp)


# @app.route("/")
# async def test(request):
#     docs = await request.db().user.find().to_list(length=100)
#     print(docs)
#     return json({"hello": "world"})

app.config.API_VERSION = '1.0.0'
app.config.API_TITLE = 'Website API'
app.config.API_TERMS_OF_SERVICE = 'Use with caution!'
app.config.API_CONTACT_EMAIL = 'channelcat@gmail.com'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT, debug=CONFIG.DEBUG)
