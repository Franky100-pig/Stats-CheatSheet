# -*- coding: utf-8 -*-
"""The book's table of contents: AP Statistics units, in CED order.

One source of truth for the chapter structure. tools/build_site.py uses it to
render the contents page, the fixed chapter sidebar, the per-sheet outline and
the breadcrumb, so adding a sheet means editing exactly this file (plus its
Chinese glosses in i18n_zh.py).

Unit numbering follows the AP Statistics Course and Exam Description:
1 Exploring One-Variable Data, 2 Exploring Two-Variable Data,
3 Collecting Data, 4 Probability/Random Variables, 5 Sampling Distributions,
6 Inference for Proportions, 7 Inference for Means, 8 Chi-Square,
9 Inference for Slopes.
"""

from __future__ import annotations

from dataclasses import dataclass

REPO_URL = "https://github.com/Franky100-pig/Stats-CheatSheet"
CALC_URL = "https://franky100-pig.github.io/Digital-Nspire-for-Stats/"


@dataclass(frozen=True)
class Sheet:
    en: str
    zh: str
    href: str | None = None
    pdf: bool = False
    note_en: str | None = None
    note_zh: str | None = None


@dataclass(frozen=True)
class Unit:
    num: int
    en: str
    zh: str
    blurb_en: str
    blurb_zh: str
    sheets: tuple[Sheet, ...] = ()

    @property
    def anchor(self) -> str:
        return f"unit-{self.num:02d}"

    @property
    def label(self) -> str:
        return f"Unit {self.num:02d}"

    @property
    def ready(self) -> bool:
        return any(s.href for s in self.sheets)


UNITS: tuple[Unit, ...] = (
    Unit(1, "Exploring One-Variable Data", "单变量数据探索",
         "Categorical and quantitative displays, centre, spread, outliers and the Normal model.",
         "分类与定量数据的图表、中心与离散程度、离群点与正态模型。",
         (Sheet("Displaying and describing one-variable data", "单变量数据的图表与描述"),)),
    Unit(2, "Exploring Two-Variable Data", "双变量数据探索",
         "Scatterplots, correlation, least-squares regression, residuals and transformations.",
         "散点图、相关系数、最小二乘回归、残差与变量变换。",
         (Sheet("Regression and two-variable relationships", "回归与双变量关系"),)),
    Unit(3, "Collecting Data", "数据收集",
         "Sampling methods, experimental design, blocking, confounding and scope of inference.",
         "抽样方法、实验设计、区组、混杂变量与结论可推广范围。",
         (Sheet("Sampling and experiments", "抽样与实验"),)),
    Unit(4, "Probability, Random Variables & Distributions", "概率、随机变量与分布",
         "Conditional probability, independence, Binomial / Geometric models, linear combinations.",
         "条件概率、独立性、二项／几何分布与随机变量的线性组合。",
         (Sheet("Probability and random variables", "概率与随机变量"),)),
    Unit(5, "Sampling Distributions", "抽样分布",
         "Parameters vs. statistics, the Central Limit Theorem, standard errors and R-I-N conditions.",
         "参数与统计量、中心极限定理、标准误与 R-I-N 条件。",
         (Sheet("Sampling Distributions & the CLT", "抽样分布与中心极限定理",
                "sampling-distributions.html", True),)),
    Unit(6, "Inference for Categorical Data: Proportions", "分类数据推断：比例",
         "One- and two-proportion z intervals and tests, including the pooled p̂c.",
         "单比例／双比例 z 区间与检验，以及只在检验里出现的合并比例 p̂c。",
         (
             Sheet("Confidence Intervals (z & t)", "置信区间（z 与 t）",
                   "confidence-intervals.html", True,
                   "Also covers Unit 7 means", "同时覆盖第 7 单元的均值区间"),
             Sheet("Hypothesis Testing & z-Tests for Proportions", "假设检验与比例的 z 检验",
                   "z-tests-proportions.html", True),
         )),
    Unit(7, "Inference for Quantitative Data: Means", "定量数据推断：均值",
         "One-sample, paired and two-sample t procedures; Welch degrees of freedom.",
         "单样本、配对与双样本 t 推断，以及 Welch 自由度。",
         (
             Sheet("t-Tests for Means & Paired Data", "均值的 t 检验与配对数据",
                   "t-tests-means.html", True),
             Sheet("t intervals (see the shared interval sheet in Unit 6)",
                   "t 区间（见第 6 单元共用的区间讲义）"),
         )),
    Unit(8, "Inference for Categorical Data: Chi-Square", "分类数据推断：卡方",
         "Goodness-of-fit, homogeneity, independence, expected counts and degrees of freedom.",
         "拟合优度、同质性、独立性、期望频数与自由度。",
         (Sheet("Chi-square tests", "卡方检验"),)),
    Unit(9, "Inference for Quantitative Data: Slopes", "定量数据推断：斜率",
         "LSRL, r and r², the standard error of the slope and a t interval/test for β.",
         "回归直线、r 与 r²、斜率标准误，以及对 β 的 t 区间与检验。",
         (Sheet("Inference for the slope", "斜率的推断"),)),
)

