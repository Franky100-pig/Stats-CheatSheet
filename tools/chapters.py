# -*- coding: utf-8 -*-
"""The book's table of contents: the AP Statistics course framework, Fall 2026.

One source of truth for the chapter structure. tools/build_site.py uses it to
render the contents page, the unit sidebar, the breadcrumbs and the
previous/next links, so adding a sheet means editing exactly this file (plus
its Chinese glosses in i18n_zh.py).

The outline follows the College Board "AP Statistics Course and Exam
Description, effective Fall 2026": **five** units, 55 topics.

    Unit 1  Exploring One-Variable Data and Collecting Data   20-30%   ~26 periods
    Unit 2  Probability, Random Variables, and Distributions  15-25%   ~24 periods
    Unit 3  Inference for Categorical Data: Proportions       15-25%   ~30 periods
    Unit 4  Inference for Quantitative Data: Means             10-20%   ~18 periods
    Unit 5  Regression Analysis                                10-20%   ~9 periods

Note for anyone who knew the older CED: the units were renumbered, and the
Fall 2026 framework has no topic on inference for a regression slope --
Unit 5 stops at least-squares regression (Topic 5.5).

Each topic carries its own Chinese breakdown of the knowledge points. Those
are our summaries, not College Board's wording. Formulas, symbols and
TI-Nspire command names are never translated.
"""

from __future__ import annotations

from dataclasses import dataclass

REPO_URL = "https://github.com/Franky100-pig/Stats-CheatSheet"
CALC_URL = "https://franky100-pig.github.io/Digital-Nspire-for-Stats/"


@dataclass(frozen=True)
class Topic:
    code: str
    en: str
    zh: str
    points: tuple[str, ...] = ()
    sheets: tuple[str, ...] = ()

    @property
    def written(self) -> bool:
        return bool(self.sheets)


@dataclass(frozen=True)
class Unit:
    num: int
    en: str
    zh: str
    weight: str
    periods: str
    topics: tuple[Topic, ...] = ()

    @property
    def anchor(self) -> str:
        return f"unit-{self.num:02d}"

    @property
    def label(self) -> str:
        return f"Unit {self.num:02d}"

    @property
    def ready(self) -> bool:
        return any(t.written for t in self.topics)

    def topics_for(self, sheet: str) -> list[Topic]:
        return [t for t in self.topics if sheet in t.sheets]


def _t(code, en, zh, points, sheets=()):
    return Topic(code=code, en=en, zh=zh, points=tuple(points), sheets=tuple(sheets))


