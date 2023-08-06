# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from aioredis import Redis
from aioredis.lock import Lock
from aioredis.exceptions import AuthenticationError, ConnectionError, ReadOnlyError, NoPermissionError

from .base import Utils, WeakContextVar, AsyncContextManager, AsyncCirculator
from .event import DistributedEvent
from .ntp import NTPClient
from .transaction import Transaction


REDIS_ERROR_RETRY_COUNT = 0x10
REDIS_POOL_WATER_LEVEL_WARNING_LINE = 0x10


class RedisDelegate:
    """Redis功能组件
    """

    def __init__(self, name=None):

        self._redis_pool = None

        self._name = name if name is not None else Utils.uuid1()[:8]

        self._redis_client_context = WeakContextVar(f'redis_client_{self._name}')

    @property
    def redis_pool(self):

        return self._redis_pool

    async def async_init_redis(self, *args, **kwargs):

        self._redis_pool = RedisClient(*args, **kwargs)

        await self._redis_pool.initialize()

    async def async_close_redis(self):

        if self._redis_pool is not None:
            await self._redis_pool.close()
            self._redis_pool = None

    async def redis_health(self):

        result = False

        async with self.get_cache_client() as cache:
            result = bool(await cache.time())

        return result

    def get_cache_client(self, *, alone=False):

        client = None

        if alone:

            client = self._redis_pool.client()

        else:

            client = self._redis_client_context.get()

            if client is None:

                client = self._redis_pool.client()

                if client:
                    self._redis_client_context.set(client)

            else:

                Utils.log.debug(r'Share redis client in context')

        return client

    def allocate_lock(self, name, timeout, sleep=0.1, blocking=True, blocking_timeout=None, thread_local=True):

        return MLock(self._redis_pool, name, timeout, sleep, blocking, blocking_timeout, thread_local)

    def share_cache(self, name):

        return ShareCache(self._redis_pool, name)

    def event_dispatcher(self, channel_name, channel_count):

        return DistributedEvent(self._redis_pool, channel_name, channel_count)

    def period_counter(self, time_slice: int, key_prefix: str = r'', ntp_client: NTPClient = None):

        return PeriodCounter(self._redis_pool, time_slice, key_prefix, ntp_client)


