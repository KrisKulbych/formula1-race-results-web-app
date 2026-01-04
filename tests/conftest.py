from copy import deepcopy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from flask import Flask
from flask.testing import FlaskClient

from formula1_web_app.api.app import api
from formula1_web_app.app_factory import create_app
from formula1_web_app.settings import settings


@pytest.fixture(scope="session")
def temp_data_directory(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_path = tmp_path_factory.mktemp("data_root")
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    return data_dir


@pytest.fixture(scope="session")
def temp_abbreviations_file(temp_data_directory: Path) -> Path:
    tmp_abbreviations = temp_data_directory / "abbreviations.txt"
    abbreviations_content = (
        "PGS_Pierre Gasly_SCUDERIA TORO ROSSO HONDA\n"
        "KMH_Kevin Magnussen_HAAS FERRARI\n"
        "FAM_Fernando Alonso_MCLAREN RENAULT\n"
    )
    tmp_abbreviations.write_text(abbreviations_content)
    return tmp_abbreviations


@pytest.fixture(scope="session")
def temp_start_log_file(temp_data_directory: Path) -> Path:
    tmp_start_log = temp_data_directory / "start.log"
    start_log_content = "FAM2018-05-24_12:13:04.512\nKMH2018-05-24_12:02:51.003\nPGS2018-05-24_12:07:23.645\n"
    tmp_start_log.write_text(start_log_content)
    return tmp_start_log


@pytest.fixture(scope="session")
def temp_end_log_file(temp_data_directory: Path) -> Path:
    tmp_end_log = temp_data_directory / "end.log"
    end_log_content = "FAM2018-05-24_12:14:17.169\nKMH2018-05-24_12:04:04.396\nPGS2018-05-24_12:08:36.586\n"
    tmp_end_log.write_text(end_log_content)
    return tmp_end_log


@pytest.fixture(scope="session")
def test_app(temp_data_directory: Path) -> Flask:
    test_settings = deepcopy(settings)
    test_settings.base_dir = temp_data_directory
    flask_app = create_app()

    flask_app.config.update(
        {
            "TESTING": True,
        },
    )
    return flask_app


@pytest.fixture(scope="session")
def client(test_app: Flask) -> FlaskClient:
    return test_app.test_client()


@pytest.fixture(scope="session")
def api_client(
    temp_data_directory: Path,
    temp_abbreviations_file: Path,
    temp_start_log_file: Path,
    temp_end_log_file: Path,
) -> TestClient:
    _ = (
        temp_abbreviations_file,
        temp_start_log_file,
        temp_end_log_file,
    )
    settings.base_dir = temp_data_directory
    return TestClient(api)