APPENDICES: tuple[Sheet, ...] = (
    Sheet("Quick Reference & Tools", "速查与工具", "reference.html", False,
          "Procedure picker, notation table, exam traps and roadmap",
          "推断程序选择器、记号表、易错点与后续计划"),
    Sheet("TI-Nspire calculator", "TI-Nspire 计算器", CALC_URL, False,
          "Opens the companion project in a new tab", "在新标签打开伴生项目"),
    Sheet("Source repository", "源码仓库", REPO_URL, False,
          "HTML sources, PDFs and the site builder", "HTML 源文件、PDF 与站点构建器"),
)


def _external(href: str | None) -> bool:
    return bool(href) and href.startswith("http")


def reading_order() -> list[str]:
    """Sheet files in book order, first appearance only (no duplicates)."""
    seen: set[str] = set()
    order: list[str] = []
    for unit in UNITS:
        for sheet in unit.sheets:
            if sheet.href and not _external(sheet.href) and sheet.href.endswith(".html") and sheet.href not in seen:
                seen.add(sheet.href)
                order.append(sheet.href)
    return order


def unit_for(href: str) -> Unit | None:
    for unit in UNITS:
        if any(s.href == href for s in unit.sheets):
            return unit
    return None


def sheet_for(href: str) -> Sheet | None:
    for unit in UNITS:
        for sheet in unit.sheets:
            if sheet.href == href:
                return sheet
    return None


def _sheet_link(sheet: Sheet, current: str | None = None) -> str:
    if not sheet.href:
        return (f'<li class="toc-sheet toc-planned"><span>{sheet.en} <span class="zh">{sheet.zh}</span></span>'
                f'<span class="toc-tag">计划中 / planned</span></li>')
    ext = ' target="_blank" rel="noopener"' if _external(sheet.href) else ""
    cur = ' aria-current="page"' if sheet.href == current else ""
    note = ""
    if sheet.note_en:
        note = f'<span class="toc-sheet-note">{sheet.note_en} <span class="zh">/ {sheet.note_zh}</span></span>'
    pdf = ""
    if sheet.pdf:
        pdf = f'<a class="toc-pdf" href="{sheet.href.replace(".html", ".pdf")}">PDF</a>'
    return (f'<li class="toc-sheet"><a href="{sheet.href}"{ext}{cur}>{sheet.en} <span class="zh">{sheet.zh}</span></a>'
            f'{pdf}{note}</li>')


def render_toc() -> str:
    """The full contents page, injected into index.html's placeholder."""
    out = ['<nav class="chapter-toc" aria-label="Table of contents">',
           '<div class="toc-legend">',
           '<span><i class="toc-dot toc-dot-ready"></i>已写 / ready</span>',
           '<span><i class="toc-dot toc-dot-planned"></i>计划中 / planned</span>',
           '<span class="zh">点标题进入讲义，PDF 为同内容 A4 打印版</span>',
           '</div>', '<ol class="toc-units">']
    for unit in UNITS:
        status = ('<span class="toc-status toc-status-ready">已写 / ready</span>'
                  if unit.ready else '<span class="toc-status toc-status-planned">计划中 / planned</span>')
        out.append(f'<li class="toc-unit" id="{unit.anchor}">')
        out.append(f'<div class="toc-unit-head"><span class="toc-unit-num">{unit.label}</span>'
                   f'<div class="toc-unit-title">{unit.en} <span class="zh">{unit.zh}</span></div>{status}</div>')
        out.append(f'<p class="toc-unit-blurb">{unit.blurb_en} <span class="zh">{unit.blurb_zh}</span></p>')
        out.append('<ol class="toc-sheets">')
        for sheet in unit.sheets:
            out.append(_sheet_link(sheet))
        out.append('</ol></li>')
    out.append('</ol>')
    out.append('<h3 class="toc-appendix-title">Appendices <span class="zh">附录</span></h3>')
    out.append('<ol class="toc-appendix">')
    for sheet in APPENDICES:
        out.append(_sheet_link(sheet))
    out.append('</ol></nav>')
    return "\n".join(out) + "\n"


