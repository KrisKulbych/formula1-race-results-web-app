from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent.parent / "data"
    ignore_errors: bool = True
    admin_token: str | None = Field(default=None)

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")


settings = AppSettings()
