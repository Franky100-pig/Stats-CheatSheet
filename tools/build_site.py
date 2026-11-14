#!/usr/bin/env python3
"""Build the bilingual, chapter-based GitHub Pages lecture from the root sheets.

The root ``*.html`` files are the source of truth: they are what build_pdfs.py
turns into the A4 PDFs, and they stay English-only on purpose -- formula
spellings, symbols and TI-Nspire command names must match the AP exam.

This script does not rewrite them. It copies them into ``public/`` and adds the
things a *book* needs that a printable sheet does not:

  * a contents page built from tools/chapters.py -- the five CED units, 55 topics
  * a fixed chapter sidebar on every sheet, with the current chapter marked
  * an in-page outline built from the sheet's own <h2> sections
  * a breadcrumb (Unit -> sheet) and previous/next links in book order
  * a Chinese annotation layer from tools/i18n_zh.py: a per-section gloss,
    bilingual section headings and a per-topic reading guide
  * a language switch (bilingual / English-only), remembered in localStorage
  * a "try it on the Nspire" callout per topic, with real TI command names

Every injected Chinese element carries ``.zh``, so English-only mode and print
both drop the whole layer. Nothing is fetched from a CDN.

    python3 tools/build_site.py                 # build into public/
    python3 tools/build_site.py --serve        # build, then serve on :8000
    python3 tools/build_site.py --serve 8123   # ...or another port
    STATS_SITE_OUT=/tmp/site python3 tools/build_site.py

The GitHub Actions workflow (.github/workflows/pages.yml) runs the same script
and uploads ``public/`` as the Pages artifact.
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import re
import shutil
import socketserver
from pathlib import Path

import chapters
from i18n_zh import INTRO_HTML, PICKER_ZH, SECTION_ZH, UI

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_OUT = ROOT / "public"

SITE_URL = "https://franky100-pig.github.io/Stats-CheatSheet/"
REPO_URL = "https://github.com/Franky100-pig/Stats-CheatSheet"
CALC_URL = "https://franky100-pig.github.io/Digital-Nspire-for-Stats/"
CALC_REPO_URL = "https://github.com/Franky100-pig/Digital-Nspire-for-Stats"

TOC_PLACEHOLDER = '<div id="chapter-toc" data-generated="chapters"><!-- filled by tools/build_site.py --></div>'

# Commands checked against tinspire_stats.catalog() in Digital-Nspire-for-Stats.
# Do not invent names here: the callout is a promise that the calculator accepts
# exactly what is printed.
CALC_TIPS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "sampling-distributions.html": (
        "Sampling distributions on the Nspire",
        [
            ("normCdf -1,1,0,1", "P(−1 ≤ Z ≤ 1) — the area under a Normal curve"),
            ("invNorm 0.975,0,1", "the critical value z* for a 95% interval"),
            ("binomCdf 10,.3,4", "P(X ≤ 4) for a Binomial count, before a Normal approximation"),
        ],
    ),
    "confidence-intervals.html": (
        "Build these intervals on the Nspire",
        [
            ("zInterval_1Prop 42,100,0.95", "one-proportion z interval"),
            ("zInterval_2Prop 42,100,35,100,0.95", "two-proportion z interval"),
            ("tInterval {3,4,5,6,7},,0.95", "one-sample t interval from a list"),
        ],
    ),
    "z-tests-proportions.html": (
        "Run these tests on the Nspire",
        [
            ("zTest_1Prop 0.5,42,100", "one-proportion z test against p₀ = 0.5"),
            ("zTest_2Prop 42,100,35,100", "two-proportion z test with the pooled p̂"),
            ("normCdf 1.96,9E999,0,1", "the upper tail behind a z statistic"),
        ],
    ),
    "t-tests-means.html": (
        "Run these t procedures on the Nspire",
        [
            ("tTest 0,{3,4,5,6,7}", "one-sample t test — also works on a paired difference list"),
            ("tTest_2Samp {1,2,3},{4,5,6}", "two-sample t test, unpooled by default"),
            ("invT 0.975,24", "the critical value t* with 24 degrees of freedom"),
        ],
    ),
}

H2_RE = re.compile(r'(<h2[^>]*>)(.*?)(</h2>)', re.S)
SUBTITLE_RE = re.compile(r'(<p class="subtitle">.*?</p>)', re.S)
TAG_RE = re.compile(r'<[^>]+>')


def topic_order() -> list[str]:
    """Book order comes from the chapter map, not from whatever index.html links."""
    return chapters.reading_order()


def nav_html() -> str:
    return f"""<nav class="site-nav">
  <a class="site-brand" href="index.html">Stats <span>Cheat Sheet</span></a>
  <div class="site-links">
    <a class="site-link" href="index.html">Contents <span class="zh">{UI['contents']}</span></a>
    <a class="site-link" href="reference.html">Quick Reference <span class="zh">{UI['reference']}</span></a>
    <a class="site-link" href="reference.html#procedure-picker">Which procedure? <span class="zh">{UI['picker']}</span></a>
    <a class="site-link site-cta" href="{CALC_URL}" target="_blank" rel="noopener">Nspire calculator <span class="zh">{UI['calculator']}</span> &#8599;</a>
    <a class="site-link" href="{REPO_URL}" target="_blank" rel="noopener">GitHub <span class="zh">{UI['github']}</span> &#8599;</a>
  </div>
  <span class="site-spacer"></span>
  <span class="site-topic-jump">AP Statistics &middot; mini lecture notes <span class="zh">/ {UI['tagline']}</span></span>
  <button class="lang-btn" id="langToggle" type="button" aria-pressed="false">{UI['lang_both']}</button>