def render_sidebar(current: str) -> str:
    """The fixed chapter navigation shown on every sheet and appendix."""
    out = ['<aside class="chapter-sidebar" aria-label="Chapter navigation">',
           '<a class="sidebar-home" href="index.html">&larr; 目录 <span class="zh">Contents</span></a>',
           '<details class="sidebar-details" id="sidebarDetails" open>',
           '<summary>Units 01&ndash;09 <span class="zh">章节</span></summary>',
           '<ol class="sidebar-units">']
    for unit in UNITS:
        out.append(f'<li class="sidebar-unit{" is-active" if unit_for(current) is unit else ""}">'
                   f'<a class="sidebar-unit-head" href="index.html#{unit.anchor}">'
                   f'<span class="sidebar-num">{unit.num:02d}</span>'
                   f'<span class="sidebar-unit-title">{unit.en} <span class="zh">{unit.zh}</span></span></a>')
        ready = [s for s in unit.sheets if s.href and not _external(s.href)]
        if ready:
            out.append('<ol class="sidebar-sheets">')
            for sheet in ready:
                cls = ' class="is-current"' if sheet.href == current else ""
                out.append(f'<li><a href="{sheet.href}"{cls}>{sheet.en} <span class="zh">{sheet.zh}</span></a></li>')
            out.append('</ol>')
        out.append('</li>')
    out.append('</ol></details>')
    out.append('<div class="sidebar-appendix"><span class="sidebar-appendix-title">附录 / Appendices</span>')
    for sheet in APPENDICES:
        ext = ' target="_blank" rel="noopener"' if _external(sheet.href) else ""
        cls = ' class="is-current"' if sheet.href == current else ""
        out.append(f'<a href="{sheet.href}"{ext}{cls}>{sheet.en} <span class="zh">{sheet.zh}</span></a>')
    out.append('</div>')
    crumb_unit = unit_for(current)
    crumb_sheet = sheet_for(current)
    if crumb_unit and crumb_sheet:
        out.append(f'<p class="sidebar-now">当前 / Now reading<br><strong>{crumb_sheet.en} '
                   f'<span class="zh">{crumb_sheet.zh}</span></strong><br>'
                   f'<span>{crumb_unit.label} · {crumb_unit.en}</span></p>')
    out.append('</aside>')
    return "\n".join(out) + "\n"


def render_outline(headings: list[tuple[str, str]]) -> str:
    """An in-page table of contents built from a sheet's <h2> sections."""
    out = ['<nav class="section-outline" aria-label="In this chapter">',
           '<h3>In this chapter <span class="zh">本章小节</span></h3>', '<ol>']
    for i, (en, zh) in enumerate(headings, 1):
        out.append(f'<li><a href="#sec-{i}">{en} <span class="zh">{zh}</span></a></li>')
    out.append('</ol></nav>')
    return "\n".join(out) + "\n"


def render_breadcrumb(current: str) -> str:
    unit = unit_for(current)
    sheet = sheet_for(current)
    if unit and sheet:
        mid = (f'<a href="index.html#{unit.anchor}">{unit.label} · {unit.en} '
               f'<span class="zh">{unit.zh}</span></a>')
        return (f'<nav class="chapter-crumb"><a href="index.html">目录 <span class="zh">Contents</span></a>'
                f' <span class="crumb-sep">/</span> {mid} <span class="crumb-sep">/</span> '
                f'<strong>{sheet.en}</strong></nav>\n  ')
    if current == "reference.html":
        return ('<nav class="chapter-crumb"><a href="index.html">目录 <span class="zh">Contents</span></a>'
                ' <span class="crumb-sep">/</span> <strong>Appendix A · Quick Reference</strong></nav>\n  ')
    return ""
