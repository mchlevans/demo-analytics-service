from os import environ
from flask_caching import Cache

# environment-dependent caching configuration
config = {}
if (environ['ENV'] == 'local'):
    config = {
        'CACHE_TYPE': 'SimpleCache'
    }
else:
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_THRESHOLD': 300,
        'CACHE_DIR': '/flaskCache/'
    }

cache = Cache(config = config)