</nav>
"""


def footer_html() -> str:
    return f"""<footer class="site-foot">
  <strong>Stats-CheatSheet</strong> &mdash; formula-first AP Statistics notes, in chapters, with a print-ready A4 PDF for every sheet.
  Companion project: <a href="{CALC_URL}" target="_blank" rel="noopener">Digital-Nspire-for-Stats</a>
  runs the same procedures using the TI-Nspire's own command names
  (<a href="{CALC_REPO_URL}" target="_blank" rel="noopener">source</a>).
  <span class="zh">{UI['footer']}</span>
</footer>
"""


def callout_html(name: str) -> str:
    title, commands = CALC_TIPS[name]
    rows = "\n".join(
        f"    <li><code>{cmd}</code> &mdash; {desc}</li>" for cmd, desc in commands
    )
    return f"""<section class="calc-callout no-print">
  <h2>Try it on the TI-Nspire <span class="zh zh-head">{UI['callout_title']}</span></h2>
  <p>{title}. These are the calculator's own function names, taken from the
     <a href="{CALC_REPO_URL}" target="_blank" rel="noopener">Digital-Nspire-for-Stats</a> catalogue.</p>
  <p class="zh">{UI['callout_lead']}</p>
  <ul>
{rows}
  </ul>
  <a class="calc-open" href="{CALC_URL}" target="_blank" rel="noopener">Open the calculator <span class="zh">/ {UI['callout_button']}</span> &#8599;</a>
