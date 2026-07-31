from playwright.sync_api import Locator, Page, expect

from {{ project_slug }}.config.settings import settings


class BasePage:
    """Base page object with shared Playwright helpers."""

    path: str = ""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = settings.base_url.rstrip("/")

    def open(self, path: str | None = None) -> None:
        target = path if path is not None else self.path
        if target.startswith("http"):
            url = target
        elif self.base_url:
            url = f"{self.base_url}{target}"
        else:
            msg = "Set BASE_URL in config or pass an absolute URL."
            raise ValueError(msg)
        self.page.goto(url, wait_until="domcontentloaded")

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def should_have_title(self, expected: str | object) -> None:
        expect(self.page).to_have_title(expected)

    def should_have_url(self, expected: str | object) -> None:
        expect(self.page).to_have_url(expected)