class RedisClient(Redis):
    """Redis客户端对象，使用with进行上下文管理

    将连接委托给客户端对象管理，提高了整体连接的使用率

    """

    def __init__(
            self, *, host=r'localhost', port=6379, password=None, max_connections=None,
            db_base=0, default_expire=3600, key_prefix=None,
            **kwargs):

        kwargs.update(
            {
                r'host': host,
                r'port': port,
                r'db': db_base,
                r'password': password,
                r'max_connections': max_connections,
            }
        )

        super().__init__(**kwargs)

        self._default_expire = default_expire

        self._key_prefix = key_prefix

        self._auto_release = False

    def set_auto_release(self, val):

        self._auto_release = val

    async def execute_command(self, *args, **kwargs):

        global REDIS_ERROR_RETRY_COUNT

        result = None

        async for times in AsyncCirculator(max_times=REDIS_ERROR_RETRY_COUNT):

            try:

                result = await super().execute_command(*args, **kwargs)

            except (AuthenticationError, ConnectionError, ReadOnlyError, NoPermissionError) as err:

                await self.close()

                raise err

            except Exception as err:

                await self.close()

                if times < REDIS_ERROR_RETRY_COUNT:
                    Utils.log.exception(err)
                else:
                    raise err

            else:

                if self._auto_release and not self.in_pubsub and not self.in_transaction:
                    await self.close()

                break

        return result

    @staticmethod
    def _list_basestring(_list):

        return [Utils.basestring(i) for i in _list]

    @staticmethod
    def _val_encode(val):

        return Utils.pickle_dumps(val)

    @staticmethod
    def _val_decode(val):

        return Utils.pickle_loads(val)

    def _list_decode(self, _list):

        return map(
            lambda i: self._val_decode(i) if i else i,
            _list
        )

    def get_key(self, name, *args, **kwargs):

        if self._key_prefix:
            name = f'{self._key_prefix}:{name}'

        if not args and not kwargs:
            return name

        sign = Utils.params_sign(*args, **kwargs)

        return f'{name}:{sign}'

    # GENERIC COMMANDS

    async def delete(self, *names):

        _names = []

        for _name in names:

            if _name.find(r'*') < 0:
                _names.append(_name)
            else:
                _names.extend((await self.keys(_name)))

        result = (await super().delete(*_names)) if len(_names) > 0 else 0

        return result

    def ori_delete(self, key, *keys):

        return super().delete(key, *keys)

    async def keys(self, pattern):

        result = await super().keys(pattern)

        if result is not None:
            result = self._list_basestring(result)

        return result

    def ori_keys(self, pattern):

        return super().keys(pattern)

    async def randomkey(self):

        result = await super().randomkey()

        if result is not None:
            result = Utils.basestring(result)

        return result

    def ori_randomkey(self):

        return super().randomkey()

    async def scan(self, cursor=0, match=None, count=None, _type=None):

        result = await super().scan(cursor, match, count, _type)

        if result is not None:
            result = (result[0], self._list_basestring(result[1]))

        return result

    def ori_scan(self, cursor=0, match=None, count=None, _type=None):

        return super().scan(cursor, match, count, _type)

    # STRING COMMANDS

    async def get(self, key):

        result = await super().get(key)

        if result is not None:
            result = self._val_decode(result)

        return result

    def ori_get(self, key):

        return super().get(key)

    async def getset(self, key, value):

        _value = self._val_encode(value)

        result = await super().getset(key, _value)

        if result is not None:
            result = self._val_decode(result)

        return result

    def ori_getset(self, key, value):

        return super().getset(key, value)

    async def mget(self, keys, *args):

        result = await super().mget(keys, *args)

        if result is not None:
            result = list(self._list_decode(result))

        return result

    def ori_mget(self, keys, *args):

        return super().mget(keys, *args)

    async def set(self, name, value, ex=None, px=None, nx=False, xx=False, keepttl=False):

        _value = self._val_encode(value)
        _expire = self._default_expire if ex is None else ex

        result = await super().set(name, _value, _expire, px, nx, xx, keepttl)

        return result

    def ori_set(self, name, value, ex=None, px=None, nx=False, xx=False, keepttl=False):

        return super().set(name, value, ex, px, nx, xx, keepttl)

    async def mset(self, mapping):

        for _key, _val in mapping:
            mapping[_key] = self._val_encode(_val)

        result = await super().mset(mapping)

        return result

    def ori_mset(self, mapping):

        return super().mset(mapping)

    async def msetnx(self, mapping):

        for _key, _val in mapping:
            mapping[_key] = self._val_encode(_val)

        result = await super().msetnx(mapping)

        return result

    def ori_msetnx(self, mapping):

        return super().msetnx(mapping)

    async def psetex(self, name, time_ms, value):

        _value = self._val_encode(value)

        result = await super().psetex(name, time_ms, _value)

        return result

    def ori_psetex(self, name, time_ms, value):

        return super().psetex(name, time_ms, value)

    async def setex(self, name, time, value):

        _value = self._val_encode(value)

        result = await super().setex(name, time, _value)

        return result

    def ori_setex(self, name, time, value):

        return super().setex(name, time, value)

    async def setnx(self, name, value):

        _value = self._val_encode(value)

        result = await super().setnx(name, _value)

        return result

    def ori_setnx(self, name, value):

        return super().setnx(name, value)

    # SET COMMANDS

    async def sdiff(self, keys, *args):

        result = await super().sdiff(keys, *args)

        if result is not None:
            result = self._list_basestring(result)

        return result

    def ori_sdiff(self, keys, *args):

        return super().sdiff(keys, *args)

    async def sinter(self, keys, *args):

        result = await super().sinter(keys, *args)

        if result is not None:
            result = self._list_basestring(result)

        return result

    def ori_sinter(self, keys, *args):

        return super().sinter(keys, *args)

    async def smembers(self, name):

        result = await super().smembers(name)

        if result is not None:
            result = self._list_basestring(result)

        return result

    def ori_smembers(self, name):

        return super().smembers(name)

    async def spop(self, name, count=None):

        result = await super().spop(name, count)

        if result is not None:
            result = Utils.basestring(result)

        return result

    def ori_spop(self, name, count=None):

        return super().spop(name, count)

    async def srandmember(self, name, number=None):

        result = await super().srandmember(name, number)

        if result is not None:
            result = self._list_basestring(result)

        return result

    def ori_srandmember(self, name, number=None):

        return super().srandmember(name, number)

    async def sunion(self, keys, *args):

        result = await super().sunion(keys, *args)

        if result is not None:
            result = self._list_basestring(result)

        return result

    def ori_sunion(self, keys, *args):

        return super().sunion(keys, *args)

    async def sscan(self, name, cursor=0, match=None, count=None):

        result = await super().sscan(name, cursor, match, count)

        if result is not None:
            result = (result[0], self._list_basestring(result[1]))

        return result

    def ori_sscan(self, name, cursor=0, match=None, count=None):

        return super().sscan(name, cursor, match, count)

    # HASH COMMANDS

    async def hget(self, name, key):

        result = await super().hget(name, key)

        if result is not None:
            result = self._val_decode(result)

        return result

    def ori_hget(self, name, key):

        return super().hget(name, key)

    async def hgetall(self, name):

        result = await super().hgetall(name)

        if result is not None:
            result = {Utils.basestring(key): self._val_decode(val) for key, val in result.items()}

        return result

    def ori_hgetall(self, name):

        return super().hgetall(name)

    async def hkeys(self, name):

        result = await super().hkeys(name)

        if result is not None:
            result = self._list_basestring(result)

        return result

    def ori_hkeys(self, name):

        return super().hkeys(name)

    async def hmget(self, name, keys, *args):

        result = await super().hmget(name, keys, *args)

        if result is not None:
            result = list(self._list_decode(result))

        return result

    def ori_hmget(self, name, keys, *args):

        return super().hmget(name, keys, *args)

    async def hset(self, name, key=None, value=None, mapping=None):

        _value = self._val_encode(value)

        result = await super().hset(name, key, _value, mapping)

        return result

    def ori_hset(self, name, key=None, value=None, mapping=None):

        return super().hset(name, key, value, mapping)

    async def hsetnx(self, name, key, value):

        _value = self._val_encode(value)

        result = await super().hsetnx(name, key, _value)

        return result

    def ori_hsetnx(self, name, key, value):

        return super().hsetnx(name, key, value)

    async def hvals(self, name):

        result = await super().hvals(name)

        if result is not None:
            result = list(self._list_decode(result))

        return result

    def ori_hvals(self, name):

        return super().hvals(name)

    async def hscan(self, name, cursor=0, match=None, count=None):

        result = await super().hscan(name, cursor, match, count)

        if result is not None:
            result = (result[0], [(Utils.basestring(key), self._val_decode(val), ) for key, val in result[1]])

        return result

    def ori_hscan(self, name, cursor=0, match=None, count=None):

        return super().hscan(name, cursor, match, count)

    # LIST COMMANDS

    async def blpop(self, keys, timeout=0):

        result = await super().blpop(keys, timeout)

        if result is not None:
            result = self._val_decode(result[1])

        return result

    def ori_blpop(self, keys, timeout=0):

        return super().blpop(keys, timeout)

    async def brpop(self, keys, timeout=0):

        result = await super().brpop(keys, timeout)

        if result is not None:
            result = self._val_decode(result[1])

        return result

    def ori_brpop(self, keys, timeout=0):

        return super().brpop(keys, timeout)

    async def brpoplpush(self, src, dst, timeout=0):

        result = await super().brpoplpush(src, dst, timeout)

        if result is not None:
            result = self._val_decode(result)

        return result

    def ori_brpoplpush(self, src, dst, timeout=0):

        return super().brpoplpush(src, dst, timeout)

    async def lindex(self, name, index):

        result = await super().lindex(name, index)

        if result is not None:
            result = self._val_decode(result)

        return result

    def ori_lindex(self, name, index):

        return super().lindex(name, index)

    async def linsert(self, name, where, refvalue, value):

        _value = self._val_encode(value)

        result = await super().linsert(name, where, refvalue, _value)

        return result

    def ori_linsert(self, name, where, refvalue, value):

        return super().linsert(name, where, refvalue, value)

    async def lpop(self, name):

        result = await super().lpop(name)

        if result is not None:
            result = self._val_decode(result)

        return result

    def ori_lpop(self, name):

        return super().lpop(name)

    async def lpush(self, name, *values):

        _values = [self._val_encode(val) for val in values]

        result = await super().lpush(name, *_values)

        return result

    def ori_lpush(self, name, *values):

        return super().lpush(name, *values)

    async def lpushx(self, key, value):

        _value = self._val_encode(value)

        result = await super().lpushx(key, _value)

        return result

    def ori_lpushx(self, key, value):

        return super().lpushx(key, value)

    async def lrange(self, name, start, end):

        result = await super().lrange(name, start, end)

        if result is not None:
            result = list(self._list_decode(result))

        return result

    def ori_lrange(self, name, start, end):

        return super().lrange(name, start, end)

    async def lrem(self, name, count, value):

        _value = self._val_encode(value)

        result = await super().lrem(name, count, _value)

        return result

    def ori_lrem(self, name, count, value):

        return super().lrem(name, count, value)

    async def lset(self, name, index, value):

        _value = self._val_encode(value)

        result = await super().lset(name, index, _value)

        return result

    def ori_lset(self, name, index, value):

        return super().lset(name, index, value)

    async def rpop(self, name):

        result = await super().rpop(name)

        if result is not None:
            result = self._val_decode(result)

        return result

    def ori_rpop(self, name):

        return super().rpop(self, name)

    async def rpoplpush(self, src, dst):

        result = await super().rpoplpush(src, dst)

        if result is not None:
            result = self._val_decode(result)

        return result

    def ori_rpoplpush(self, src, dst):

        return super().rpoplpush(src, dst)

    async def rpush(self, name, *values):

        _values = [self._val_encode(val) for val in values]

        result = await super().rpush(name, *_values)

        return result

    def ori_rpush(self, name, *values):

        return super().rpush(name, *values)

    async def rpushx(self, name, value):

        _value = self._val_encode(value)

        result = await super().rpushx(name, _value)

        return result

    def ori_rpushx(self, name, value):

        return super().rpushx(name, value)


