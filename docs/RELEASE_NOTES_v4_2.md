# Release Notes — Foundral Investment Atlas v4.2

**Theme:** Robust ingestion + resilient signal computation

## Fixes
- `scripts/fetch_prices.py`: MultiIndex-safe yfinance handling, guaranteed numeric `Close`.
- `scripts/compute_signals.py`: coerces `Close` to numeric + drops malformed rows before returns/drawdown calculations.

## Outcome
- Running `./runit.sh` should consistently produce `site/report.html` even when yfinance output formatting varies.

Educational use only. Not financial advice.
