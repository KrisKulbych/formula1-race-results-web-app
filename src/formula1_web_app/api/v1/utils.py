import xml.etree.ElementTree as ET

from fastapi.responses import JSONResponse, Response
from formula1_race_analysis import RaceResult

from formula1_web_app.api.v1.custom_types import SerializedXmlData
from formula1_web_app.api.v1.schemas import DriverListSchema, Format, RaceResultSchema


def serialize_data_to_xml_element(root_tag: str, data: SerializedXmlData) -> ET.Element:
    """Recursively serialize data into an XML element."""
    root = ET.Element(root_tag)

    if isinstance(data, list):
        for info in data:
            root.append(serialize_data_to_xml_element("info", info))

    elif isinstance(data, dict):
        for tag, content in data.items():
            root.append(serialize_data_to_xml_element(tag, content))

    else:
        root.text = str(data)

    return root


def convert_data_to_xml_string(root_tag: str, data: SerializedXmlData) -> str:
    """Convert data into an XML string with the given root tag."""
    root_element = serialize_data_to_xml_element(root_tag, data)
    return ET.tostring(root_element, encoding="utf-8")


def convert_race_results_to_schema_objects(results: list[RaceResult]) -> list[RaceResultSchema]:
    """Convert a list of RaceResult dataclass instances into Pydantic schemas."""
    return [RaceResultSchema.model_validate(result) for result in results]


def build_api_response(
    results: list[RaceResultSchema] | list[DriverListSchema], fmt: Format
) -> JSONResponse | Response:
    """Build API response in JSON or XML format."""
    payload = [item.model_dump() for item in results]

    if fmt == Format.xml:
        xml_content = convert_data_to_xml_string("results", payload)
        return Response(content=xml_content, media_type="application/xml")

    return JSONResponse({"results": payload})
