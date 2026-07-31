import allure
from playwright.sync_api import Page, expect

from python_playwright.pages.base_page import BasePage


class DuckDuckGoPage(BasePage):
    """Page object for DuckDuckGo search flows."""

    path = "https://duckduckgo.com/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.search_input = page.locator('[name="q"]')
        self.result_links = page.locator('[data-testid="result-title-a"]')

    @allure.step("Open DuckDuckGo")
    def open(self, path: str | None = None) -> "DuckDuckGoPage":
        super().open(path)
        return self

    @allure.step('Search for "{query}"')
    def search(self, query: str) -> "DuckDuckGoPage":
        self.search_input.fill(query)
        self.search_input.press("Enter")
        return self

    @allure.step("Verify at least {min_count} search results")
    def should_have_at_least_results(self, min_count: int) -> "DuckDuckGoPage":
        expect(self.result_links.nth(min_count - 1)).to_be_visible(timeout=10_000)
        return self

    @allure.step("Open search result at index {index}")
    def open_result(self, index: int = 0) -> None:
        self.result_links.nth(index).click()
