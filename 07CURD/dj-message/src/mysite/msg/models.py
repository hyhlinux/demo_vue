from django.db import models
import datetime

# Create your models here.
class Message(models.Model):
    fromUserId = models.CharField(max_length=60)
    toUserId = models.CharField(max_length=60)
    status = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    Text = models.CharField(max_length=1000)
    isDelete = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title
