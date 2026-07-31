#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

uv sync
uv run playwright install --with-deps

echo "Template project generated successfully."
echo "Next steps:"
echo "  cd $(basename "$PWD")"
echo "  cp config.local.env.example config.local.env"
echo "  ./run/tests.sh"
