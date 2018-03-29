#### message

#### 站内信方案对比
```
1.https://blog.csdn.net/u012081441/article/details/74337844
2.https://blog.csdn.net/u012081441/article/details/74337844
3.https://blog.csdn.net/yun_yg/article/details/19919421
```

##### 1.model
```python
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
```


##### 2.接口api
```python
站内信，认证通知等
独立服务 API  

查询接口
发送接口
修改接口
删除接口
```
###### 2.0 创建假数据
```sh

```
###### 2.1 find
###### 2.2 insert
###### 2.3 update
###### 2.4 remove->update isDelete True