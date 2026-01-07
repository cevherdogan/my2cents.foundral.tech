#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import yaml

def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def load_latest(raw_dir: Path, ticker: str) -> pd.DataFrame:
    p = raw_dir / f"latest_{ticker}.csv"
    if not p.exists():
        raise FileNotFoundError(f"Missing {p}")

    df = pd.read_csv(p)

    # Normalize Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Normalize Close (robust against junk rows like Close='TTD')
    if "Close" not in df.columns:
        raise KeyError(f"'Close' column not found in {p}. Columns={list(df.columns)}")

    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Drop any junk rows
    df = df.dropna(subset=["Date", "Close"]).sort_values("Date")
    return df[["Date", "Close"]]
def ret_n(df: pd.DataFrame, n: int) -> float:
    if len(df) < n+1:
        n = max(1, len(df)-1)
    if n <= 0:
        return 0.0
    a = float(df["Close"].iloc[-(n+1)])
    b = float(df["Close"].iloc[-1])
    return (b/a)-1.0 if a else 0.0

def drawdown(df: pd.DataFrame, window: int=126) -> float:
    sub = df.tail(window).copy()
    peak = sub["Close"].cummax()
    dd = (sub["Close"]/peak)-1.0
    return float(dd.min()) * -1.0

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def norm_rs(x: float) -> float:
    # clip RS at +/-25% into [-1,1]
    return max(-1.0, min(1.0, x/0.25))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_config(Path(args.config))
    data_dir = Path(cfg["data"].get("output_dir","data"))
    raw_dir = data_dir/"raw"
    derived_dir = data_dir/"derived"
    logs_dir = data_dir/"logs"
    derived_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # macro
    macro_p = derived_dir/"macro_latest.json"
    macro_hint = cfg["scoring"].get("macro_regime_hint","UNKNOWN").upper()
    if macro_p.exists():
        macro_hint = json.loads(macro_p.read_text(encoding="utf-8")).get("macro_regime_hint", macro_hint).upper()

    weights = cfg["scoring"]["weights"]
    bonus_map = cfg["scoring"].get("regime_bonus",{})
    bonus = bonus_map.get(macro_hint, bonus_map.get("UNKNOWN",{}))
    bonus_ttd = float(bonus.get("TTD",0.0))
    bonus_enph = float(bonus.get("ENPH",0.0))

    ttd = load_latest(raw_dir,"TTD")
    enph = load_latest(raw_dir,"ENPH")

    ttd_r20, ttd_r60 = ret_n(ttd,20), ret_n(ttd,60)
    enph_r20, enph_r60 = ret_n(enph,20), ret_n(enph,60)
    rs20, rs60 = ttd_r20 - enph_r20, ttd_r60 - enph_r60

    ttd_dd, enph_dd = drawdown(ttd,126), drawdown(enph,126)
    ttd_surv, enph_surv = 1-clamp01(ttd_dd), 1-clamp01(enph_dd)

    score_ttd = (float(weights["trend"])*norm_rs(rs60) +
                 float(weights["survival"])*((ttd_surv*2)-1) +
                 float(weights["macro"])*bonus_ttd +
                 float(weights["events"])*0.0)
    score_enph = (float(weights["trend"])*norm_rs(-rs60) +
                  float(weights["survival"])*((enph_surv*2)-1) +
                  float(weights["macro"])*bonus_enph +
                  float(weights["events"])*0.0)

    pick = "TTD" if score_ttd >= score_enph else "ENPH"
    margin = abs(score_ttd-score_enph)
    confidence = clamp01(0.5 + margin)

    alerts = []
    thr = cfg.get("thresholds",{})
    dd_breach = float(thr.get("drawdown_breach",0.45))
    if ttd_dd >= dd_breach: alerts.append({"type":"DRAWDOWN_BREACH","ticker":"TTD","drawdown":ttd_dd})
    if enph_dd >= dd_breach: alerts.append({"type":"DRAWDOWN_BREACH","ticker":"ENPH","drawdown":enph_dd})
    flip_margin = float(thr.get("pick_flip_margin",0.10))
    if score_enph > score_ttd + flip_margin:
        alerts.append({"type":"PICK_FLIP_CANDIDATE","from":"TTD","to":"ENPH","margin":score_enph-score_ttd})

    payload = {
      "ts_utc": datetime.now(timezone.utc).isoformat(),
      "macro_regime_hint": macro_hint,
      "metrics":{
        "TTD":{"ret_20d":ttd_r20,"ret_60d":ttd_r60,"drawdown_6m":ttd_dd},
        "ENPH":{"ret_20d":enph_r20,"ret_60d":enph_r60,"drawdown_6m":enph_dd},
        "rs_20d": rs20,
        "rs_60d": rs60
      },
      "scores":{"TTD":score_ttd,"ENPH":score_enph},
      "pick": pick,
      "confidence": confidence,
      "alerts": alerts
    }

    (derived_dir/"latest_signals.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with (logs_dir/"runs.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
    print(f"OK: signals computed. pick={pick} confidence={confidence:.2f} alerts={len(alerts)}")

if __name__ == "__main__":
    main()
