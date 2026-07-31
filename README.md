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