</section>
"""


def pager_html(name: str, order: list[str]) -> str:
    i = order.index(name)
    prev_link = (
        f'<a href="{order[i-1]}"><span>&larr; Previous chapter <span class="zh">/ {UI["prev"]}</span></span>{Path(order[i-1]).stem.replace("-", " ").title()}</a>'
        if i > 0 else f'<a class="site-pager-home" href="index.html"><span>Start <span class="zh">/ {UI["start"]} · {UI["back_home"]}</span></span>Back to the contents</a>'
    )
    mid_link = '<a class="site-pager-home" href="index.html">Contents <span class="zh">/ 目录</span></a>'
    next_link = (
        f'<a class="site-pager-next" href="{order[i+1]}"><span>Next chapter &rarr; <span class="zh">/ {UI["next"]}</span></span>{Path(order[i+1]).stem.replace("-", " ").title()}</a>'
        if i + 1 < len(order) else f'<a class="site-pager-home" href="index.html"><span>End of the book <span class="zh">/ {UI["end"]} · {UI["back_home"]}</span></span>Back to the contents</a>'
    )
    return f'<nav class="site-pager no-print">{prev_link}{mid_link}{next_link}</nav>\n'


def inject_chinese(html: str, name: str) -> tuple[str, str | None, list[tuple[str, str]]]:
    """Add the Chinese layer and section anchors. One pair per <h2>."""
    pairs = SECTION_ZH.get(name)
    matches = list(H2_RE.finditer(html))
    if pairs is None or len(pairs) != len(matches):
        have = 0 if pairs is None else len(pairs)
        return html, f"{name}: {len(matches)} <h2> sections but {have} Chinese entries in i18n_zh.py", []

    out: list[str] = []
    headings: list[tuple[str, str]] = []
    last = 0
    for i, (m, (zh_head, zh_gloss)) in enumerate(zip(matches, pairs), 1):
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        existing = re.search(r'id="([^"]+)"', open_tag)
        if existing:
            sec_id = existing.group(1)
        else:
            sec_id = f"sec-{i}"
            open_tag = open_tag.replace("<h2", f'<h2 id="{sec_id}"', 1)
        en_text = TAG_RE.sub("", inner).strip()
        headings.append((en_text, zh_head))
        out.append(html[last:m.start()])
        out.append(f'{open_tag}{inner} <span class="zh zh-head">{zh_head}</span>{close_tag}')
        out.append(f'\n  <div class="zh zh-gloss">{zh_gloss}</div>')
        last = m.end()
    out.append(html[last:])
    html = "".join(out)

    sub = SUBTITLE_RE.search(html)
    if sub and name in INTRO_HTML:
        html = html[:sub.end()] + "\n  " + INTRO_HTML[name] + html[sub.end():]

    if name == "index.html":
        data = json.dumps(PICKER_ZH, ensure_ascii=False)
        html = html.replace("</head>", f"  <script>window.STATS_I18N_ZH = {data};</script>\n</head>", 1)

    return html, None, headings


def decorate(html: str, name: str, order: list[str]) -> tuple[str, str | None]:
    """Add the site chrome, the chapter navigation and the Chinese layer."""
    html, problem, headings = inject_chinese(html, name)

    if "site.css" not in html:
        html = html.replace("</head>", '  <link rel="stylesheet" href="site.css" />\n</head>', 1)
    if '<script src="site.js">' not in html:
        html = html.replace("</head>", '  <script src="site.js"></script>\n</head>', 1)
    if 'class="site-nav"' not in html:
        html = html.replace("<body>", "<body>\n" + nav_html(), 1)

    if name == "index.html":
        # The contents page: the chapter map replaces the placeholder.
        if TOC_PLACEHOLDER not in html:
            return html, "index.html: the chapter-toc placeholder is missing"
        html = html.replace(TOC_PLACEHOLDER, chapters.render_toc())
    else:
        # Sidebar, breadcrumb and the in-page outline. The sidebar goes right
        # after the navigation bar so it reads as part of the chrome.
        html = html.replace("</nav>\n", "</nav>\n" + chapters.render_sidebar(name), 1)
        crumb = chapters.render_breadcrumb(name)
        if crumb:
            html = html.replace('<span class="badge">', crumb + '<span class="badge">', 1)
        if headings:
            outline = chapters.render_outline(headings)
            marker = INTRO_HTML.get(name)
            if marker and marker in html:
                html = html.replace(marker, marker + "\n  " + outline, 1)
            else:
                html = html.replace("</div>\n</body>", outline + "</div>\n</body>", 1)

    if name in CALC_TIPS:
        # The last </div> before </body> closes .page. Put the callout inside it
        # so it inherits the sheet's own typography instead of floating outside.
        body_at = html.rfind("</body>")
        close_at = html.rfind("</div>", 0, body_at)
        if close_at < 0:
            return html, f"{name}: could not find the closing .page div"
        html = html[:close_at] + callout_html(name) + html[close_at:]

    if name in order:
        html = html.replace("</body>", pager_html(name, order) + "</body>", 1)

    html = html.replace("</body>", footer_html() + "</body>", 1)
    return html, problem


def build(out_dir: Path) -> int:
    order = topic_order()

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    shutil.copy(ROOT / "styles.css", out_dir / "styles.css")
    shutil.copy(HERE / "site.css", out_dir / "site.css")
    shutil.copy(HERE / "site.js", out_dir / "site.js")

    pdfs = sorted(ROOT.glob("*.pdf"))
    for pdf in pdfs:
        shutil.copy(pdf, out_dir / pdf.name)

    problems: list[str] = []
    html_files = sorted(ROOT.glob("*.html"))
    for src in html_files:
        decorated, problem = decorate(src.read_text(encoding="utf-8"), src.name, order)
        if problem:
            problems.append(problem)
        (out_dir / src.name).write_text(decorated, encoding="utf-8")

    # A broken link in a lecture note is worse than a missing note. Say so loudly.
    for unit in chapters.UNITS:
        for topic in unit.topics:
            for sheet in topic.sheets:
                if not (ROOT / sheet).is_file():
                    problems.append(f"topic {topic.code} links {sheet}, but the file is missing")
                if not (ROOT / sheet.replace(".html", ".pdf")).is_file():
                    problems.append(f"{sheet} has no matching print-ready PDF")
    for topic in chapters.APPENDICES:
        for sheet in topic.sheets:
            if not (ROOT / sheet).is_file():
                problems.append(f"appendix links {sheet}, but the file is missing")
    for name in CALC_TIPS:
        if name not in order:
            problems.append(f"{name} has a calculator callout but is not in the chapter map")

    # The English-only exam view must really be English-only. Any Chinese text
    # sitting outside a .zh element would survive the language switch, so fail
    # the deploy rather than shipping a half-switched page.
    for built in sorted(out_dir.glob("*.html")):
        text = built.read_text(encoding="utf-8")
        text = re.sub(r"<script\b.*?</script>", "", text, flags=re.S | re.I)
        text = re.sub(r'<button[^>]*id="langToggle"[^>]*>.*?</button>', "", text, flags=re.S)
        text = re.sub(r'<(\w+)[^>]*class="[^"]*\bzh\b[^"]*"[^>]*>.*?</\1>', "", text, flags=re.S)
        text = re.sub(r"<[^>]+>", "", text)
        stray = [ln.strip() for ln in text.splitlines() if re.search(r"[\u4e00-\u9fff]", ln)]
        if stray:
            problems.append(f"{built.name} leaks Chinese into English-only mode: {stray[0][:60]}")

    for problem in problems:
        print(f"  WARNING  {problem}", flush=True)

    zh_pages = sum(1 for p in out_dir.glob("*.html") if 'class="zh' in p.read_text(encoding="utf-8"))
    topics = sum(len(u.topics) for u in chapters.UNITS)
    ready = sum(1 for u in chapters.UNITS for t in u.topics if t.written)
    print(f"built  {out_dir}")
    print(f"  {len(html_files)} HTML pages  ({len(chapters.UNITS)} units, {topics} topics, "
          f"{ready} with sheets, {len(order)} sheets)")
    print(f"  {zh_pages} bilingual pages  ({len(SECTION_ZH)} pages with Chinese glosses)")
    print(f"  {len(pdfs)} PDFs            ({sum(p.stat().st_size for p in pdfs):,} bytes, English only)")
    print(f"  site.css + site.js + styles.css + contents + sidebar + outline + callouts + pager")
    print(f"  live URL  {SITE_URL}")
    total = sum(p.stat().st_size for p in out_dir.rglob("*") if p.is_file())
    print(f"  total     {total:,} bytes")
    return 1 if problems else 0


def serve(out_dir: Path, port: int) -> None:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(out_dir), **kwargs)

    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        print(f"serving {out_dir} at http://127.0.0.1:{port}/  (Ctrl-C to stop)")
        httpd.serve_forever()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=None, help="output folder (default: public/)")
    ap.add_argument("--serve", nargs="?", const=8000, type=int, metavar="PORT",
                    help="build, then serve the result locally")
    args = ap.parse_args()
    out_dir = (args.out or Path(os.environ.get("STATS_SITE_OUT", DEFAULT_OUT))).resolve()
    if out_dir == ROOT:
        raise SystemExit("refusing to write the build into the repository root")
    rc = build(out_dir)
    if args.serve is not None:
        serve(out_dir, args.serve)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