UNITS: tuple[Unit, ...] = (
    Unit(
        1, "Exploring One-Variable Data and Collecting Data", "单变量数据探索与数据收集",
        "20–30%", "~26",
        (
            _t("1.1", "Introducing Statistics: What Can We Learn from Data?", "统计研究入门：数据能回答什么",
               ("统计研究的组成：总体与样本、变量、数据、参数与统计量",
                "研究问题必须可回答：所需数据能被收集与分析，且不因结果改口",
                "描述统计与推断统计的分工；相关不等于因果")),
            _t("1.2", "Variables", "变量",
               ("分类变量与定量变量；单变量与双变量",
                "离散与连续定量变量：计数还是测量",
                "解释变量、响应变量与混杂变量")),
            _t("1.3", "Tabular Representation and Summary Statistics for One Categorical Variable",
               "单个分类变量：表格与汇总统计",
               ("频数表、相对频率与百分比",
                "条形图读数；众数与类别数",
                "从表格里比较两个分类变量的分布")),
            _t("1.4", "Graphical Representations for One Categorical Variable", "单个分类变量：图形表示",
               ("条形图、饼图、点图、频数图各自的用途",
                "从图形读出类别与相对频率",
                "按图形选择与比较：类别顺序、集中位置")),
            _t("1.5", "Graphical Representations for One Quantitative Variable", "单个定量变量：图形表示",
               ("直方图、箱线图、点图、茎叶图",
                "选图依据：变量类型、类别数、是否比较两组",
                "直方图的分组与组距")),
            _t("1.6", "Descriptions for One Quantitative Variable Distributions", "单个定量变量分布的描述",
               ("形状：对称、右偏、左偏、双峰",
                "异常值与缺口；中心与离散程度",
                "写完整描述：shape, outliers, center, spread")),
            _t("1.7", "Summary Statistics for One Quantitative Variable", "单个定量变量：汇总统计",
               ("均值、中位数、众数各自的含义与敏感性",
                "极差、四分位距、标准差",
                "位置：z 分数与四分位位置")),
            _t("1.8", "Graphical Representations of Summary Statistics for One Quantitative Variable",
               "汇总统计的图形表示",
               ("箱线图五个数的含义与异常值规则",
                "用箱线图比较两个分布",
                "异常值如何影响均值与中位数")),
            _t("1.9", "Comparisons of the Distributions for One Quantitative Variable", "两个定量分布的比较",
               ("比较形状、中心、离散与异常值",
                "用具体数值支撑比较结论",
                "为什么不能只看一个数字")),
            _t("1.10", "The Investigative Question Revisited and Data Collection", "回到研究问题与数据收集",
               ("观察性研究与实验的区别",
                "随机抽样与随机分配不是一回事",
                "回答研究问题需要收集哪些数据")),
            _t("1.11", "Random Sampling", "随机抽样",
               ("简单随机抽样 SRS、分层、整群、系统、便利抽样",
                "根据描述判断用的是哪种抽样方法",
                "各方法的适用场景与成本")),
            _t("1.12", "Potential Problems with Sampling", "抽样中的问题",
               ("抽样偏差、无应答、自愿应答、覆盖不足",
                "判断偏差方向：偏高还是偏低，并给证据",
                "为什么有偏样本不能推广到总体")),
            _t("1.13", "Experimental Design", "实验设计",
               ("处理、响应、控制组、随机分配",
                "完全随机、区块、重复；确定性与随机性实验",
                "什么情况下可以说差异是处理造成的")),
        )),
    Unit(
        2, "Probability, Random Variables, and Probability Distributions", "概率、随机变量与概率分布",
        "15–25%", "~24",
        (
            _t("2.1", "Tabular and Graphical Representations for the Distributions of Two Categorical Variables",
               "两个分类变量的表与图",
               ("列联表：联合、边际、条件分布",
                "分段图与堆叠条形图",
                "用相对频率比较两个分类变量")),
            _t("2.2", "Summary Statistics for Two Categorical Variables", "两个分类变量的汇总统计",
               ("边际分布 vs 条件分布",
                "从列联表算百分比与比值",
                "「总体中的比例」vs「这一组里的比例」")),
            _t("2.3", "Estimating Probabilities Using Simulation", "用模拟估计概率",
               ("用随机模拟估计一个概率",
                "重复次数越多估计越稳定",
                "模拟结果与精确概率的对照")),
            _t("2.4", "Introduction to Probability", "概率入门",
               ("概率的取值 0 到 1；试验、结果、样本空间",
                "P(A) 与 P(not A) = 1 − P(A)",
                "概率是长期比例")),
            _t("2.5", "Mutually Exclusive Events", "互斥事件",
               ("互斥与不互斥；加法法则",
                "P(A∪B) = P(A) + P(B) − P(A∩B)",
                "补集与 Venn 图")),
            _t("2.6", "Conditional Probability", "条件概率",
               ("P(A|B) = P(A∩B)/P(B)",
                "限制样本空间：把 B 当成新的总体",
                "用表格或树状图解读")),
            _t("2.7", "Independent Events and Unions of Events", "独立事件与并集",
               ("独立：P(A∩B) = P(A)P(B)",
                "互斥与独立通常不能同时成立",
                "「至少一个」用补事件算")),
            _t("2.8", "Introduction to Random Variables and Probability Distributions", "随机变量与概率分布",
               ("随机变量把结果映射成数值；离散与连续",
                "概率分布：每个取值有概率，总和为 1",
                "分布图与取值范围")),
            _t("2.9", "Parameters of Random Variables", "随机变量的参数",
               ("期望 μ：长期平均",
                "方差 σ² 与标准差 σ",
                "在具体情境里解释均值与标准差")),
            _t("2.10", "The Binomial Distribution", "二项分布",
               ("条件：次数固定、各次独立、成功概率不变",
                "μ = np，σ = √(np(1−p))",
                "binomPdf / binomCdf 的用法")),
            _t("2.11", "The Normal Distribution", "正态分布",
               ("正态曲线性质：对称，均值=中位数=众数",
                "经验法则 68–95–99.7",
                "normCdf 求面积、invNorm 求分位数")),
            _t("2.12", "Sampling Distributions and the Central Limit Theorem", "抽样分布与中心极限定理",
               ("样本均值的抽样分布：中心 μ、标准误 σ/√n",
                "样本比例的抽样分布与 Large Counts",
                "CLT：n 够大时近似正态；抽样分布 ≠ 总体分布"),
               sheets=("sampling-distributions.html",)),
        )),
    Unit(
        3, "Inference for Categorical Data: Proportions", "分类数据推断：比例",
        "15–25%", "~30",
        (
            _t("3.1", "Estimators", "估计量",
               ("参数是固定未知数，估计量是样本算出来的数",
                "无偏性：估计量的期望等于参数",
                "用哪个统计量去估计哪个参数")),
            _t("3.2", "Sampling Distributions for Sample Proportions", "样本比例的抽样分布",
               ("p̂ = X/n；中心 p，标准误 √(p(1−p)/n)",
                "Large Counts：np ≥ 10 且 n(1−p) ≥ 10",
                "正态近似的条件"),
               sheets=("sampling-distributions.html",)),
            _t("3.3", "Constructing a Confidence Interval for a Population Proportion", "总体比例的置信区间",
               ("p̂ ± z*·√(p̂(1−p̂)/n)",
                "条件：随机、10%、Large Counts（这里用 p̂ 检查）",
                "zInterval_1Prop 与手算一致"),
               sheets=("confidence-intervals.html",)),
            _t("3.4", "Justifying a Claim Based on a Confidence Interval for a Population Proportion",
               "基于置信区间做判断",
               ("解释区间：重复抽样角度的方法保证",
                "原假设值落在区间内 → 支持不了该声明",
                "区间越宽、样本量越小 → 证据越弱"),
               sheets=("confidence-intervals.html",)),
            _t("3.5", "Setting Up a Test for a Population Proportion", "设置总体比例的检验",
               ("H₀: p = p₀ 与 Hₐ: p ≠ p₀（也可单侧）",
                "检验的标准误用 p₀，不是 p̂",
                "Large Counts 同样用 p₀ 检查"),
               sheets=("z-tests-proportions.html",)),
            _t("3.6", "p-Values", "p 值",
               ("p 值 = 在 H₀ 为真时得到当前或更极端结果的概率",
                "p ≤ α 则拒绝 H₀",
                "p 值小不等于效应大"),
               sheets=("z-tests-proportions.html",)),
            _t("3.7", "Carrying Out a Test for a Population Proportion", "执行总体比例的检验",
               ("算 z 统计量与 p 值，与临界值法互相验证",
                "结论只说参数，不说统计量",
                "写情境化的结论句"),
               sheets=("z-tests-proportions.html",)),
            _t("3.8", "Potential Errors When Performing Tests", "检验中的潜在错误",
               ("第一类错误 α、第二类错误 β、功效 1−β",
                "哪些因素会改变 β 与功效",
                "降低 α 的代价"),
               sheets=("z-tests-proportions.html",)),
            _t("3.9", "Sampling Distributions for the Difference Between Sample Proportions",
               "两个样本比例之差的抽样分布",
               ("中心 p₁ − p₂；标准误把两个方差相加",
                "四项条件：随机、独立、10%、Large Counts",
                "差值的区间/检验与单样本不同"),
               sheets=("sampling-distributions.html",)),
            _t("3.10", "Constructing a Confidence Interval for the Difference Between Two Population Proportions",
               "两个总体比例之差的置信区间",
               ("(p̂₁ − p̂₂) ± z*·SE，用各自的 p̂，不用合并",
                "条件检查",
                "合并比例只属于检验"),
               sheets=("confidence-intervals.html",)),
            _t("3.11", "Justifying a Claim Based on a Confidence Interval for the Difference Between Two Population Proportions",
               "基于差值区间做判断",
               ("差值区间的情境化解释",
                "0 是否落在区间内",
                "与「差异是否显著」的表述"),
               sheets=("confidence-intervals.html",)),
            _t("3.12", "Setting Up a Test for the Difference Between Two Population Proportions",
               "设置两个总体比例之差的检验",
               ("H₀: p₁ = p₂，所以用合并 p̂c = (X₁+X₂)/(n₁+n₂)",
                "条件：随机、独立、10%、Large Counts",
                "检验与区间在这里必须用不同的标准误"),
               sheets=("z-tests-proportions.html",)),
            _t("3.13", "Carrying Out a Test for the Difference Between Two Population Proportions",
               "执行两个比例之差的检验",
               ("算 z 与 p 值",
                "结论说两个总体比例的差异",
                "把情境写进结论句"),
               sheets=("z-tests-proportions.html",)),
            _t("3.14", "Setting Up a Chi-Square Test for Homogeneity or Independence", "设置卡方检验",
               ("期望频数 E = (行合计 × 列合计)/n",
                "H₀：两分布相同 / 两变量独立",
                "自由度 df = (行数 − 1)(列数 − 1)")),
            _t("3.15", "Carrying Out a Chi-Square Test for Homogeneity or Independence", "执行卡方检验",
               ("χ² = Σ (观测 − 期望)²/期望，右尾",
                "p 值来自卡方分布",
                "结论：分布不同 / 变量不独立")),
        )),
    Unit(
        4, "Inference for Quantitative Data: Means", "定量数据推断：均值",
        "10–20%", "~18",
        (
            _t("4.1", "Sampling Distributions for Sample Means", "样本均值的抽样分布",
               ("中心 μ；σ 已知用 σ/√n，未知用 s/√n",
                "条件：随机、10%、总体正态或 n 足够大",
                "n 增大 → 标准误变小，但偏差不会消失"),
               sheets=("sampling-distributions.html",)),
            _t("4.2", "Constructing a Confidence Interval for a Population Mean or Population Mean Difference",
               "总体均值（或均值差）的置信区间",
               ("t 分布：σ 未知、自由度 n−1、尾部更厚",
                "单样本 t 区间：x̄ ± t*·s/√n",
                "配对 t（对差值）与双样本 t（不合并方差）"),
               sheets=("confidence-intervals.html",)),
            _t("4.3", "Justifying a Claim Based on a Confidence Interval for a Population Mean or Population Mean Difference",
               "基于均值区间做判断",
               ("区间的情境化解释：参数是 μ 或 μ₁−μ₂",
                "原假设值落在区间内 → 支持不了声明",
                "区间宽度与样本量、置信水平的关系"),
               sheets=("confidence-intervals.html",)),
            _t("4.4", "Setting Up a Test for a Population Mean or Population Mean Difference",
               "设置总体均值（或均值差）的检验",
               ("σ 未知 → t 检验；H₀: μ = μ₀",
                "参数写清楚：μ、μ₁−μ₂、μ_d",
                "条件检查与选择检验方法"),
               sheets=("t-tests-means.html",)),
            _t("4.5", "Carrying Out a Test for a Population Mean or Population Mean Difference",
               "执行总体均值（或均值差）的检验",
               ("t = (x̄−μ₀)/(s/√n)，df = n−1",
                "算 p 值或用临界值 t*",
                "结论：拒绝 / 未能拒绝，并写情境"),
               sheets=("t-tests-means.html",)),
            _t("4.6", "Sampling Distributions for the Difference Between Two Sample Means",
               "两个样本均值之差的抽样分布",
               ("中心 μ₁ − μ₂；标准误 √(s₁²/n₁+s₂²/n₂)，方差相加",
                "条件：两组独立随机、正态或样本足够大",
                "Welch 自由度 vs 保守自由度"),
               sheets=("sampling-distributions.html",)),
            _t("4.7", "Constructing a Confidence Interval for the Difference Between Two Population Means",
               "两个总体均值之差的置信区间",
               ("(x̄₁ − x̄₂) ± t*·SE",
                "条件检查；不合并方差",
                "与双比例区间的平行结构"),
               sheets=("confidence-intervals.html",)),
            _t("4.8", "Justifying a Claim Based on a Confidence Interval for the Difference Between Two Population Means",
               "基于差值区间做判断",
               ("0 是否落在区间内",
                "情境化解释 μ₁ − μ₂",
                "结论与检验的等价关系"),
               sheets=("confidence-intervals.html",)),
            _t("4.9", "Setting Up a Test for the Difference Between Two Population Means",
               "设置两个总体均值之差的检验",
               ("H₀: μ₁ = μ₂；参数是 μ₁ − μ₂",
                "配对 → 单样本 t（差值）；独立 → 双样本 t",
                "条件检查"),
               sheets=("t-tests-means.html",)),
            _t("4.10", "Carrying Out a Test for the Difference Between Two Population Means",
               "执行两个总体均值之差的检验",
               ("算 t 与 p 值",
                "自由度用 Welch 近似或保守值",
                "结论写情境与参数"),
               sheets=("t-tests-means.html",)),
        )),
    Unit(
        5, "Regression Analysis", "回归分析",
        "10–20%", "~9",
        (
            _t("5.1", "Graphical Representations Between Two Quantitative Variables", "两个定量变量的图形表示",
               ("画散点图并描述关联：形状、方向、强度、异常点",
                "区分线性关联与非线性关联",
                "相关不等于因果")),
            _t("5.2", "Correlation", "相关系数",
               ("r 的取值范围与方向含义",
                "强度：|r| 越接近 1 越强",
                "异常值与非线性会误导 r；r² 的解释力")),
            _t("5.3", "Linear Regression Models", "线性回归模型",
               ("模型 ŷ = a + bx，a 是截距、b 是斜率",
                "用模型做预测（代入 x）",
                "预测值不是实际值")),
            _t("5.4", "Residuals", "残差",
               ("残差 = 观测值 − 预测值",
                "残差图：看线性模型是否合适",
                "异常点与杠杆点的区别")),
            _t("5.5", "Least-Squares Regression", "最小二乘回归",
               ("用公式算 a、b",
                "解释斜率与截距的情境含义",
                "最小二乘性质：残差和为 0")),
        )),
)

