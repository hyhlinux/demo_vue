import sys
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS

sys.path.append('../')
from src.config import CONFIG
from src.views import contanct_bp

app = Sanic()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.blueprint(contanct_bp)

@app.route("/")
async def test(request):
    docs = await request.db().user.find().to_list(length=100)
    print(docs)
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT, debug=CONFIG.DEBUG)
