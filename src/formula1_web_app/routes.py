from http import HTTPStatus

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue
from formula1_race_analysis.display import SortStrategy, filter_report, sort_report
from formula1_race_analysis.models import RaceResult
from formula1_race_analysis.schemas import ID_LENGTH

from formula1_web_app.cache_config import cache
from formula1_web_app.service.data_loader import load_race_results

main = Blueprint("main", __name__)


@cache.cached(key_prefix="get_race_results")
def get_race_results() -> list[RaceResult]:
    return load_race_results()


@main.route("/")
def index() -> ResponseReturnValue:
    return redirect(url_for("main.report"), 301)


@main.route("/report/")
def report() -> str:
    race_results = get_race_results()
    order = request.args.get("order", SortStrategy.ASCENDING_ORDER)
    try:
        sort_strategy = SortStrategy(order)
    except ValueError:
        sort_strategy = SortStrategy.ASCENDING_ORDER
    sorted_race_results = sort_report(race_results, sort_strategy)
    return render_template("report.html", race_results=sorted_race_results, order=order)


@main.route("/report/drivers")
def drivers_list() -> str:
    race_results = get_race_results()
    return render_template("drivers.html", race_results=race_results)


@main.route("/report/drivers/<driver_id>")
def driver_info(driver_id: str) -> ResponseReturnValue:
    race_results = get_race_results()
    driver_id = driver_id.upper()

    if not driver_id.isalpha() or len(driver_id) != ID_LENGTH:
        abort(
            HTTPStatus.BAD_REQUEST,
            f"Identifier '{driver_id}' is not recognized. Try to use 3-letter code like 'KRF'.",
        )

    filtered_race_results = filter_report(race_results, driver_id)

    if not filtered_race_results:
        abort(HTTPStatus.NOT_FOUND, f"No driver with ID '{driver_id}' found in race data.")

    return render_template("driver_info.html", race_results=filtered_race_results, driver_id=driver_id)