class MLock(AsyncContextManager):
    """基于Redis实现的分布式锁，使用with进行上下文管理
    """

    def __init__(self, redis_pool, name, timeout, sleep=0.1, blocking=True, blocking_timeout=None, thread_local=True):

        self._lock = Lock(redis_pool.client(), name, timeout, sleep, blocking, blocking_timeout, thread_local)

    async def locked(self):

        return self._lock.locked()

    async def _context_release(self):

        await self.release()

    async def acquire(self, blocking=None, blocking_timeout=None, token=None):

        await self._lock.acquire(blocking, blocking_timeout, token)

    async def extend(self, additional_time, replace_ttl=False):

        return self._lock.extend(additional_time, replace_ttl)

    async def wait(self, timeout=0):

        resp = await self.acquire(True, timeout)

        if resp:
            await self.release()
            return True
        else:
            return False

    async def release(self):

        self._lock.release()


class ShareCache(AsyncContextManager):
    """共享缓存，使用with进行上下文管理

    基于分布式锁实现的一个缓存共享逻辑，保证在分布式环境下，同一时刻业务逻辑只执行一次，其运行结果会通过缓存被共享

    """

    def __init__(self, redis_pool, name):

        self._redis_pool = redis_pool
        self._name = name

        self._locker = None
        self._locked = False

        self.result = None

    async def _context_release(self):

        await self.release()

    async def get(self):

        result = await self._redis_pool.get(self._name)

        if result is None:

            self._locker = self._redis_pool.allocate_lock(self._name)
            self._locked = await self._locker.acquire()

            if not self._locked:
                await self._locker.wait()
                result = await self._redis_pool.get(self._name)

        return result

    async def set(self, value, expire=0):

        result = await self._redis_pool.set(self._name, value, expire)

        return result

    async def release(self):

        if self._locked:

            self._locked = False

            if self._locker:
                await self._locker.release()

        self._redis_pool = self._locker = None


class PeriodCounter:

    MIN_EXPIRE = 60

    def __init__(self, redis_pool: RedisClient, time_slice: int, key_prefix: str = r'', ntp_client: NTPClient = None):

        self._redis_pool = redis_pool

        self._time_slice = time_slice
        self._key_prefix = key_prefix

        self._ntp_client = ntp_client

    def _get_key(self, key: str = None) -> str:

        timestamp = Utils.timestamp() if self._ntp_client is None else self._ntp_client.timestamp

        time_period = Utils.math.floor(timestamp / self._time_slice)

        if key is None:
            return f'{self._key_prefix}:{time_period}'
        else:
            return f'{self._key_prefix}:{key}:{time_period}'

    async def _incr(self, key: int, val: str) -> int:

        res = None

        async with self._redis_pool.get_client() as cache:
            pipeline = cache.pipeline()
            pipeline.incrby(key, val)
            pipeline.expire(key, max(self._time_slice, self.MIN_EXPIRE))
            res, _ = await pipeline.execute()

        return res

    async def _decr(self, key: int, val: str) -> int:

        res = None

        async with self._redis_pool.get_client() as cache:
            pipeline = cache.pipeline()
            pipeline.decrby(key, val)
            pipeline.expire(key, max(self._time_slice, self.MIN_EXPIRE))
            res, _ = await pipeline.execute()

        return res

    async def incr(self, val: int, key: str = None):

        _key = self._get_key(key)

        res = await self._incr(_key, val)

        return res

    async def incr_with_trx(self, val: int, key: str = None) -> (int, Transaction):

        _key = self._get_key(key)

        res = await self._incr(_key, val)

        if res is not None:
            trx = Transaction()
            trx.add_rollback_callback(self._decr, _key, val)
        else:
            trx = None

        return res, trx

    async def decr(self, val: int, key: str = None) -> int:

        _key = self._get_key(key)

        res = await self._decr(_key, val)

        return res

    async def decr_with_trx(self, val: int, key: str = None) -> (int, Transaction):

        _key = self._get_key(key)

        res = await self._decr(_key, val)

        if res is not None:
            trx = Transaction()
            trx.add_rollback_callback(self._incr, _key, val)
        else:
            trx = None

        return res, trx