APPENDICES: tuple[Topic, ...] = (
    _t("A", "Quick Reference & Tools", "速查与工具",
       ("推断程序选择器：数据结构 × 估计/检验",
        "记号速查表：参数 / 统计量 / 标准误",
        "必背易错点与后续章节计划"),
       sheets=("reference.html",)),
)


def _external(href: str | None) -> bool:
    return bool(href) and href.startswith("http")


def reading_order() -> list[str]:
    """Sheet files in book order, first appearance only (no duplicates)."""
    seen: set[str] = set()
    order: list[str] = []
    for unit in UNITS:
        for topic in unit.topics:
            for sheet in topic.sheets:
                if sheet not in seen:
                    seen.add(sheet)
                    order.append(sheet)
    return order


def unit_for(href: str) -> Unit | None:
    for unit in UNITS:
        if any(href in t.sheets for t in unit.topics):
            return unit
    return None


def topics_for_sheet(href: str) -> list[Topic]:
    out: list[Topic] = []
    for unit in UNITS:
        out.extend(unit.topics_for(href))
    return out


def topic_code_range(href: str) -> str:
    codes = [t.code for t in topics_for_sheet(href)]
    if not codes:
        return ""
    if len(codes) == 1:
        return codes[0]
    return f"{codes[0]}–{codes[-1]}"


