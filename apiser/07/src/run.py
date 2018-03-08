import sys
from sanic import Sanic
from sanic.response import json

sys.path.append('../')
from src.config import CONFIG
from src.views import contanct_bp
from sanic_mongo import Mongo

app = Sanic()

mongo_uri = "mongodb://{host}:{port}/{database}".format(
    database='test',
    port=27017,
    host='localhost'
)

Mongo.SetConfig(app, test=mongo_uri)
Mongo(app)

app.blueprint(contanct_bp)

@app.route("/")
async def test(request):
    docs = await request.db().user.find().to_list(length=100)
    print(docs)
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT, debug=CONFIG.DEBUG)
