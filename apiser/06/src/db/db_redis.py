#!/usr/bin/env python
import os
import asyncio_redis

REDIS_DICT = dict(
    IS_CACHE=True,
    REDIS_ENDPOINT=os.getenv('REDIS_ENDPOINT', "localhost"),
    REDIS_PORT=os.getenv('REDIS_PORT', 6379),
    REDIS_PASSWORD=os.getenv('REDIS_PASSWORD', None),
    DB=0,
    POOLSIZE=10,
)


class RedisSession:
    """
    建立redis连接池
    """
    _pool = None

    async def get_redis_pool(self):
        if not self._pool:
            self._pool = await asyncio_redis.Pool.create(
                host=str(REDIS_DICT.get('REDIS_ENDPOINT', "localhost")), port=int(REDIS_DICT.get('REDIS_PORT', 6379)),
                poolsize=int(REDIS_DICT.get('POOLSIZE', 10)), password=REDIS_DICT.get('REDIS_PASSWORD', None),
                db=REDIS_DICT.get('DB', None)
            )

        return self._pool


if __name__ == '__main__':
    import asyncio

    redis_session = RedisSession()
    redis_pool = redis_session.get_redis_pool


    async def do_set():
        redis_connection = await redis_pool()
        await redis_connection.set('name', 'name1')
        res = await redis_connection.get('name')
        print("get name: {0}".format(res))
        return res


    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_set())
