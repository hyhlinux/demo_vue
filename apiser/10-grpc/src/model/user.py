from mongoengine import *
from sanic.log import logger

try:
    connect('sanic')
except MongoEngineConnectionError as e:
   logger.error("Model e:{}".format(e))

class User(Document):
    """"
    """
    email = EmailField(unique=True)
    password = StringField()
    phone = StringField()
    active = BooleanField(default=False)
    ## others
