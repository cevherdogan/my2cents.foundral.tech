#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import datetime, timezone
import yaml

def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_config(Path(args.config))
    hint = cfg["scoring"].get("macro_regime_hint","UNKNOWN").upper()

    out_dir = Path(cfg["data"].get("output_dir","data")) / "derived"
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {"ts_utc": datetime.now(timezone.utc).isoformat(), "macro_regime_hint": hint}
    (out_dir/"macro_latest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"OK: macro regime hint saved ({hint})")

if __name__ == "__main__":
    main()
