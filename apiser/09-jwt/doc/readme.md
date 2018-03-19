#### jwt 认证

### token 存放在header/url_args中

```python
    token = request.headers.get('token', '') or request.args.get('token', '')
    check_token, user_info = check_jwt(token)
    if not check_token and request.path not in ('/api/register', '/api/login'):
        return json({}, status=403)
```
