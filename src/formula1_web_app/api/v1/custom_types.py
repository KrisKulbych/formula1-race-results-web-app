from typing import TypedDict


class SerializedXmlData(TypedDict):
    data: list[str] | dict[str, str] | str
