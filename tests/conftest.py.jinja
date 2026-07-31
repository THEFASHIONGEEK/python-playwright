import pytest
from playwright.sync_api import Page

from {{ project_slug }}.config.settings import settings
from {{ project_slug }}.support.allure_helpers import attach_failure_artifacts


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "headless": settings.headless,
        "slow_mo": settings.slow_mo_ms,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    context_args = {
        **browser_context_args,
        "viewport": {
            "width": settings.viewport_width,
            "height": settings.viewport_height,
        },
    }
    if settings.base_url:
        context_args["base_url"] = settings.base_url
    if settings.video != "off":
        context_args["record_video_dir"] = "test-results/videos"
    return context_args


@pytest.fixture(autouse=True)
def configure_page_timeouts(page: Page) -> None:
    page.set_default_timeout(settings.timeout_ms)
    page.set_default_navigation_timeout(settings.timeout_ms)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    page: Page | None = item.funcargs.get("page")
    if page is not None:
        attach_failure_artifacts(page)
