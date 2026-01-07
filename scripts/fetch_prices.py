#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import yaml

def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def fetch_yfinance(ticker: str, lookback_days: int) -> pd.DataFrame:
    import yfinance as yf
    df = yf.download(ticker, period=f"{lookback_days}d", interval="1d", auto_adjust=False, progress=False)
    if df is None or df.empty:
        raise RuntimeError(f"No data returned for {ticker}")
    df = df.reset_index()
    df = df.rename(columns={"Close":"Close"})
    df = df[["Date","Close"]].dropna()
    return df

def load_sample(raw_dir: Path, ticker: str) -> pd.DataFrame:
    p = raw_dir / f"sample_{ticker}.csv"
    if not p.exists():
        raise FileNotFoundError(f"Missing sample file: {p}")
    df = pd.read_csv(p)
    df["Date"] = pd.to_datetime(df["Date"])
    return df[["Date","Close"]].dropna()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_config(Path(args.config))
    tickers = cfg["universe"]["tickers"]
    lookback = int(cfg["data"].get("lookback_days", 365))
    use_live = bool(cfg["data"].get("use_live_fetch", True))

    data_dir = Path(cfg["data"].get("output_dir","data"))
    out_raw = data_dir / "raw"
    out_raw.mkdir(parents=True, exist_ok=True)

    for t in tickers:
        df = None
        err = None
        if use_live:
            try:
                df = fetch_yfinance(t, lookback)
            except Exception as e:
                err = e
        if df is None:
            df = load_sample(out_raw, t)

        ts = pd.Timestamp.utcnow().strftime("%Y%m%d_%H%M%S")
        out = out_raw / f"prices_{t}_{ts}.csv"
        df.to_csv(out, index=False)
        # latest pointer
        (out_raw / f"latest_{t}.csv").write_text(out.read_text(encoding="utf-8"), encoding="utf-8")

    print("OK: prices fetched (live or sample fallback)")

if __name__ == "__main__":
    main()
