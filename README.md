# Playwright Python Test Automation

This repository provides a starter setup for browser UI tests with Playwright, pytest, Allure, Ruff, and uv.

## Features

- Playwright browser automation with pytest-playwright
- pytest test runner with smoke and regression markers
- Allure reporting with screenshots and page source on failure
- Ruff for linting and formatting
- uv for fast dependency management
- Environment-based configuration with local and production settings
- Example page-object and test files to help you get started

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- [Allure CLI](https://docs.qameta.io/allure/) (optional, for local HTML reports)

## Setup

```bash
uv sync
uv run playwright install --with-deps
cp config.local.env.example config.local.env
```

## VS Code

Open the folder in VS Code or Cursor. When prompted, install the [recommended extensions](.vscode/extensions.json):

- **Python** + **Pylance** — interpreter, pytest discovery, debugging
- **Ruff** — lint and format (matches `./run/lint.sh`)
- **Playwright** — test explorer and trace viewer
- **Even Better TOML**, **YAML**, **DotENV** — config file editing

Shared workspace settings in [.vscode/settings.json](.vscode/settings.json) point at the `.venv` interpreter, enable pytest, and format on save with Ruff. Use **Run Task** for smoke tests, lint, and Allure, or **Run and Debug** for headed pytest debugging.

## AI Assistant Skills

This project includes a `playwright-python` skill for [Cursor](.cursor/skills/playwright-python/SKILL.md) and [Claude Code](.claude/skills/playwright-python/SKILL.md). These teach AI assistants this repo's conventions for page objects, tests, configuration, and running the suite.

## Page Object Model

UI interactions follow the **Page Object Model** — each page is a class in `python_playwright/pages/` that owns locators and actions. Tests describe scenarios; page objects describe how to drive the UI.

```
tests/test_login.py          →  LoginPage(page).open().login(...).should_show_dashboard()
python_playwright/pages/     →  LoginPage, DashboardPage, BasePage
```

See [.cursor/skills/playwright-python/page-object-model.md](.cursor/skills/playwright-python/page-object-model.md) for the full guide (layers, naming, fluent interface, examples).

## Project Structure

- [tests/conftest.py](tests/conftest.py) contains shared Playwright and Allure fixtures
- [tests/test_duckduckgo.py](tests/test_duckduckgo.py) and [tests/test_playwright_docs.py](tests/test_playwright_docs.py) are example tests
- [python_playwright](python_playwright) contains the package code, including config, page objects, and support helpers
- [run](run) contains shell scripts for common workflows

## Configuration

Settings are loaded from [config.local.env.example](config.local.env.example) and [config.prod.env](config.prod.env), plus environment variables.

Common settings include:

- CONTEXT: local or prod
- BASE_URL: base URL for relative navigation
- HEADLESS: run browsers headless
- BROWSER: chromium, firefox, or webkit
- TIMEOUT_MS: default timeout in milliseconds
- VIEWPORT_WIDTH / VIEWPORT_HEIGHT: browser viewport size

## Running Tests

```bash
./run/tests_smoke.sh
./run/tests.sh
./run/tests.sh -m smoke
./run/tests.sh -n auto
./run/tests.sh --browser firefox
./run/tests.sh --reruns 2
```

## Linting and Formatting

```bash
./run/lint.sh
```

## Allure Reports

Test results are written to the allure-results directory. To view them locally:

```bash
./run/tests_and_allure_report.sh
```

Or with the CLI:

```bash
allure serve allure-results
```

## License

MIT
