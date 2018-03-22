#### jwt 鉴权系统
```
https://zhuanlan.zhihu.com/p/28295641
```


#### jwt 验证安全性

##### 1. sign key 每一个用户不同
```py
key = f(salt, uid) # uid 就直接使用用户表中的id， 由数据库维护，且全局唯一.
f: 直接使用hash也可以.
salt: 不变字符串.
uid: 不同的用户不同.
```


##### 2.jwt token 如何失效？

1.邮箱激活时，限定时间过期?
```sh
payload:
{
    "exp": 过期时间戳
}
```

2.由人考虑到，用户idx, 登陆后，觉得无聊注销了账户, token已经下发到cli, ser无法删除, 如何处理?.
```sh
1.token 已经由jwt ser 下发到客户端，用户注册后，客户端可以使用该token, 继续访问服务器api接口.

处理方法:
   api ser:
   step1:
   cli--->req(token, uid)-->ser:

   step2:
                            ser:
                                1. 生成key=f(salt, uid).
                                2. 验证token有效, 访问api接口.

   step2: 修订
                            ser:
                                0. user表中是否有uid对应的用户.
                                    无:无权反问.
                                    有:下一步.
                                1. 生成key=f(salt, uid).
                                2. 验证token有效, 访问api接口.

```

