from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

root_router = APIRouter()


@root_router.get("/", summary="Redirect to report", description="Redirect to full report in JSON format by default")
def redirect_to_report(request: Request) -> RedirectResponse:
    url = request.url_for("get_race_report")
    return RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
