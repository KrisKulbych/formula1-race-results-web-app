import html
from http import HTTPStatus

from flask.testing import FlaskClient

from formula1_web_app.settings import settings


class TestRoutes:
    def test_redirect_from_root_to_report_page(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/")
        # Then
        assert response.status_code == HTTPStatus.MOVED_PERMANENTLY
        assert response.headers["Content-Type"] == "text/html; charset=utf-8"
        assert response.location.endswith("/report/")

    def test_report_page_returns_success_status(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/", follow_redirects=True)
        data = response.get_data(as_text=True)
        # Then
        assert response.status_code == HTTPStatus.OK
        assert "<h2>Formula1 Race Report</h2>" in data
        assert "<th>Driver name</th>" in data
        assert "<td>Kevin Magnussen</td>" in data

    def test_correct_sort_order(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/?order=asc")
        data = response.get_data(as_text=True)
        # Then
        assert response.status_code == HTTPStatus.OK
        assert "Sorting in ascending order" in data
        assert data.index("Kevin Magnussen") > data.index("Pierre Gasly")
        assert data.index("Pierre Gasly") > data.index("Fernando Alonso")

    def test_default_sorting_is_used_when_order_parameter_is_invalid(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/?order=minus")
        data = response.get_data(as_text=True)
        # Then
        assert response.status_code == HTTPStatus.OK
        assert "Sorting in descending order" in data
        assert data.index("Kevin Magnussen") < data.index("Pierre Gasly")
        assert data.index("Pierre Gasly") < data.index("Fernando Alonso")

    def test_not_found_driver_id_request(self, client: FlaskClient) -> None:
        # Given
        client_request = "vvv"
        response = client.get(f"/report/drivers/{client_request}")
        expected_error_message = f"No driver with ID '{client_request.upper()}' found in race data."
        # Then
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert expected_error_message in html.unescape(response.get_data(as_text=True))

    def test_invalid_driver_id_request(self, client: FlaskClient) -> None:
        # Given
        client_request = "123"
        response = client.get(f"/report/drivers/{client_request}")
        expected_error_message = (
            f"Identifier '{client_request}' is not recognized. Try to use 3-letter code like 'KRF': "
            "the first letters of the first name: 'K', the first letters of the last name: 'R' and the first "
            "letters of the car model: 'F'."
        )
        # Then
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert expected_error_message in html.unescape(response.get_data(as_text=True))

    def test_correct_driver_id_request(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/drivers/FAM")
        data = response.get_data(as_text=True)
        # Then
        assert response.status_code == HTTPStatus.OK
        assert "Fernando Alonso" in data
        assert "MCLAREN RENAULT" in data
        assert "1:12.657" in data

    def test_drivers_page(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/drivers")
        data = response.get_data(as_text=True)
        # Then
        assert response.status_code == HTTPStatus.OK
        assert "list of drivers" in data
        assert "Fernando Alonso" in data
        assert 'href="/report/drivers/FAM"' in data

    def test_clean_cache_success(self, client: FlaskClient) -> None:
        # Given
        response = client.get(f"/admin/clean-cache?token={settings.admin_token}")
        # Then
        assert response.status_code == HTTPStatus.OK
        assert b"Cache has been successfully cleaned." in response.data

    def test_clean_cache_invalid_token(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/admin/clean-cache?token=wrong_token")
        # Then
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert b"Access denied: invalid or missing token." in response.data
