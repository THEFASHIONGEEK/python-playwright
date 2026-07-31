# Development

Contributor notes for this Playwright Python test automation project.

## Setup

```bash
uv sync
uv run playwright install --with-deps
cp config.local.env.example config.local.env
./run/tests_smoke.sh
```

## Validate changes

```bash
./run/lint.sh
./run/tests_smoke.sh
./run/tests.sh
```

## AI skills

`.cursor/skills/playwright-python/` and `.claude/skills/playwright-python/` hold project-specific Playwright conventions. Update both when changing test patterns so Cursor and Claude Code stay in sync.

## VS Code

Commit shared files under `.vscode/` (`extensions.json`, `settings.json`, `launch.json`, `tasks.json`). `.gitignore` uses an allowlist so personal VS Code state stays local.

## Stack

- Playwright + pytest-playwright
- Allure reporting
- Ruff (lint + format)
- uv (package manager)
- Pydantic Settings
- GitHub Actions CI
- pre-commit hooks

## pre-commit

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```
