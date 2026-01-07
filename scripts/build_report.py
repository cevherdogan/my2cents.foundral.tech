#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import datetime, timezone
import yaml

def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def fmt_pct(x: float) -> str:
    return f"{x*100:+.2f}%"

def fmt_dd(x: float) -> str:
    return f"{x*100:.1f}%"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = load_config(Path(args.config))
    data_dir = Path(cfg["data"].get("output_dir","data"))
    site_dir = Path(cfg["data"].get("site_dir","site"))
    site_dir.mkdir(parents=True, exist_ok=True)
    (site_dir/"history").mkdir(parents=True, exist_ok=True)

    s = json.loads((data_dir/"derived/latest_signals.json").read_text(encoding="utf-8"))
    pick = s["pick"]
    conf = float(s.get("confidence",0.5))
    regime = s.get("macro_regime_hint","UNKNOWN")
    m = s["metrics"]
    scores = s["scores"]
    alerts = s.get("alerts",[])

    def badge_class():
        if conf >= 0.75: return "good"
        if conf >= 0.60: return "warn"
        return "bad"

    if alerts:
        li = []
        for a in alerts:
            if a["type"]=="DRAWDOWN_BREACH":
                li.append(f"<li><b>DRAWDOWN_BREACH</b> — {a['ticker']} drawdown {fmt_dd(float(a['drawdown']))}</li>")
            elif a["type"]=="PICK_FLIP_CANDIDATE":
                li.append(f"<li><b>PICK_FLIP_CANDIDATE</b> — {a['from']} → {a['to']} margin {float(a['margin']):.2f}</li>")
            else:
                li.append(f"<li><b>{a['type']}</b></li>")
        alerts_html = "<ul class='small'>" + "".join(li) + "</ul>"
    else:
        alerts_html = "<div class='small'>No alerts triggered.</div>"

    ts = datetime.now(timezone.utc)
    ts_label = ts.strftime("%Y-%m-%d %H:%M UTC")
    ts_file = ts.strftime("%Y%m%d_%H%M%S")

    html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Foundral Daily Brief — {pick}</title>
<style>
:root{{--bg:#050a18;--panel:rgba(255,255,255,0.06);--line:rgba(255,255,255,0.12);
--text:rgba(255,255,255,0.92);--muted:rgba(255,255,255,0.65);--muted2:rgba(255,255,255,0.52);
--accent:#45b7ff;--good:#38ef7d;--warn:#ffd166;--bad:#ff6b6b;--shadow:0 22px 60px rgba(0,0,0,0.38);
--radius:18px;--radius2:14px;--mono:ui-monospace,Menlo,Monaco,Consolas,monospace;--sans:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:var(--sans);color:var(--text);
background:radial-gradient(1000px 600px at 15% 10%, rgba(69,183,255,0.18), transparent 60%),
radial-gradient(900px 600px at 85% 15%, rgba(56,239,125,0.12), transparent 60%),
radial-gradient(900px 700px at 50% 90%, rgba(255,209,102,0.10), transparent 62%),var(--bg);}}
.wrap{{max-width:1050px;margin:0 auto;padding:18px 14px 56px}}
.hero{{border:1px solid var(--line);border-radius:var(--radius);
background:linear-gradient(135deg, rgba(69,183,255,0.18), rgba(255,255,255,0.05));box-shadow:var(--shadow);padding:16px}}
h1{{margin:0 0 6px;font-size:20px}}
.sub{{margin:0;color:var(--muted);font-size:13.6px;line-height:1.6}}
.row{{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:10px}}
.badge{{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;border:1px solid rgba(255,255,255,0.14);
background:rgba(69,183,255,0.14);font-size:12.8px;font-weight:650}}
.pill{{display:inline-flex;align-items:center;gap:8px;padding:8px 10px;border-radius:999px;border:1px solid var(--line);
background:rgba(0,0,0,0.22);font-size:12.5px;color:var(--muted)}}
.mono{{font-family:var(--mono)}}
.grid{{display:grid;gap:12px;margin-top:12px}}
@media(min-width:860px){{.grid{{grid-template-columns:1fr 1fr}}}}
.card{{border:1px solid rgba(255,255,255,0.12);border-radius:var(--radius2);background:rgba(0,0,0,0.20);padding:14px}}
.card h2{{margin:0 0 8px;font-size:15.5px}}
.small{{font-size:12.5px;color:var(--muted2);line-height:1.6}}
.kpis{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}}
.kpi{{border:1px solid rgba(255,255,255,0.12);border-radius:14px;background:rgba(0,0,0,0.18);padding:12px}}
.kpi .label{{font-size:12px;color:var(--muted2)}}
.kpi .value{{font-size:15px;font-weight:760;margin-top:4px}}
.good{{color:var(--good)}} .warn{{color:var(--warn)}} .bad{{color:var(--bad)}}
.footer{{margin-top:12px;color:var(--muted2);font-size:12.2px;line-height:1.7}}
</style></head>
<body><div class="wrap">
<section class="hero">
  <h1>Daily Brief — Pick: <span class="mono">{pick}</span></h1>
  <p class="sub">Generated: <span class="mono">{ts_label}</span> · Regime: <span class="mono">{regime}</span></p>
  <div class="row">
    <span class="badge">Confidence: <span class="{badge_class()} mono" style="margin-left:6px">{conf:.2f}</span></span>
    <span class="pill">Canon: <b class="mono">TTD</b></span>
    <span class="pill">Universe: <b class="mono">TTD vs ENPH</b></span>
  </div>
