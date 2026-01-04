from fastapi import status
from fastapi.testclient import TestClient

from formula1_web_app.api.v1.schemas import Format


class TestEndpoints:
    def test_redirect_from_root_to_report_endpoint(self, api_client: TestClient) -> None:
        # Given
        response = api_client.get("/", follow_redirects=False)
        # Then
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"].endswith("/api/v1/report/")
        # Given
        redirected = api_client.get("/", follow_redirects=True)
        # Then
        assert redirected.status_code == status.HTTP_200_OK

    def test_get_race_report_in_json_format(self, api_client: TestClient) -> None:
        # Given
        response = api_client.get("/api/v1/report/")
        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "results": [
                {
                    "driver": {"identifier": "FAM", "name": "Fernando Alonso", "car_model": "MCLAREN RENAULT"},
                    "lap_time": "1:12.657",
                },
                {
                    "driver": {"identifier": "PGS", "name": "Pierre Gasly", "car_model": "SCUDERIA TORO ROSSO HONDA"},
                    "lap_time": "1:12.941",
                },
                {
                    "driver": {"identifier": "KMH", "name": "Kevin Magnussen", "car_model": "HAAS FERRARI"},
                    "lap_time": "1:13.393",
                },
            ]
        }

    def test_get_drivers_list_in_json_format(self, api_client: TestClient) -> None:
        # Given
        response = api_client.get("/api/v1/report/drivers/")
        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "results": [
                {"identifier": "PGS", "name": "Pierre Gasly"},
                {"identifier": "KMH", "name": "Kevin Magnussen"},
                {"identifier": "FAM", "name": "Fernando Alonso"},
            ]
        }

    def test_get_drivers_list_in_xml_format(self, api_client: TestClient) -> None:
        # Given
        response = api_client.get(f"/api/v1/report/drivers/?fmt={Format.xml}")
        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/xml"
        expected_response = (
            "<results>"
            "<info><identifier>PGS</identifier><name>Pierre Gasly</name></info>"
            "<info><identifier>KMH</identifier><name>Kevin Magnussen</name></info>"
            "<info><identifier>FAM</identifier><name>Fernando Alonso</name></info>"
            "</results>"
        )
        assert response.text == expected_response

    def test_get_driver_info_in_json_format(self, api_client: TestClient) -> None:
        # Given
        driver_id = "FAM"
        response = api_client.get(f"/api/v1/report/drivers/{driver_id}")
        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "results": [
                {
                    "driver": {"identifier": "FAM", "name": "Fernando Alonso", "car_model": "MCLAREN RENAULT"},
                    "lap_time": "1:12.657",
                }
            ]
        }

    def test_get_driver_info_in_xml_format(self, api_client: TestClient) -> None:
        # Given
        driver_id = "FAM"
        response = api_client.get(f"/api/v1/report/drivers/{driver_id}?fmt={Format.xml}")
        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/xml"
        expected_response = (
            "<results>"
            "<info>"
            "<driver>"
            "<identifier>FAM</identifier><name>Fernando Alonso</name><car_model>MCLAREN RENAULT</car_model>"
            "</driver>"
            "<lap_time>1:12.657</lap_time>"
            "</info>"
            "</results>"
        )
        assert response.text == expected_response

    def test_driver_not_found(self, api_client: TestClient) -> None:
        # Given
        driver_id = "MAF"
        response = api_client.get(f"/api/v1/report/drivers/{driver_id}")
        # Then
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == f"No driver with ID '{driver_id}' found in race data."
        assert data["request"]["method"] == "GET"
        assert data["request"]["path"] == f"/api/v1/report/drivers/{driver_id}"

    def test_invalid_driver_id(self, api_client: TestClient) -> None:
        # Given
        driver_id = "MA1"
        response = api_client.get(f"/api/v1/report/drivers/{driver_id}")
        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data["detail"] == f"Identifier '{driver_id}' is not recognized. Try to use 3-letter code like 'KRF'."
        assert data["request"]["method"] == "GET"
        assert data["request"]["path"] == f"/api/v1/report/drivers/{driver_id}"
