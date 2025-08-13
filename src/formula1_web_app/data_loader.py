from formula1_race_analysis import RaceResult, build_q1_report

from formula1_web_app.cache_config import cache
from formula1_web_app.settings import settings


@cache.cached(key_prefix="get_race_results")
def get_race_results() -> list[RaceResult]:
    return build_q1_report(settings.base_dir, settings.ignore_errors)
