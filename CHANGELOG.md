# CHANGELOG

## v4.2 — Robust price ingestion + signal parsing
- Fixed yfinance MultiIndex edge cases (prevents malformed CSV)
- Hardened signal computation by coercing Close to numeric and dropping junk rows
- Version bumps and docs updates


## v4.1 — Integration Layer ZIP
- Repo skeleton (docs/config/scripts/data/site/ops)
- Working pipeline: (sample/live) prices → signals → score → Magic HTML report
- Append-only JSONL logging
- Report archiving in `site/history/`
- Optional Slack webhook notify

### Docs
- Added release notes, config walkthrough, and operational guide (dev runbook)
