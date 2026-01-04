from typing import Annotated

from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse, Response
from formula1_race_analysis.display import SortStrategy, filter_report, sort_report
from formula1_race_analysis.schemas import ID_LENGTH

from formula1_web_app.api.v1.exceptions import DriverNotFoundError, InvalidDriverIdError
from formula1_web_app.api.v1.schemas import DriverListSchema, Format, RaceResultSchema
from formula1_web_app.api.v1.utils import build_api_response, convert_race_results_to_schema_objects
from formula1_web_app.service.data_loader import load_race_results

route = APIRouter()


@route.get(
    "/report/",
    response_model=list[RaceResultSchema],
    summary="Race report",
    description="Returns a full report of the race results.",
)
def get_race_report(
    fmt: Annotated[Format, Query(description="Output format")] = Format.json,
    order: Annotated[SortStrategy, Query(description="Sorting order")] = SortStrategy.ASCENDING_ORDER,
) -> JSONResponse | Response:
    race_results = load_race_results()
    sorted_results = sort_report(race_results, order)
    converted_results = convert_race_results_to_schema_objects(sorted_results)

    return build_api_response(converted_results, fmt)


@route.get(
    "/report/drivers/",
    response_model=list[DriverListSchema],
    summary="List of drivers",
    description="Returns a list of all drivers participating in the race.",
)
def get_drivers_list(
    fmt: Annotated[Format, Query(description="Output format")] = Format.json,
) -> list[RaceResultSchema] | Response:
    race_results = load_race_results()
    driver_list = [DriverListSchema.model_validate(result.driver) for result in race_results]

    return build_api_response(driver_list, fmt)


@route.get(
    "/report/drivers/{driver_id}",
    response_model=list[RaceResultSchema],
    summary="Driver info",
    description="Returns the results of a specific driver by his ID",
)
def get_driver_info(
    driver_id: Annotated[str, Path(..., min_length=3, max_length=3, description="Unique driver ID")],
    fmt: Annotated[Format, Query(description="Output format")] = Format.json,
) -> list[RaceResultSchema] | Response:
    race_results = load_race_results()
    driver_id = driver_id.upper()

    if not driver_id.isalpha() or len(driver_id) != ID_LENGTH:
        raise InvalidDriverIdError(driver_id)

    filtered_results = filter_report(race_results, driver_id)

    if not filtered_results:
        raise DriverNotFoundError(driver_id)

    converted_results = convert_race_results_to_schema_objects(filtered_results)

    return build_api_response(converted_results, fmt)
