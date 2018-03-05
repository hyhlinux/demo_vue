from sanic import Sanic
from sanic.response import json, text
from sanic_cors import CORS, cross_origin

app = Sanic()
cors = CORS(app, resources={r"/api/*": {"origins": "192.168.0.96"}})

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
    app.run(host="0.0.0.0", port=8000)
