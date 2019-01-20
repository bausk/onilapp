from flask_caching import Cache


def get_cache(app):
    return Cache(app.server, config={
        # Note that filesystem cache doesn't work on systems with ephemeral
        # filesystems like Heroku.
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': '/tmp/cache-directory',

        # should be equal to maximum number of users on the app at a single time
        # higher numbers will store more data in the filesystem / redis cache
        'CACHE_THRESHOLD': 200
    })
