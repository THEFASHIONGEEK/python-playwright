import allure
import pytest
from playwright.sync_api import Page, expect

from {{ project_slug }}.pages.playwright_docs_page import PlaywrightDocsPage


@allure.feature("Documentation")
@allure.story("Playwright Python docs")
@pytest.mark.smoke
def test_playwright_docs_getting_started(page: Page) -> None:
    docs = PlaywrightDocsPage(page).open()
    docs.go_to_getting_started()
    docs.should_show_installation()
    expect(page).to_have_url("docs/intro", timeout=10_000)


@allure.feature("Documentation")
@allure.story("Straightforward style")
@pytest.mark.regression
def test_playwright_docs_title(page: Page) -> None:
    page.goto("https://playwright.dev/python/")
    expect(page).to_have_title(
        "Fast and reliable end-to-end testing for modern web apps | Playwright Python"
    )