</section>

<div class="grid">
  <section class="card">
    <h2>Scores</h2>
    <div class="kpis">
      <div class="kpi"><div class="label">TTD</div><div class="value mono">{scores["TTD"]:.3f}</div></div>
      <div class="kpi"><div class="label">ENPH</div><div class="value mono">{scores["ENPH"]:.3f}</div></div>
    </div>
    <div class="kpis">
      <div class="kpi"><div class="label">RS 60d (TTD−ENPH)</div><div class="value mono">{fmt_pct(m["rs_60d"])}</div></div>
      <div class="kpi"><div class="label">RS 20d (TTD−ENPH)</div><div class="value mono">{fmt_pct(m["rs_20d"])}</div></div>
    </div>
  </section>

  <section class="card">
    <h2>Survival + Drawdown</h2>
    <div class="kpis">
      <div class="kpi"><div class="label">TTD drawdown (6m)</div><div class="value mono">{fmt_dd(m["TTD"]["drawdown_6m"])}</div></div>
      <div class="kpi"><div class="label">ENPH drawdown (6m)</div><div class="value mono">{fmt_dd(m["ENPH"]["drawdown_6m"])}</div></div>
    </div>
    <div class="kpis">
      <div class="kpi"><div class="label">TTD ret 60d</div><div class="value mono">{fmt_pct(m["TTD"]["ret_60d"])}</div></div>
      <div class="kpi"><div class="label">ENPH ret 60d</div><div class="value mono">{fmt_pct(m["ENPH"]["ret_60d"])}</div></div>
    </div>
  </section>
</div>

<section class="card" style="margin-top:12px">
  <h2>Alerts</h2>
  {alerts_html}
</section>

<section class="card" style="margin-top:12px">
  <h2>Action</h2>
  <div class="small">
    If pick differs from canon (TTD) or if alerts fire, run re-validation:
    verify earnings/guidance + check invalidation rules.
  </div>
</section>

<div class="footer">Foundral v4.1 — Integration prototype. Educational only, not financial advice.</div>
</div></body></html>"""

    (site_dir/"report.html").write_text(html, encoding="utf-8")
    (site_dir/"history"/f"report_{ts_file}.html").write_text(html, encoding="utf-8")
    print("OK: report built")

if __name__ == "__main__":
    main()
