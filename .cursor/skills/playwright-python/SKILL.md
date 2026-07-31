---
name: playwright-python
description: >-
  Write, run, and debug Playwright Python UI tests in this project using pytest,
  page objects, Allure, and uv. Use when adding or fixing tests, creating page
  objects, running smoke/regression suites, configuring browsers, or debugging
  Playwright failures.
---

# Playwright Python Test Automation

## Stack

- Playwright (sync API) + pytest-playwright
- Page Object Model in `python_playwright/pages/`
- Allure reporting (`@allure.feature`, `@allure.step`)
- Config via Pydantic Settings (`python_playwright/config/settings.py`)
- uv for deps; Ruff for lint/format

## Before writing tests

1. Ensure setup: `uv sync` and `uv run playwright install --with-deps`
2. Copy `config.local.env.example` → `config.local.env` and set `BASE_URL`
3. Read existing page objects and tests before adding new ones

## Page Object Model

Each UI page maps to a class in `python_playwright/pages/`. Tests stay thin (scenario + business assertions); page objects own locators, actions, and page-level checks.

| Layer | Responsibility |
|-------|----------------|
| `tests/` | Arrange steps, pytest markers, cross-page URL/title assertions |
| `pages/*.py` | Locators, user actions, `should_*` assertions for that page |
| `base_page.py` | Shared `open()`, navigation helpers |

**Rules:** extend `BasePage`; set `path`; define locators in `__init__`; prefix assertions with `should_`; return `self` for fluent chains; use `@allure.step` on public methods; never put selectors in tests.

Full POM guide with examples and naming conventions: [page-object-model.md](page-object-model.md)

```python
class MyPage(BasePage):
    path = "/dashboard"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.submit_btn = page.get_by_role("button", name="Submit")

    @allure.step("Open My Page")
    def open(self, path: str | None = None) -> "MyPage":
        super().open(path)
        return self

    @allure.step("Submit the form")
    def submit(self) -> "MyPage":
        self.submit_btn.click()
        return self

    @allure.step("Verify dashboard is shown")
    def should_show_dashboard(self) -> "MyPage":
        expect(self.page.get_by_role("heading", name="Dashboard")).to_be_visible()
        return self
```

### Tests

- Live in `tests/test_*.py`
- Use the `page` fixture from pytest-playwright (do not create browsers manually)
- Mark tests: `@pytest.mark.smoke` or `@pytest.mark.regression`
- Use `@allure.feature` / `@allure.story` for reporting
- Prefer page objects over raw `page` calls in test bodies
- Use `expect(page).to_have_url(...)` / `to_have_title(...)` for cross-page checks

### Configuration

Settings load from `config.{context}.env` (default `local`). Key vars:

| Var | Purpose |
|-----|---------|
| `BASE_URL` | Base URL for relative navigation |
| `HEADLESS` | Browser headless mode |
| `BROWSER` | chromium / firefox / webkit |
| `TIMEOUT_MS` | Default timeout |
| `VIEWPORT_WIDTH/HEIGHT` | Browser viewport |

Fixtures in `tests/conftest.py` wire settings into browser launch, context, and timeouts. On failure, screenshots and page source attach to Allure automatically.

## Running tests

```bash
./run/tests_smoke.sh              # smoke only
./run/tests.sh                    # full suite
./run/tests.sh -m smoke           # by marker
./run/tests.sh -n auto            # parallel
./run/tests.sh --browser firefox  # browser override
./run/lint.sh                     # ruff check + format
./run/tests_and_allure_report.sh  # tests + Allure HTML
```

Always run via `uv run pytest` or the `run/*.sh` scripts — never bare `pytest`.

## Adding a new test flow

1. Create or extend a page object in `python_playwright/pages/`
2. Export it from `python_playwright/pages/__init__.py` if needed
3. Add test in `tests/test_<feature>.py` with appropriate markers and Allure decorators
4. Run `./run/lint.sh` then `./run/tests_smoke.sh` (or targeted: `uv run pytest tests/test_foo.py -k test_name`)
5. Fix failures using Allure artifacts (screenshot + page source)

## Locator priority

1. `get_by_role` (with accessible name)
2. `get_by_label` / `get_by_placeholder`
3. `get_by_test_id`
4. `get_by_text` (exact match when possible)
5. CSS/XPath only as last resort

Avoid brittle selectors tied to layout or styling.

## Anti-patterns

- Do not use `time.sleep()` — use Playwright auto-waiting and `expect()`
- Do not hardcode URLs when `BASE_URL` + `path` works
- Do not skip Allure steps on multi-step flows
- Do not add dependencies outside `pyproject.toml`
- Do not commit `config.local.env` (gitignored secrets/overrides)

## CI alignment

CI runs `uv run ruff check`, `ruff format --check`, then `uv run pytest -m smoke --browser chromium`. Keep changes green against that pipeline.

## Additional resources

- Page Object Model guide: [page-object-model.md](page-object-model.md)
- Locator cheat sheet and env reference: [reference.md](reference.md)
