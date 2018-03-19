import time
import jwt
import datetime
try:
    from src.config import CONFIG
except ImportError:
    class CONFIG:
        JWT = {
            "sercret": 'tplinux',
            "algorithm": 'HS256'
        }


def check_jwt(token=None):
    if not token:
        return False, None

    try:
        data = jwt.decode(token, CONFIG.JWT.get('sercret', 'tplinux'),
                algorithms=CONFIG.JWT.get('algorithm', 'HS256'))
        return True, data
    except jwt.ExpiredSignatureError as e:
        print('token获取，请刷新token: {}'.format(e))
        return False, dict(msg="{}".format(e))
    except jwt.DecodeError as e:
        print('token解码失败: {} \ntoken:{}'.format(e, token))
        return False, dict(msg="{}".format(e))


def main():
    expires = datetime.datetime.now() + datetime.timedelta(seconds=1)
    # expires = int(expires.timestamp()*1000) #前端需要
    # jwt 解码需要s
    expires = int(expires.timestamp())
    payload = dict(
        exp=expires,
        user_name="123456",
    )
    token = jwt.encode(payload=payload,
                       key=CONFIG.JWT.get('sercret', 'tplinux'),
                       algorithm=CONFIG.JWT.get('algorithm', 'HS256'))
    time.sleep(2)
    check_token, user_info = check_jwt(token=token)
    print(check_token, user_info)

if __name__ == '__main__':
    main()
