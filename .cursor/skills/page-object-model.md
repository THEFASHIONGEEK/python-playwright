# Page Object Model (POM)

## What it is

The **Page Object Model** is a design pattern that maps each page (or major UI surface) in your application to a Python class. Each class:

- **Encapsulates locators** — selectors live in one place, not scattered across tests
- **Exposes user actions** — `search()`, `submit()`, `go_to_settings()` mirror what a user does
- **Hides Playwright details** — tests call readable methods instead of raw `page.locator(...).click()`

Tests stay thin: they describe *what* to verify. Page objects describe *how* to interact with the UI.

## Layer responsibilities

```
tests/                    → Arrange + assert business outcomes (no locators)
python_playwright/pages/  → Locators, actions, page-level assertions
base_page.py              → Shared navigation and cross-page helpers
```

| Layer | Owns | Does not own |
|-------|------|--------------|
| **Test** | Scenario steps, markers, cross-page URL/title checks | CSS selectors, click/fill details |
| **Page object** | Locators, interactions, visibility/text assertions on that page | Browser lifecycle, config |
| **BasePage** | `open()`, shared `expect()` helpers | Page-specific locators |

## File layout

```
python_playwright/pages/
├── __init__.py           # public exports
├── base_page.py          # BasePage — extend this
├── login_page.py         # one class per page / flow
├── dashboard_page.py
└── components/           # optional: shared widgets (header, modal)
    └── nav_bar.py
```

- One primary class per file; filename is `snake_case` matching the class (`LoginPage` → `login_page.py`)
- Register new page objects in `pages/__init__.py`

## Class structure

Every page object follows this shape:

```python
class ExamplePage(BasePage):
  path = "/example"                    # 1. route (relative or absolute)

  def __init__(self, page: Page):      # 2. locators
    super().__init__(page)
    self.heading = page.get_by_role("heading", name="Example")

  def open(...) -> "ExamplePage":       # 3. navigation (returns self)
  def do_something(...) -> "ExamplePage":  # 4. actions (returns self)
  def should_show_...(...) -> "ExamplePage":  # 5. assertions (returns self)
  def leave_page(...) -> None:          # 6. terminal action (no return)
```

### 1. `path`

- Relative path when `BASE_URL` is set: `path = "/login"`
- Absolute URL for external sites: `path = "https://example.com/"`

### 2. Locators (in `__init__`)

Define once as instance attributes. Prefer accessible selectors:

```python
self.submit_btn = page.get_by_role("button", name="Submit")
self.email_input = page.get_by_label("Email")
```

### 3. Navigation — `open()`

Override `open()` to return `self` for method chaining:

```python
@allure.step("Open Example page")
def open(self, path: str | None = None) -> "ExamplePage":
    super().open(path)
    return self
```

### 4. Actions

Methods that change UI state. Name with verbs (`search`, `fill_form`, `click_save`). Return `self` for fluent chains:

```python
@allure.step('Search for "{query}"')
def search(self, query: str) -> "ExamplePage":
    self.search_input.fill(query)
    self.search_input.press("Enter")
    return self
```

### 5. Assertions — `should_*`

Page-level checks using `expect()`. Prefix with `should_`:

```python
@allure.step("Verify welcome message is visible")
def should_show_welcome(self) -> "ExamplePage":
    expect(self.heading).to_be_visible()
    return self
```

### 6. Terminal actions

When navigation leaves the page (clicking a link to a new page object), return `None` or the *next* page object:

```python
# Returns None — test asserts URL after
def open_result(self, index: int = 0) -> None:
    self.result_links.nth(index).click()

# Or return the destination page object
def go_to_settings(self) -> "SettingsPage":
    self.settings_link.click()
    return SettingsPage(self.page)
```

## Fluent interface

Chain calls in tests for readable scenarios:

```python
def test_search_flow(page: Page) -> None:
    (
        DuckDuckGoPage(page)
        .open()
        .search("playwright python")
        .should_have_at_least_results(3)
    )
    DuckDuckGoPage(page).open_result(0)  # terminal — leaves page
    expect(page).to_have_url("**/playwright.dev/**")
```

Rules:

- **Actions and assertions** → return `self`
- **Navigation to another page object** → return the new page object (preferred) or `None`
- **Never** return `self` after an action that navigates away unless you stay on the same logical page

## Method naming

| Type | Prefix / style | Examples |
|------|----------------|----------|
| Action | verb | `search()`, `submit()`, `select_option()` |
| Assertion | `should_` | `should_be_visible()`, `should_have_count(3)` |
| Query | `get_` (rare) | `get_error_message()` — prefer assertions |
| Navigation | `open`, `go_to` | `open()`, `go_to_checkout()` |

## Components (optional)

Extract repeated UI fragments into component classes that take `page` or a root `Locator`:

```python
class NavBar:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logout_btn = page.get_by_role("button", name="Log out")

    def logout(self) -> None:
        self.logout_btn.click()
```

Use inside page objects:

```python
class DashboardPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.nav = NavBar(page)
```

## Real example

From `duckduckgo_page.py` + `test_duckduckgo.py`:

**Page object** — owns locators and interactions:

```python
class DuckDuckGoPage(BasePage):
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
```

**Test** — owns the scenario, no selectors:

```python
def test_duckduckgo_search_with_page_object(page: Page) -> None:
    duckduckgo = DuckDuckGoPage(page).open()
    duckduckgo.search("playwright python")
    duckduckgo.should_have_at_least_results(3)
    duckduckgo.open_result(0)
    expect(page).to_have_url("**/playwright.dev/**", timeout=15_000)
```

## Do / don't

| Do | Don't |
|----|-------|
| Put selectors only in page objects | Duplicate selectors in tests |
| Use `@allure.step` on public methods | Put test logic (`if`/`for` loops) in page objects |
| Keep one page per class | Create a mega-class for the entire app |
| Assert page state in `should_*` methods | Assert business rules that belong in tests |
| Return next page object on navigation | Hardcode waits with `time.sleep()` |
| Use `expect()` auto-waiting | Catch exceptions to swallow failures |

## Adding a new page object

1. Create `python_playwright/pages/<name>_page.py` extending `BasePage`
2. Set `path`, define locators in `__init__`
3. Add `open()`, actions, and `should_*` assertions
4. Export from `pages/__init__.py`
5. Write tests in `tests/test_<feature>.py` using only the page API
