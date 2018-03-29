
# coding: utf-8

# In[1]:


import datetime
from mongoengine import connect
from mongoengine import *


# In[2]:


connect('test')


# In[ ]:


class MyMessage(Document):  
    """"
    方案一: 站内信，每产生一条，插入一条.
    """
    fromUserId = IntField()
    toUserId = IntField()
    status = IntField()     #0 未读  1 已读
    title = StringField()
    message = StringField()
    isDelete = BooleanField(default=False) # remove 设置为True, 查询时，isDelete=False.
    createAt = DateTimeField(default=datetime.datetime.utcnow)


# In[33]:


# 创建开发者
dev_users = [500+i for i in range(1000000)]


# In[34]:


# 发送给dev_users, 管理员广播
for i in dev_users:
    msg_info = MyMessage(
        fromUserId=0,
        toUserId=i,
        status=0,
        title="管理员-祝贺成为{}开发者".format(i),
        message="欢迎加入APKPURE 开发者团队",
        isDelete=False,
    )
    msg_info.save()


# In[25]:


# 查看当前开发者的未读信息
my_msgs = MyMessage.objects.filter(fromUserId=0, toUserId=508, status=0)
for msg in my_msgs:
    print("from:{} to:{} status:{} title:{}".format(msg.fromUserId, msg.toUserId, msg.status, msg.title))
    msg.status = 1
    msg.save()


# In[15]:


get_ipython().run_line_magic('pinfo', 'MyMessage.objects.filter')

