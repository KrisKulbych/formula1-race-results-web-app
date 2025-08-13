from http import HTTPStatus

from flask.testing import FlaskClient


class TestErrorHandlers:
    def test_page_is_not_found(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/drive_id")
        # Then
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert b"The page is not found" in response.data
