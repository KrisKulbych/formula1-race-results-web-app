from formula1_race_analysis import RaceResult, build_q1_report

from formula1_web_app.settings import settings


def load_race_results() -> list[RaceResult]:
    return build_q1_report(settings.base_dir, settings.ignore_errors)
