#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CFG="config/config.yaml"
if [ ! -f "$CFG" ]; then
  CFG="config/config.example.yaml"
fi

python scripts/fetch_prices.py --config "$CFG"
python scripts/fetch_macro.py --config "$CFG"
python scripts/compute_signals.py --config "$CFG"
python scripts/build_report.py --config "$CFG"
python scripts/notify.py --config "$CFG" || true

echo "DONE. Open: site/report.html"
