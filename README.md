# Foundral Investment Atlas — v4.2 (Integration Layer ZIP)

This ZIP is a **repo skeleton + runnable prototype** that turns the v3 “TTD vs ENPH” decision into an operational system:
**data → signals → score → report → (optional) alerts**.

> Educational use only. Not financial advice.

---

## Quick Start (macOS)

```bash
cd foundral-investment-atlas-v4.2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create your editable config (gitignored)
cp config/config.example.yaml config/config.yaml

# Run the daily pipeline (uses sample data if live fetch fails)
bash scripts/run_daily.sh

# Open the report
open site/report.html
```

### What you should see
- `site/report.html` updated (mobile-friendly Magic HTML)
- `data/logs/runs.jsonl` appended (audit trail)
- `site/history/report_YYYYMMDD_HHMMSS.html` archived

---

## Live data options (optional)
This prototype includes **sample data** so it runs offline.

If you want live prices:
- Ensure internet access.
- `scripts/fetch_prices.py` uses `yfinance` by default.

For macro proxy (rates regime):
- v4.2 uses a **manual hint** in config: `macro_regime_hint` (CUTS/HIKES/STICKY/UNKNOWN).
- v4.2 can wire auto-regime detection.

---

## Repo Map (what matters)
- `docs/ATLAS_CANON_v3.md` — frozen decision canon (don’t edit without bumping)
- `config/config.yaml` — thresholds + weights + notifications
- `scripts/compute_signals.py` — core: RS, drawdown, regime bonus, scores
- `scripts/build_report.py` — generates Magic HTML report
- `scripts/notify.py` — optional Slack webhook notify
