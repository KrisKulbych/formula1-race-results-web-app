from flask import Flask
from flask_caching import Cache

cache = Cache()


def init_cache(app: Flask) -> None:
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 10

    cache.init_app(app)
