from enum import StrEnum

from formula1_race_analysis import Driver, RaceResult
from pydantic import BaseModel, ConfigDict, model_validator


class Format(StrEnum):
    """Supported API response formats."""

    json = "json"
    xml = "xml"


class DriverSchema(BaseModel):
    """Pydantic model for a Formula 1 driver."""

    identifier: str
    name: str
    car_model: str

    model_config = ConfigDict(from_attributes=True)


class RaceResultSchema(BaseModel):
    """Pydantic model for a race result with formatted lap time."""

    driver: Driver
    lap_time: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def format_lap_time(cls, value: RaceResult) -> dict[str, Driver | str]:
        return {"driver": value.driver, "lap_time": value.format_lap_time()}


class DriverListSchema(BaseModel):
    """Simplified driver information for listing endpoints."""

    identifier: str
    name: str

    model_config = ConfigDict(from_attributes=True)
