import allure
from playwright.sync_api import Page, expect

from python_playwright.pages.base_page import BasePage


class PlaywrightDocsPage(BasePage):
    """Page object for Playwright documentation."""

    path = "https://playwright.dev/python/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.get_started_link = page.get_by_role("link", name="Get started")
        self.installation_heading = page.get_by_role("heading", name="Installation")

    @allure.step("Open Playwright Python docs")
    def open(self, path: str | None = None) -> "PlaywrightDocsPage":
        super().open(path)
        return self

    @allure.step("Navigate to Getting Started")
    def go_to_getting_started(self) -> "PlaywrightDocsPage":
        self.get_started_link.click()
        return self

    @allure.step("Verify installation section is visible")
    def should_show_installation(self) -> "PlaywrightDocsPage":
        expect(self.installation_heading).to_be_visible()
        return self
