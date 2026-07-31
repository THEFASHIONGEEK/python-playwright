from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

EnvContext = Literal["local", "prod"]
BrowserName = Literal["chromium", "firefox", "webkit"]
TraceMode = Literal["on", "off", "retain-on-failure"]
ScreenshotMode = Literal["on", "off", "only-on-failure"]
VideoMode = Literal["on", "off", "retain-on-failure"]

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def env_file_for(context: EnvContext) -> Path:
    return PROJECT_ROOT / f"config.{context}.env"


class Settings(BaseSettings):
    """Project configuration loaded from env files and environment variables."""

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    context: EnvContext = "local"
    base_url: str = "{{ base_url }}"
    headless: bool = False
    browser: BrowserName = "chromium"
    timeout_ms: int = 30_000
    slow_mo_ms: int = 0
    viewport_width: int = 1440
    viewport_height: int = 900
    trace: TraceMode = "retain-on-failure"
    screenshot: ScreenshotMode = "only-on-failure"
    video: VideoMode = "off"
    parallel_workers: str = "auto"
    reruns: int = 0
    author: str = Field(default="{{ author_name }}")

    @classmethod
    def in_context(cls, env: EnvContext | None = None) -> "Settings":
        asked_or_current = env or cls().context
        return cls(_env_file=env_file_for(asked_or_current))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.in_context()


settings = get_settings()


if __name__ == "__main__":
    print(settings.model_dump())
