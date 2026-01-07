# Operational Guide (Dev Runbook) — v4.1

This runbook describes how to run, validate, and automate the Atlas pipeline.

---

## Local run (macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp config/config.example.yaml config/config.yaml
bash scripts/run_daily.sh
open site/report.html
```

Validation checklist:
- `site/report.html` exists and has today’s timestamp in the header
- `data/derived/latest_signals.json` exists
- `data/logs/runs.jsonl` grew by one line
- `site/history/` contains a new archived report

---

## What to commit vs ignore
Commit:
- `scripts/`
- `docs/`
- `ops/`
- `site/report.html` (optional, but nice for GitHub Pages)
- `site/history/` (optional)
- `data/derived/latest_signals.json` (optional)
- `data/logs/runs.jsonl` (optional; can get large)

Ignore:
- `config/config.yaml` (contains secrets)

---

## Recommended Git workflow (tagged releases)

### First-time repo setup
```bash
git init
git add .
git commit -m "v4.1: integration layer prototype (TTD vs ENPH)"
```

### Tag
```bash
git tag -a v4.1 -m "Foundral Investment Atlas v4.1"
```

### Add remote + push
```bash
git remote add origin <YOUR_GIT_URL>
git branch -M main
git push -u origin main
git push origin --tags
```

---

## GitHub Actions (daily)
- Copy `ops/github_actions_workflow.yml` into `.github/workflows/atlas.yml`
- Ensure `config/config.yaml` is created in the runner using GitHub Secrets (v4.2+), or keep `use_live_fetch=false` and run sample mode.
- For Slack webhook, store it as a secret and write it into config at runtime.

---

## Operational policy (strongly recommended)
- Treat `docs/ATLAS_CANON_v3.md` as frozen truth.
- Any changes to scoring/invalidation must bump version (v4.2, v4.3, …).
- Keep `runs.jsonl` append-only to preserve auditability.
