#!/usr/bin/env python3
"""Build the GitHub Pages "mini lecture" from the root cheat sheets.

The root ``*.html`` files are the source of truth: they are what build_pdfs.py
turns into the A4 PDFs, and they work when opened straight from the repository.
This script does not rewrite them. It copies them into ``public/`` and adds the
things a *site* needs that a printable sheet does not:

  * a shared navigation bar (home, topic index, procedure picker, calculator)
  * a "try it on the Nspire" callout per topic, with real TI command names
  * previous / next links, in the reading order taken from index.html
  * a footer linking the two companion projects

The injected chrome is hidden by ``@media print`` in site.css, so printing a
built page still produces a clean sheet. Everything the site needs is local --
no CDN, no tracking, no network calls beyond the two outbound links.

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
import os
import re
import shutil
import socketserver
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_OUT = ROOT / "public"

SITE_URL = "https://franky100-pig.github.io/Stats-CheatSheet/"
REPO_URL = "https://github.com/Franky100-pig/Stats-CheatSheet"
CALC_URL = "https://franky100-pig.github.io/Digital-Nspire-for-Stats/"
CALC_REPO_URL = "https://github.com/Franky100-pig/Digital-Nspire-for-Stats"

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

HREF_RE = re.compile(r'href="([a-z0-9-]+\.html)"')


def topic_order(index_html: str) -> list[str]:
    """Reading order is whatever index.html links, minus the index itself."""
    seen: set[str] = set()
    order: list[str] = []
    for name in HREF_RE.findall(index_html):
        if name == "index.html" or name in seen:
            continue
        seen.add(name)
        order.append(name)
    return order


def nav_html() -> str:
    return f"""<nav class="site-nav">
  <a class="site-brand" href="index.html">Stats <span>Cheat Sheet</span></a>
  <div class="site-links">
    <a class="site-link" href="index.html">Home</a>
    <a class="site-link" href="index.html#topics">Topics</a>
    <a class="site-link" href="index.html#procedure-picker">Which procedure?</a>
    <a class="site-link site-cta" href="{CALC_URL}" target="_blank" rel="noopener">Nspire calculator &#8599;</a>
    <a class="site-link" href="{REPO_URL}" target="_blank" rel="noopener">GitHub &#8599;</a>
  </div>
  <span class="site-spacer"></span>
  <span class="site-topic-jump">AP Statistics &middot; mini lecture notes</span>
</nav>
"""


def footer_html() -> str:
    return f"""<footer class="site-foot">
  <strong>Stats-CheatSheet</strong> &mdash; formula-first AP Statistics notes, with a print-ready A4 PDF for every topic.
  Companion project: <a href="{CALC_URL}" target="_blank" rel="noopener">Digital-Nspire-for-Stats</a>
  runs the same procedures using the TI-Nspire's own command names
  (<a href="{CALC_REPO_URL}" target="_blank" rel="noopener">source</a>).
</footer>
"""


def callout_html(name: str) -> str:
    title, commands = CALC_TIPS[name]
    rows = "\n".join(
        f"    <li><code>{cmd}</code> &mdash; {desc}</li>" for cmd, desc in commands
    )
    return f"""<section class="calc-callout no-print">
  <h2>Try it on the TI-Nspire</h2>
  <p>{title}. These are the calculator's own function names, taken from the
     <a href="{CALC_REPO_URL}" target="_blank" rel="noopener">Digital-Nspire-for-Stats</a> catalogue.</p>
  <ul>
{rows}
  </ul>
  <a class="calc-open" href="{CALC_URL}" target="_blank" rel="noopener">Open the calculator &#8599;</a>
</section>
"""


def pager_html(name: str, order: list[str]) -> str:
    i = order.index(name)
    prev_link = (
        f'<a href="{order[i-1]}"><span>&larr; Previous topic</span>{Path(order[i-1]).stem.replace("-", " ").title()}</a>'
        if i > 0 else '<a class="site-pager-home" href="index.html"><span>Start</span>Back to the index</a>'
    )
    next_link = (
        f'<a class="site-pager-next" href="{order[i+1]}"><span>Next topic &rarr;</span>{Path(order[i+1]).stem.replace("-", " ").title()}</a>'
        if i + 1 < len(order) else '<a class="site-pager-home" href="index.html"><span>End of the current set</span>Back to the index</a>'
    )
    return f'<nav class="site-pager no-print">{prev_link}{next_link}</nav>\n'


def decorate(html: str, name: str, order: list[str]) -> str:
    """Add the site chrome to one page, without touching its printable body."""
    if "site.css" not in html:
        html = html.replace("</head>", '  <link rel="stylesheet" href="site.css" />\n</head>', 1)
    if 'class="site-nav"' not in html:
        html = html.replace("<body>", "<body>\n" + nav_html(), 1)

    if name != "index.html":
        # The last </div> before </body> closes .page. Put the callout inside it
        # so it inherits the sheet's own typography instead of floating outside.
        body_at = html.rfind("</body>")
        close_at = html.rfind("</div>", 0, body_at)
        if close_at < 0:
            raise SystemExit(f"{name}: could not find the closing .page div")
        html = html[:close_at] + callout_html(name) + html[close_at:]
        html = html.replace("</body>", pager_html(name, order) + "</body>", 1)

    html = html.replace("</body>", footer_html() + "</body>", 1)
    return html


def build(out_dir: Path) -> int:
    index_src = (ROOT / "index.html").read_text(encoding="utf-8")
    order = topic_order(index_src)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    shutil.copy(ROOT / "styles.css", out_dir / "styles.css")
    shutil.copy(HERE / "site.css", out_dir / "site.css")

    pdfs = sorted(ROOT.glob("*.pdf"))
    for pdf in pdfs:
        shutil.copy(pdf, out_dir / pdf.name)

    html_files = sorted(ROOT.glob("*.html"))
    for src in html_files:
        (out_dir / src.name).write_text(
            decorate(src.read_text(encoding="utf-8"), src.name, order),
            encoding="utf-8",
        )

    # A broken link in a lecture note is worse than a missing note. Say so loudly.
    problems: list[str] = []
    for name in order:
        if not (ROOT / name).is_file():
            problems.append(f"index.html links {name}, but the file is missing")
        if not (ROOT / name.replace(".html", ".pdf")).is_file():
            problems.append(f"{name} has no matching print-ready PDF")
    for name in CALC_TIPS:
        if name not in order:
            problems.append(f"{name} has a calculator callout but is not linked from index.html")
    if problems:
        for problem in problems:
            print(f"  WARNING  {problem}", flush=True)

    print(f"built  {out_dir}")
    print(f"  {len(html_files)} HTML pages  ({len(order)} topics in reading order)")
    print(f"  {len(pdfs)} PDFs            ({sum(p.stat().st_size for p in pdfs):,} bytes)")
    print(f"  site.css + styles.css + navigation + calculator callouts + pager")
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
