import time
import json
import asyncio
from redis.asyncio import Redis
from config import redis_config

r = Redis(
    host=redis_config.REDIS_HOST,
    port=redis_config.REDIS_PORT,
    password=redis_config.REDIS_PASSWORD,
    decode_responses=True
)



async def refresh_cache(key, fetch_fn, *args, **kwargs):
    if not await r.set(key + ":lock", "1", nx=True, ex=60):
        return

    data = await fetch_fn(*args, **kwargs)

    await r.set(key, json.dumps(data))
    await r.set(key + ":ts", time.time())


def make_cache_key(fn, args, kwargs):
    name = fn.__name__
    params = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    return f"{name}:{params}"


async def get_data_with_cache(fetch_fn, *args, **kwargs):
    try:
        key = make_cache_key(fetch_fn, args, kwargs)
        data = await r.get(key)
        ts = await r.get(key + ":ts")

        if not data or not ts:
            fresh = await fetch_fn(*args, **kwargs)
            await r.set(key, json.dumps(fresh))
            await r.set(key + ":ts", time.time())
            return fresh

        age = time.time() - float(ts)

        if age < redis_config.MAIN_TTL:
            return json.loads(data)
        asyncio.create_task(refresh_cache(key, fetch_fn, *args, **kwargs))
        return json.loads(data)
        
    except:
        data = await fetch_fn(*args, **kwargs)
        return data

