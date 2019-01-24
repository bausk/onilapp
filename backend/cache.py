import os
from flask_caching import Cache


def get_cache(app):

    CACHE_CONFIG = {
        # try 'filesystem' if you don't want to setup redis
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.environ.get('REDIS_HOST', 'localhost:6379'),
        'CACHE_THRESHOLD': 200
    }
    config = {
        # Note that filesystem cache doesn't work on systems with ephemeral
        # filesystems like Heroku.
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': '/tmp/cache-directory',

        # should be equal to maximum number of users on the app at a single time
        # higher numbers will store more data in the filesystem / redis cache
        'CACHE_THRESHOLD': 200
    }
    return Cache(app.server, config=CACHE_CONFIG)
