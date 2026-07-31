# Playwright Python Reference

## Page Object Model

See [page-object-model.md](page-object-model.md) for the full pattern definition, layer responsibilities, naming conventions, and worked examples.

## Environment variables

Loaded from `config.local.env` (local) or `config.prod.env` (prod). Override via env vars at runtime.

| Variable | Default | Description |
|----------|---------|-------------|
| `CONTEXT` | `local` | `local` or `prod` — selects env file |
| `BASE_URL` | `""` | Base URL for relative `path` navigation |
| `HEADLESS` | `false` | Run browsers without UI |
| `BROWSER` | `chromium` | `chromium`, `firefox`, or `webkit` |
| `TIMEOUT_MS` | `30000` | Default action/navigation timeout |
| `SLOW_MO_MS` | `0` | Delay between actions (debugging) |
| `VIEWPORT_WIDTH` | `1440` | Browser viewport width |
| `VIEWPORT_HEIGHT` | `900` | Browser viewport height |
| `TRACE` | `retain-on-failure` | `on`, `off`, `retain-on-failure` |
| `SCREENSHOT` | `only-on-failure` | `on`, `off`, `only-on-failure` |
| `VIDEO` | `off` | `on`, `off`, `retain-on-failure` |
| `PARALLEL_WORKERS` | `auto` | pytest-xdist workers |
| `RERUNS` | `0` | pytest-rerunfailures count |

## Locator examples

```python
# Preferred: role-based
page.get_by_role("button", name="Submit")
page.get_by_role("link", name="Get started")
page.get_by_role("heading", name="Installation")

# Form fields
page.get_by_label("Email")
page.get_by_placeholder("Search...")

# Test IDs
page.get_by_test_id("result-title-a")

# Text (use exact=True when possible)
page.get_by_text("Sign in", exact=True)

# CSS (last resort)
page.locator('[name="q"]')
```

## Allure decorators

```python
@allure.feature("Search")
@allure.story("DuckDuckGo")
@pytest.mark.smoke
def test_example(page: Page) -> None:
    ...

@allure.step('Search for "{query}"')
def search(self, query: str) -> "MyPage":
    ...
```

## Common assertions

```python
from playwright.sync_api import expect

expect(page).to_have_url("**/docs/**")
expect(page).to_have_title("Expected Title")
expect(locator).to_be_visible()
expect(locator).to_have_text("Hello")
expect(locator).to_have_count(3)
```

## Targeted test runs

```bash
uv run pytest tests/test_duckduckgo.py
uv run pytest -k "search"
uv run pytest -m "smoke and not regression"
uv run pytest --headed --slowmo 500
uv run pytest --tracing on
```

## Debugging failures

1. Check Allure report for screenshot and page source attachments
2. Re-run with `--headed` and `HEADLESS=false` in `config.local.env`
3. Use `SLOW_MO_MS=500` to slow actions
4. Use `page.pause()` for interactive debugging (headed mode)
5. Check `test-results/videos/` when `VIDEO=on`
