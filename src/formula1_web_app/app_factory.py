from flask import Flask
from formula1_race_analysis import build_q1_report

from formula1_web_app.cache_config import init_cache
from formula1_web_app.error_handlers import register_error_handlers
from formula1_web_app.routes import main
from formula1_web_app.settings import settings


def create_app() -> Flask:
    app = Flask(__name__)

    init_cache(app)
    register_error_handlers(app)

    app.register_blueprint(main)

    app.config["RACE_RESULTS"] = build_q1_report(settings.base_dir, settings.ignore_errors)

    return app
