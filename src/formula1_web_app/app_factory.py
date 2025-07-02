from flask import Flask

from formula1_web_app.cache_config import init_cache
from formula1_web_app.error_handlers import register_error_handlers
from formula1_web_app.routes import main


def create_app() -> Flask:
    app = Flask(__name__)

    init_cache(app)
    register_error_handlers(app)

    app.register_blueprint(main)
    return app
