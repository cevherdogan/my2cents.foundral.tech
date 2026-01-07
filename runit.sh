#!/usr/bin/env bash
set -euo pipefail
cp -n config/config.example.yaml config/config.yaml || true

bash scripts/run_daily.sh

if [ -f site/report.html ]; then
  open site/report.html
else
  echo "ERROR: site/report.html was not generated."
  echo "Check logs by running: bash scripts/run_daily.sh"
  exit 1
fi
