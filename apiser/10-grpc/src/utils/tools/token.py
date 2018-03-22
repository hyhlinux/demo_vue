import time
import json
import sys
import base64
import hashlib
import jwt
import datetime
try:
    from src.config import CONFIG
except ImportError:
    class CONFIG:
        WEBSITE = dict(
            TOKEN='owllook',
        )
        JWT = {
            "playload_sec": False,
            "salt": "+-*/.",
            "sercret": 'tplinux',
            "payload_pre": "++",
            "payload_end": "--",
            "exp": 30,
            "algorithm": 'HS256'
        }

PY3 = sys.version_info[0] == 3


if PY3:
    text_type = str
    binary_type = bytes
else:
    text_type = unicode
    binary_type = str

def encry_pwd(pwd=""):
    new_pwd = hashlib.md5((CONFIG.WEBSITE["TOKEN"] + pwd).encode("utf-8")).hexdigest()
    return new_pwd


def check_token(token=None, key=None):
    if not token:
        return False, dict(msg="token can't be empty")
    try:
        data = jwt.decode(token,
                key=key,
                algorithms=CONFIG.JWT.get('algorithm', 'HS256'))
        if CONFIG.JWT.get("playload_sec", False):
            return True, json.loads(data.get("payload", "{}"))
        return True, data
    except jwt.ExpiredSignatureError as e:
        return False, dict(msg="{}".format(e))
    except jwt.DecodeError as e:
        return False, dict(msg="jwt.DecodeError {}".format(e))

def payload_encode(input):
    # todo jwe 实现payload 加密
    return base64.urlsafe_b64encode(input).replace(b'=', b'')

def payload_decode(input):
    # todo jwe 实现payload 解密
    # payload["payload"] 是加密信息，需要
    return base64.urlsafe_b64decode(input)


def new_sec_secret(uid):
    """
    生成jwt编/解密key的规则.

    :param: uid 不同的用户不同
    :return: key 针对用户生成唯一的key, 单向加密
    """
    salt_pre = CONFIG.JWT.get('sercret', 'tplinux'),
    key = "{pre}{salt}{uid}".format(pre=salt_pre,
                                    salt=CONFIG.JWT.get("salt", "+-*/."), uid=uid)
    # 也可以不md5
    # return encry_pwd(key)
    return key

def new_token(payload={}, key=None):
    sec_payload = dict()
    if CONFIG.JWT.get("playload_sec", False):
        # todo payload 加密
        sec_payload["payload"] = json.dumps(payload)
    else:
       sec_payload = payload
    if isinstance(sec_payload, dict) and not sec_payload.get('exp', None):
        expires = datetime.datetime.now() + datetime.timedelta(minutes=CONFIG.JWT.get("exp", 5))
        # jwt 解码需要s
        expires = int(expires.timestamp())
        sec_payload['exp'] = expires

    return jwt.encode(
        payload=sec_payload,
        key=key,
        algorithm=CONFIG.JWT.get('algorithm', 'HS256')
    )


def main():
    expires = datetime.datetime.now() + datetime.timedelta(seconds=3)
    # expires = int(expires.timestamp()*1000) #前端需要
    # jwt 解码需要s
    # expires = int(expires.timestamp())
    uid = "123456"
    payload = dict(
    #     exp=expires,
        uid=uid,
    )
    key = new_sec_secret(uid)
    token = new_token(payload=payload, key=key)
    time.sleep(2)
    check, user_info = check_token(token=token, key=key)
    print(check, user_info)

if __name__ == '__main__':
    main()
