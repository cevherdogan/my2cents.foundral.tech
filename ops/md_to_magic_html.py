#!/usr/bin/env python3
"""
Foundral Magic HTML generator (no external deps)

- Walks one or more directories
- Converts *.md -> *.html next to it
- Skips if HTML is newer unless --force
"""

from __future__ import annotations
import argparse
import html
import os
import re
from pathlib import Path
from datetime import datetime

CSS = r"""
:root{--bg:#0b1220;--card:rgba(15,27,51,.82);--text:#eaf0ff;--muted:#a9b6d5;--line:rgba(255,255,255,.12);
--accent:#7dd3fc;--accent2:#a78bfa;}
*{box-sizing:border-box}
body{margin:0;font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;
background:radial-gradient(1200px 600px at 16% -10%, rgba(125,211,252,.22), transparent 60%),
radial-gradient(900px 520px at 110% 12%, rgba(167,139,250,.18), transparent 55%), var(--bg);
color:var(--text);line-height:1.55}
.wrap{max-width:980px;margin:0 auto;padding:28px 18px 64px}
.hero{border:1px solid var(--line);border-radius:18px;background:linear-gradient(135deg, rgba(125,211,252,.18), rgba(167,139,250,.14));
padding:18px 16px;margin:10px 0 16px}
.hero h1{margin:0 0 6px;font-size:1.55rem}
.meta{color:var(--muted);font-size:.95rem}
.card{border:1px solid var(--line);border-radius:16px;background:var(--card);padding:16px;margin:14px 0}
h2{margin:18px 0 8px;font-size:1.2rem}
h3{margin:14px 0 6px;font-size:1.05rem}
p{margin:10px 0;color:var(--text)}
ul,ol{padding-left:22px}
li{margin:6px 0}
blockquote{margin:10px 0;padding:10px 12px;border-left:3px solid var(--accent);background:rgba(125,211,252,.08);
border-radius:12px}
code{background:rgba(0,0,0,.25);border:1px solid var(--line);padding:2px 6px;border-radius:8px}
pre{background:rgba(0,0,0,.25);border:1px solid var(--line);padding:12px;border-radius:12px;overflow:auto}
a{color:var(--accent)}
hr{border:none;border-top:1px solid var(--line);margin:14px 0}
.footer{color:var(--muted);font-size:.9rem;margin-top:18px}
.tableline{white-space:pre-wrap}
"""

def md_to_html_body(md: str) -> str:
    lines = md.splitlines()
    out = []
    in_ul = in_ol = in_code = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    for line in lines:
        if line.strip().startswith("```"):
            close_lists()
            if not in_code:
                in_code = True
                out.append("<pre><code>")
            else:
                in_code = False
                out.append("</code></pre>")
            continue

        if in_code:
            out.append(html.escape(line))
            continue

        # headings
        if line.startswith("# "):
            close_lists()
            out.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
            continue
        if line.startswith("## "):
            close_lists()
            out.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
            continue
        if line.startswith("### "):
            close_lists()
            out.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
            continue

        # blockquote
        if line.startswith("> "):
            close_lists()
            out.append(f"<blockquote>{inline_format(line[2:].strip())}</blockquote>")
            continue

        # ordered list: "1) thing"
        m = re.match(r"^\s*\d+\)\s+(.*)$", line)
        if m:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline_format(m.group(1).strip())}</li>")
            continue

        # unordered list: "- thing"
        if line.startswith("- "):
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_format(line[2:].strip())}</li>")
            continue

        # tables (simple): keep as pre for readability
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            close_lists()
            out.append(f"<pre class='tableline'>{html.escape(line)}</pre>")
            continue

        # blank
        if not line.strip():
            close_lists()
            continue

        close_lists()
        out.append(f"<p>{inline_format(line.strip())}</p>")

    # close open structures
    if in_code:
        out.append("</code></pre>")
    close_lists()

    return "\n".join(out)

def inline_format(text: str) -> str:
    # escape first, then do simple **bold** and *italic*
    t = html.escape(text)

    # links: [text](url)
    ## t = re.sub(r"$begin:math:display$\(\[\^$end:math:display$]+)\]$begin:math:text$\(\[\^\)\]\+\)$end:math:text$", r"<a href='\2'>\1</a>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<a href='\2'>\1</a>", t)

    # bold/italic
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
    return t

def wrap(title: str, rel_path: str, body: str) -> str:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>{html.escape(title)}</h1>
      <div class="meta">Foundral • Magic HTML mirror • {html.escape(rel_path)} • {stamp}</div>
    </div>
    <div class="card">
      {body}
    </div>
    <div class="footer">Generated from Markdown. Edit the <code>.md</code> file and regenerate.</div>
  </div>
</body>
</html>
"""

def should_build(md_path: Path, html_path: Path, force: bool) -> bool:
    if force:
        return True
    if not html_path.exists():
        return True
    return md_path.stat().st_mtime > html_path.stat().st_mtime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Repo root (default: .)")
    ap.add_argument("--dirs", nargs="+", default=["templates", "docs", "ops"],
                    help="Directories to scan (default: templates docs ops)")
    ap.add_argument("--force", action="store_true", help="Regenerate even if HTML is newer")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    generated = 0
    skipped = 0

    for d in args.dirs:
        target = root / d
        if not target.exists():
            continue
        for md_path in target.rglob("*.md"):
            html_path = md_path.with_suffix(".html")
            if not should_build(md_path, html_path, args.force):
                skipped += 1
                continue

            md_text = md_path.read_text(encoding="utf-8", errors="replace")
            body = md_to_html_body(md_text)

            # title: use first H1 if present, else file stem
            first_h1 = None
            for line in md_text.splitlines():
                if line.startswith("# "):
                    first_h1 = line[2:].strip()
                    break
            title = first_h1 or md_path.stem.replace("_", " ")

            rel_path = str(md_path.relative_to(root))
            html_doc = wrap(title, rel_path, body)
            html_path.write_text(html_doc, encoding="utf-8")
            generated += 1

    print(f"Generated: {generated} HTML files")
    print(f"Skipped:   {skipped} (already up-to-date)")

if __name__ == "__main__":
    main()

