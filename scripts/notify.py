#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
import requests

def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_config(Path(args.config))
    notif = cfg.get("notifications",{})
    if not notif.get("enabled", False):
        print("SKIP: notifications disabled")
        return
    url = (notif.get("slack_webhook_url","") or "").strip()
    if not url:
        print("SKIP: slack_webhook_url not set")
        return

    s = json.loads((Path(cfg["data"].get("output_dir","data"))/"derived/latest_signals.json").read_text(encoding="utf-8"))
    pick = s["pick"]
    conf = float(s.get("confidence",0.5))
    regime = s.get("macro_regime_hint","UNKNOWN")
    alerts = s.get("alerts",[])

    text = f"Foundral v4.1 — Pick: {pick} | confidence {conf:.2f} | regime {regime} | alerts {len(alerts)}"
    r = requests.post(url, json={"text": text}, timeout=15)
    r.raise_for_status()
    print("OK: notification sent")

if __name__ == "__main__":
    main()
