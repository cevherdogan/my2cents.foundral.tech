# Release Notes — Foundral Investment Atlas v4.1

**Release name:** Integration Layer ZIP (TTD vs ENPH)  
**Status:** Runnable prototype (offline-safe with sample data; live fetch optional)  
**Primary artifact:** `site/report.html` (Magic HTML daily brief)  
**Audit trail:** `data/logs/runs.jsonl` (append-only)

---

## What shipped

### 1) Runnable daily pipeline
- Fetch prices (live via `yfinance` or sample fallback)
- Persist `data/raw/latest_TTD.csv` and `data/raw/latest_ENPH.csv`
- Save macro regime hint in `data/derived/macro_latest.json`
- Compute signals + scores in `data/derived/latest_signals.json`
- Build Magic HTML daily report at `site/report.html`
- Archive report copies in `site/history/`

### 2) Transparent scoring (editable)
- Relative strength (20d / 60d)
- 6-month drawdown proxy (126 trading days)
- Rate-regime bonus (manual hint for v4.1)
- Confidence heuristic based on score margin

### 3) Optional notification hook
- Slack webhook support via `scripts/notify.py` (disabled by default)

---

## Known limitations (by design in v4.1)
- **Macro regime is manual** (`macro_regime_hint`). (v4.2 will auto-detect.)
- Earnings calendar and “guide shock” detection are placeholders. (v4.3.)
- Scoring normalization is intentionally simple (audit-first, not ML-first).

---

## Upgrade path
- **v4.2**: auto rate-regime detection (2Y/10Y or FFR proxy)
- **v4.3**: earnings calendar + post-earnings gap alerts
- **v4.4**: expand universe while keeping TTD/ENPH as the decision core

---

## Safety note
This is an educational workflow template and is **not** financial advice.
