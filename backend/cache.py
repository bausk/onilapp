import os
from flask_caching import Cache
from .secrets import get_secret, SECRETS


def get_cache(app):
    redis_url = get_secret(SECRETS.REDIS_HOST)
    if redis_url is not None:
        redis_url = 'redis://' + redis_url + '/0'
        CACHE_CONFIG = {
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_URL': redis_url,
            'CACHE_THRESHOLD': 200
        }
        return Cache(app.server, config=CACHE_CONFIG)
    else:
        CACHE_CONFIG = {
            'CACHE_TYPE': 'filesystem',
            'CACHE_DIR': '/tmp/cache-directory',
            'CACHE_THRESHOLD': 200
        }
        return Cache(app.server, config=CACHE_CONFIG)
