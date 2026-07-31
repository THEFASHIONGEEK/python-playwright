#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

./run/tests.sh "$@"

if command -v allure >/dev/null 2>&1; then
  allure serve allure-results
else
  echo "Allure CLI not found. Install from https://docs.qameta.io/allure/"
  echo "Raw results are available in ./allure-results"
fi
