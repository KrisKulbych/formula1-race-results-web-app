from datetime import UTC, datetime

from fastapi import Request, status
from fastapi.responses import JSONResponse

from formula1_web_app.api.v1.exceptions import DriverNotFoundError, InvalidDriverIdError


def handle_invalid_driver_id(request: Request, exc: InvalidDriverIdError) -> JSONResponse:
    """Exception handler for invalid driver identifiers."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": f"Identifier '{exc.driver_id}' is not recognized. Try to use 3-letter code like 'KRF'.",
            "request": {
                "method": request.method,
                "path": request.url.path,
            },
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )


def handle_driver_not_found(request: Request, exc: DriverNotFoundError) -> JSONResponse:
    """Exception handler for drivers that are not found in the race results."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": f"No driver with ID '{exc.driver_id}' found in race data.",
            "request": {
                "method": request.method,
                "path": request.url.path,
            },
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )
