from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from formula1_web_app.settings import settings
from main import create_app


@pytest.fixture(scope="session")
def prepare_database(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_path = tmp_path_factory.mktemp("data_root")
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    tmp_abbreviations = data_dir / "abbreviations.txt"
    abbreviations_content = (
        "PGS_Pierre Gasly_SCUDERIA TORO ROSSO HONDA\n"
        "KMH_Kevin Magnussen_HAAS FERRARI\n"
        "FAM_Fernando Alonso_MCLAREN RENAULT\n"
    )
    tmp_abbreviations.write_text(abbreviations_content)

    tmp_start_log = data_dir / "start.log"
    start_log_content = "FAM2018-05-24_12:13:04.512\nKMH2018-05-24_12:02:51.003\nPGS2018-05-24_12:07:23.645\n"
    tmp_start_log.write_text(start_log_content)

    tmp_end_log = data_dir / "end.log"
    end_log_content = "FAM2018-05-24_12:14:17.169\nKMH2018-05-24_12:04:04.396\nPGS2018-05-24_12:08:36.586\n"
    tmp_end_log.write_text(end_log_content)

    return data_dir


@pytest.fixture(scope="session")
def test_app(prepare_database: Path) -> Flask:
    settings.base_dir = prepare_database

    flask_app = create_app()
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )
    return flask_app


@pytest.fixture
def client(test_app: Flask) -> FlaskClient:
    return test_app.test_client()
