from pathlib import Path

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    base_dir: Path = Path("data/")
    ignore_errors: bool = True


settings = AppSettings()
