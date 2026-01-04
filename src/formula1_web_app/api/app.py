import uvicorn
from fastapi import FastAPI

from formula1_web_app.api.v1.endpoints import route
from formula1_web_app.api.v1.exception_handlers import handle_driver_not_found, handle_invalid_driver_id
from formula1_web_app.api.v1.exceptions import DriverNotFoundError, InvalidDriverIdError
from formula1_web_app.api.v1.root import root_router

api = FastAPI(title="Formula 1 Race Results API", version="v1")


api.include_router(root_router)
api.include_router(route, prefix="/api/v1")
api.add_exception_handler(DriverNotFoundError, handle_driver_not_found)
api.add_exception_handler(InvalidDriverIdError, handle_invalid_driver_id)


def run() -> None:
    uvicorn.run("formula1_web_app.api.app:api", port=8000, reload=True)


if __name__ == "__main__":
    run()
