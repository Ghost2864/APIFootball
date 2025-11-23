import time
import json
import asyncio
import redis
from config import redis_config

r = redis.Redis(
    host=redis_config.REDIS_HOST,
    port=redis_config.REDIS_PORT,
    password=redis_config.REDIS_PASSWORD,
    decode_responses=True
)


async def refresh_cache(key, fetch_fn, *args, **kwargs):
    if not r.set(key + ":lock", "1", nx=True, ex=60):
        return

    data = await fetch_fn(*args, **kwargs)

    r.set(key, json.dumps(data))
    r.set(key + ":ts", time.time())


def make_cache_key(fn, args, kwargs):
    name = fn.__name__
    params = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    return f"{name}:{params}"


async def get_data_with_cache(fetch_fn, *args, **kwargs):
    key = make_cache_key(fetch_fn, args, kwargs)
    data = r.get(key)
    ts = r.get(key + ":ts")

    if not data or not ts:
        fresh = await fetch_fn(*args, **kwargs)
        r.set(key, json.dumps(fresh))
        r.set(key + ":ts", time.time())
        return fresh

    age = time.time() - float(ts)

    if age < redis_config.MAIN_TTL:
        return json.loads(data)
    asyncio.create_task(refresh_cache(key, fetch_fn, *args, **kwargs))
    return json.loads(data)
