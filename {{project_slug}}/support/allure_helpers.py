import allure
from playwright.sync_api import Page


def attach_failure_artifacts(page: Page) -> None:
    """Attach screenshot and page source to the Allure report on failure."""
    screenshot = page.screenshot(full_page=True)
    allure.attach(
        screenshot,
        name="screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(
        page.content(),
        name="page-source",
        attachment_type=allure.attachment_type.HTML,
    )
