from http import HTTPStatus

from flask import Flask
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def page_not_found_error(_: HTTPException) -> tuple[str, int]:
        return ("The page is not found", HTTPStatus.NOT_FOUND)
