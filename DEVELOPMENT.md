# Copier template: Playwright Python

This repository is a [Copier](https://copier.readthedocs.io/) template — not a runnable test project on its own.

## Use the template

```bash
uv tool install copier
copier copy /path/to/playwright-python my-product-tests
cd my-product-tests
cp config.local.env.example config.local.env
./run/tests_smoke.sh
```

## Validate locally

```bash
./scripts/generate-sample.sh /tmp/playwright-test-sample
cd /tmp/playwright-test-sample
./run/tests_smoke.sh
```

## Stack

- Playwright + pytest-playwright
- Allure reporting
- Ruff (lint + format)
- uv (package manager)
- Pydantic Settings
- GitHub Actions CI
- pre-commit hooks

See `README.md.jinja` for the documentation copied into generated projects.
