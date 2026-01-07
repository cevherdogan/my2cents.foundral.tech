# Config Walkthrough (Dev/Ops) — v4.1

File location:
- Template: `config/config.example.yaml`
- Your live config (gitignored): `config/config.yaml`

---

## Step 1 — Create your config

```bash
cp config/config.example.yaml config/config.yaml
```

---

## Step 2 — Set data behavior

```yaml
data:
  use_live_fetch: true
  lookback_days: 365
  output_dir: "data"
  site_dir: "site"
```

**Notes**
- If `use_live_fetch: true` but live fetch fails, the pipeline falls back to sample CSVs.
- Increase `lookback_days` if you want longer windows for drawdown calculations.

---

## Step 3 — Set macro regime (v4.1 manual)

```yaml
scoring:
  macro_regime_hint: "UNKNOWN"  # CUTS | HIKES | STICKY | UNKNOWN
```

This is the integration point for later automation (v4.2).

---

## Step 4 — Tune weights (audit-first)

```yaml
scoring:
  weights:
    trend: 0.35
    survival: 0.35
    macro: 0.20
    events: 0.10
```

Guidance:
- If you want “survival-first,” raise `survival` and lower `trend`.
- Keep `events` small until v4.3 adds real event logic.

---

## Step 5 — Regime bonus map

```yaml
scoring:
  regime_bonus:
    CUTS:   {TTD: 0.20, ENPH: 0.35}
    HIKES:  {TTD: 0.35, ENPH: 0.05}
    STICKY: {TTD: 0.30, ENPH: 0.10}
    UNKNOWN:{TTD: 0.15, ENPH: 0.15}
```

Interpretation:
- ENPH gets more upside in **CUTS** (demand/financing sensitivity).
- TTD gets more resilience in **HIKES/STICKY**.

---

## Step 6 — Thresholds and alerts

```yaml
thresholds:
  drawdown_breach: 0.45
  pick_flip_margin: 0.10
```

- `drawdown_breach`: triggers a drawdown alert if exceeded.
- `pick_flip_margin`: flags a flip candidate only if ENPH score exceeds TTD by this margin.

---

## Step 7 — Notifications (optional)

```yaml
notifications:
  enabled: false
  slack_webhook_url: ""
```

To enable Slack alerts:
1) Paste your webhook URL.
2) Set `enabled: true`.
3) Run `bash scripts/run_daily.sh`.

---

## Troubleshooting
- If you see “Missing latest prices…” run:
  - `python scripts/fetch_prices.py --config config/config.yaml`
- If report doesn’t change:
  - Delete `site/report.html` and rerun the pipeline.
