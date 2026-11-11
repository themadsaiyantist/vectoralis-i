"""The dashboard: one self-contained HTML page built from the records. No script, light and dark."""
from __future__ import annotations

import datetime
import html

from . import checks, records

STYLE = """
:root{--bg:#f7f7f5;--card:#fff;--ink:#16181d;--soft:#5d6470;--line:#e3e4e8;--good:#1f8a4c;--warn:#b7791f;--bad:#c0392b;--bar:#dfe1e6}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--card:#171a21;--ink:#e8eaee;--soft:#9aa3b2;--line:#262b35;--good:#4ec27f;--warn:#e0a948;--bad:#ef6b5c;--bar:#2a303b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1080px;margin:0 auto;padding:32px 20px 56px}h1{font-size:26px;margin:0 0 4px}h2{font-size:15px;margin:0 0 12px;letter-spacing:.02em}
.sub{color:var(--soft);margin:0 0 24px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}.wide{grid-column:1/-1}
.stat{display:flex;gap:28px;flex-wrap:wrap}.stat div{min-width:96px}.stat b{display:block;font-size:26px;line-height:1.1}.stat span{color:var(--soft);font-size:13px}
ul{margin:0;padding:0;list-style:none}li{padding:6px 0;border-top:1px solid var(--line)}li:first-child{border-top:0}
.row{display:flex;align-items:center;gap:12px;padding:6px 0}.row span:first-child{flex:0 0 38%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bar{flex:1;height:8px;border-radius:8px;background:var(--bar);overflow:hidden}.bar i{display:block;height:100%;background:var(--good)}
.num{flex:0 0 64px;text-align:right;color:var(--soft);font-variant-numeric:tabular-nums}.good{color:var(--good)}.warn{color:var(--warn)}.bad{color:var(--bad)}
.none{color:var(--soft)}code{font:13px ui-monospace,SFMono-Regular,Menlo,monospace}footer{margin-top:24px;color:var(--soft);font-size:13px}
"""


def _list(items, empty) -> str:
    if not items:
        return f'<p class="none">{html.escape(empty)}</p>'
    return "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"


def build(proj) -> str:
    """The whole page as one string."""
    tracker, todo = proj.read("tracker.md"), proj.read("todo.md")
    rows = records.tracker_rows(tracker)
    sections = {}
    for row in rows:
        done, total = sections.get(row["section"], (0, 0))
        marks = list(row["marks"].values())
        sections[row["section"]] = (done + marks.count(records.DONE), total + marks.count(records.DONE) + marks.count(records.OPEN))
    done = sum(d for d, _ in sections.values())
    total = sum(t for _, t in sections.values())
    boxes = records.todo_boxes(todo)
    mine = [b["text"] for b in boxes if not b["yours"] and not b["done"]]
    yours = [b["text"] for b in boxes if b["yours"] and not b["done"]]
    fails = records.failures(proj.read("failures.md"))
    open_fails = [f"{f['date']} · {f['title']}" for f in fails if f["open"]]
    locks = records.locks(proj.read("locks.md"))
    flags = checks.stale(proj)
    spent = checks.budget(proj)
    over = spent["total"] > spent["cap"]
    bars = "".join(
        f'<div class="row"><span>{html.escape(name or "Tracker")}</span><div class="bar"><i style="width:{(d * 100 // t) if t else 0}%"></i></div>'
        f'<span class="num">{d} / {t}</span></div>'
        for name, (d, t) in sections.items()
    ) or '<p class="none">The tracker has no rows yet.</p>'
    now = records.section_text(todo, "Now")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(proj.root.name)} · harness</title><style>{STYLE}</style></head><body><main>
<h1>{html.escape(proj.root.name)}</h1>
<p class="sub">The {proj.profile} harness · built from <code>harness/</code> on {stamp}</p>
<div class="grid">
<section class="card wide"><div class="stat">
<div><b>{done} / {total}</b><span>boxes done</span></div>
<div><b>{len(mine)}</b><span>open for the agent</span></div>
<div><b>{len(yours)}</b><span>open for you</span></div>
<div><b class="{'bad' if open_fails else 'good'}">{len(open_fails)}</b><span>open failures</span></div>
<div><b class="{'warn' if flags else 'good'}">{len(flags)}</b><span>stale flags</span></div>
<div><b class="{'bad' if over else 'good'}">{spent['total']}</b><span>tokens always loaded, cap {spent['cap']}</span></div>
</div></section>
<section class="card wide"><h2>Now</h2>{_list([line.strip() for line in now.splitlines() if line.strip()], "No handoff written yet.")}</section>
<section class="card wide"><h2>Open work</h2>{bars}</section>
<section class="card"><h2>Next for the agent</h2>{_list(mine[:8], "Nothing open.")}</section>
<section class="card"><h2>Yours</h2>{_list(yours[:8], "Nothing waits on you.")}</section>
<section class="card"><h2>Open failures</h2>{_list(open_fails, "None open.")}</section>
<section class="card"><h2>Stale</h2>{_list(flags, "Every record is backed by the repository.")}</section>
<section class="card"><h2>Locks</h2>{_list(locks, "Nothing is locked.")}</section>
<section class="card"><h2>Always loaded</h2>{_list([f"{name} · about {tokens} tokens" for name, _, tokens in spent["rows"]], "Nothing.")}</section>
</div>
<footer>Vectoralis · one page, built from the files, on your machine. Run <code>vectoralis dashboard</code> to refresh it.</footer>
</main></body></html>
"""
