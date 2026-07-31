import allure
import pytest
from playwright.sync_api import Page, expect

from {{ project_slug }}.pages.duckduckgo_page import DuckDuckGoPage


@allure.feature("Search")
@allure.story("DuckDuckGo")
@pytest.mark.smoke
def test_duckduckgo_search_with_page_object(page: Page) -> None:
    duckduckgo = DuckDuckGoPage(page).open()
    duckduckgo.search("playwright python")
    duckduckgo.should_have_at_least_results(3)
    duckduckgo.open_result(0)
    expect(page).to_have_url("**/playwright.dev/**", timeout=15_000)
