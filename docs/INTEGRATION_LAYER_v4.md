# INTEGRATION_LAYER_v4

v4 goal: make the decision repeatable and auditable.

Pipeline
1) Fetch prices (live via yfinance OR sample fallback)
2) Fetch macro proxy (v4.1: regime hint from config)
3) Compute signals + scores (TTD vs ENPH)
4) Build HTML report
5) Append JSONL run log
6) Optional notify

Artifacts
- data/raw/latest_TTD.csv, latest_ENPH.csv
- data/derived/latest_signals.json
- data/logs/runs.jsonl
- site/report.html + site/history/
