#!/usr/bin/env bash
# Generate a sample project locally to validate the template.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${1:-/tmp/playwright-test-sample}"

rm -rf "$OUTPUT_DIR"
copier copy "$ROOT_DIR" "$OUTPUT_DIR" \
  --defaults \
  --trust \
  --data project_name="Sample Playwright Tests" \
  --data project_slug="sample_playwright_tests" \
  --data author_name="Template Maintainer" \
  --data author_email="maintainer@example.com" \
  --data python_version="3.12" \
  --data base_url=""

echo "Sample project generated at: $OUTPUT_DIR"
