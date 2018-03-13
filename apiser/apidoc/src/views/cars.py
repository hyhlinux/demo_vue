from sanic.blueprints import Blueprint
from sanic.response import json
from sanic_openapi import doc

from src.models import Car, Status, test_car, test_success


car_bp = Blueprint('Car', '/car')


@car_bp.get("/", strict_slashes=True)
@doc.summary("Fetches all cars")
@doc.description("Really gets the job done fetching these cars.  I mean, really, wow.")
@doc.produces([Car])
def car_list(request):
    return json([test_car])


@car_bp.get("/<car_id:int>", strict_slashes=True)
@doc.summary("Fetches a car")
@doc.produces(Car)
def car_get(request, car_id):
    return json(test_car)


@car_bp.put("/<car_id:int>", strict_slashes=True)
@doc.summary("Updates a car")
@doc.consumes(Car, location='body')
@doc.consumes({'AUTHORIZATION': str}, location='header')
@doc.produces(Car)
def car_put(request, car_id):
    return json(test_car)


@car_bp.delete("/<car_id:int>", strict_slashes=True)
@doc.summary("Deletes a car")
@doc.produces(Status)
def car_put(request, car_id):
    return json(test_success)
