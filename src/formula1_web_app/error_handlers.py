from http import HTTPStatus

from flask import Flask, request
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def page_not_found_error(error: HTTPException) -> tuple[str, int]:
        message: str = error.description or "No driver found"
        code: int = error.code or HTTPStatus.NOT_FOUND

        if request.path.startswith("/report/drivers/"):
            return message, code
        return "The page is not found", code
