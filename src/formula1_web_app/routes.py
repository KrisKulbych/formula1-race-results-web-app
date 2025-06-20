from http import HTTPStatus

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue
from formula1_race_analysis.display import SortStrategy, filter_report, sort_report

from formula1_web_app.cache_config import cache

main = Blueprint("main", __name__)


@main.route("/")
@cache.cached()
def index() -> ResponseReturnValue:
    return redirect(url_for("main.report"), 301)


@main.route("/report/")
@cache.cached()
def report() -> str:
    race_results = current_app.config["RACE_RESULTS"]
    order = request.args.get("order", SortStrategy.DESCENDING_ORDER)
    try:
        sort_strategy = SortStrategy(order)
    except ValueError:
        sort_strategy = SortStrategy.DESCENDING_ORDER
    sorted_race_results = sort_report(race_results, sort_strategy)
    return render_template("report.html", race_results=sorted_race_results, order=order)


@main.route("/report/drivers")
@cache.cached()
def drivers_list() -> str:
    race_results = current_app.config["RACE_RESULTS"]
    return render_template("drivers.html", race_results=race_results)


@main.route("/report/drivers/<driver_id>")
@cache.cached()
def driver_info(driver_id: str) -> ResponseReturnValue:
    race_results = current_app.config["RACE_RESULTS"]
    filtered_race_results = filter_report(race_results, driver_id)

    if not filtered_race_results:
        return render_template("400.html", driver_id=driver_id), HTTPStatus.BAD_REQUEST

    return render_template("driver_info.html", race_results=filtered_race_results, driver_id=driver_id)
