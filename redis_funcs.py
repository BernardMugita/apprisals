import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6381, decode_responses=True)

def redis_set(user, key, value, expire=None):
    if expire:
        r.hset(f'{user}', mapping={f'{key}': f'{value}'})
        r.expire(f'{user}', expire)
    else:
        r.hset(f'{user}', mapping={f'{key}': f'{value}'})

def redis_exists(user, key):
    return r.hexists(user, key)

def redis_del_all(user):
    for key in r.scan_iter(user):
        r.delete(key)

def redis_get(user, key,):
    return r.hget(f'{user}', f'{key}')