def _sheet_links(sheets: tuple[str, ...]) -> str:
    out = []
    for sheet in sheets:
        pdf = sheet.replace(".html", ".pdf")
        out.append(f'<a class="toc-sheet-link" href="{sheet}">讲义</a>'
                   f'<a class="toc-sheet-link toc-pdf" href="{pdf}">PDF</a>')
    return "".join(out)


def render_toc() -> str:
    """The full contents page, injected into index.html's placeholder."""
    out = ['<nav class="chapter-toc" aria-label="Table of contents">',
           '<div class="toc-legend">',
           '<span><i class="toc-dot toc-dot-ready"></i>已有讲义 / sheet written</span>',
           '<span><i class="toc-dot toc-dot-planned"></i>计划中 / planned</span>',
           '<span class="zh">按 AP 统计考纲（2026 秋季生效版）五个单元、55 个主题排列；'
           '每个主题下是中文分点</span>',
           '</div>', '<ol class="toc-units">']
    for unit in UNITS:
        out.append(f'<li class="toc-unit" id="{unit.anchor}">')
        out.append(f'<div class="toc-unit-head"><span class="toc-unit-num">{unit.label}</span>'
                   f'<div class="toc-unit-title">{unit.en} <span class="zh">{unit.zh}</span></div>'
                   f'<span class="toc-unit-meta">AP 权重 {unit.weight} &middot; ~{unit.periods} 课时</span></div>')
        out.append('<ol class="toc-topics">')
        for topic in unit.topics:
            open_attr = " open" if topic.written else ""
            status = ('<span class="toc-status toc-status-ready">已写 / written</span>'
                      if topic.written else '<span class="toc-status toc-status-planned">计划中 / planned</span>')
            out.append(f'<li class="toc-topic"><details{open_attr}>'
                       f'<summary><span class="toc-topic-code">{topic.code}</span>'
                       f'<span class="toc-topic-title">{topic.en} '
                       f'<span class="zh">{topic.zh}</span></span>{status}</summary>')
            if topic.points:
                out.append('<ul class="toc-points">')
                for point in topic.points:
                    out.append(f'<li>{point}</li>')
                out.append('</ul>')
            if topic.sheets:
                out.append(f'<p class="toc-topic-sheets">{_sheet_links(topic.sheets)}</p>')
            out.append('</details></li>')
        out.append('</ol></li>')
    out.append('</ol>')
    out.append('<h3 class="toc-appendix-title">Appendices <span class="zh">附录</span></h3>')
    out.append('<ol class="toc-appendix">')
    for topic in APPENDICES:
        points = "".join(f"<li>{p}</li>" for p in topic.points)
        out.append(f'<li class="toc-topic"><details open><summary>'
                   f'<span class="toc-topic-code">{topic.code}</span>'
                   f'<span class="toc-topic-title">{topic.en} <span class="zh">{topic.zh}</span></span>'
                   f'<span class="toc-status toc-status-ready">已写 / written</span></summary>'
                   f'<ul class="toc-points">{points}</ul>'
                   f'<p class="toc-topic-sheets">{_sheet_links(topic.sheets)}</p></details></li>')
    out.append('</ol></nav>')
    return "\n".join(out) + "\n"


