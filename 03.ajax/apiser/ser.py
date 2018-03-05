from sanic import Sanic
from sanic.response import json, text
from sanic_cors import CORS
from sanic.exceptions import NotFound

from config import CONFIG

app = Sanic()
app.config.from_object(CONFIG)
cors = CORS(app, resources={r"/api/*": {"origins": "192.168.0.96"}})


@app.exception(NotFound)
def ignore_404s(request, exception):
    return text("Yep, I totally found the page: {}--{}".format(request.url, exception),
                status=404)

@app.route("/", methods=['GET'])
async def index(request):
    return json({'hello': 'nihao'})


@app.route("/api/", methods=['GET'])
async def api(request):
    return json({"hello": "world"})

@app.get("/api/customers/")
async def customers_handler_get(request):
    print(request)
    gridColumns = ['customerId', 'companyName', 'contactName', 'phone']
    data = []
    for i in range(2):
        people = dict(
            customerId=i,
            companyName='hk:{}'.format(i),
            contactName='cName:{}'.format(i),
            phone='123'
        )
        data.append(people)
    return json(dict(data=data))

@app.get("/api/customers/<cid:int>")
async def customer_handler_get(request, cid):
    data = []
    return json(dict(cid=cid, data=[]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config['PORT'], debug=app.config['DEBUG'])