def render_sidebar(current: str) -> str:
    """The fixed chapter navigation shown on every sheet and appendix."""
    current_unit = unit_for(current)
    out = ['<aside class="chapter-sidebar" aria-label="Chapter navigation">',
           '<a class="sidebar-home" href="index.html">&larr; 目录 <span class="zh">Contents</span></a>',
           '<details class="sidebar-details" id="sidebarDetails" open>',
           '<summary>Units 01&ndash;05 <span class="zh">章节</span></summary>',
           '<ol class="sidebar-units">']
    for unit in UNITS:
        active = " is-active" if unit is current_unit else ""
        out.append(f'<li class="sidebar-unit{active}">'
                   f'<a class="sidebar-unit-head" href="index.html#{unit.anchor}">'
                   f'<span class="sidebar-num">{unit.num:02d}</span>'
                   f'<span class="sidebar-unit-title">{unit.en} <span class="zh">{unit.zh}</span></span></a>')
        ready = [t for t in unit.topics if t.written]
        if ready:
            out.append('<ol class="sidebar-sheets">')
            for topic in ready:
                sheet = topic.sheets[0]
                cls = ' class="is-current"' if sheet == current else ""
                out.append(f'<li><a href="{sheet}"{cls}><span class="sidebar-code">{topic.code}</span>'
                           f'{topic.zh}</a></li>')
            out.append('</ol>')
        out.append('</li>')
    out.append('</ol></details>')
    out.append('<div class="sidebar-appendix"><span class="sidebar-appendix-title">附录 / Appendices</span>')
    for topic in APPENDICES:
        cls = ' class="is-current"' if topic.sheets and topic.sheets[0] == current else ""
        out.append(f'<a href="{topic.sheets[0]}"{cls}>{topic.en} <span class="zh">{topic.zh}</span></a>')
    out.append('</div>')
    out.append('<a class="sidebar-all" href="index.html">完整 55 个主题 <span class="zh">/ full outline</span></a>')
    unit = unit_for(current)
    if unit:
        codes = topic_code_range(current)
        out.append(f'<p class="sidebar-now">当前 / Now reading<br><strong>{codes} &middot; {unit.label}</strong><br>'
                   f'<span>{unit.en}</span></p>')
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
    if unit:
        codes = topic_code_range(current)
        mid = (f'<a href="index.html#{unit.anchor}">{unit.label} · {unit.en} '
               f'<span class="zh">{unit.zh}</span></a>')
        return (f'<nav class="chapter-crumb"><a href="index.html">目录 <span class="zh">Contents</span></a>'
                f' <span class="crumb-sep">/</span> {mid} <span class="crumb-sep">/</span> '
                f'<strong>Topic {codes}</strong></nav>\n  ')
    if current == "reference.html":
        return ('<nav class="chapter-crumb"><a href="index.html">目录 <span class="zh">Contents</span></a>'
                ' <span class="crumb-sep">/</span> <strong>Appendix A · Quick Reference</strong></nav>\n  ')
    return ""
