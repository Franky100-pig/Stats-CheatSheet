# -*- coding: utf-8 -*-
"""All Chinese text for the bilingual lecture site, in one place.

The root *.html sheets stay English-only: they are the source for the A4 PDFs
and match the language of the AP Statistics exam. tools/build_site.py injects
this Chinese layer into the *built* pages only, and tools/site.js lets readers
switch between bilingual and English-only.

Maintenance rule: SECTION_ZH[page] must have exactly one (heading, gloss) pair
per <h2> in that page. build_site.py checks the counts and fails the deploy if
a new section was added without its Chinese counterpart -- that is deliberate.

Formulas, symbols and TI-Nspire command names are never translated.
"""

from __future__ import annotations

# One entry per <h2>, in document order: (中文小标题, 中文导读).
SECTION_ZH: dict[str, list[tuple[str, str]]] = {
    "index.html": [
        ("本书怎么组织",
         "一章对应 AP 考纲的一个单元，章内按「公式 → 条件 → 计算 → 情境解释」推进；还没写的单元也会先列出要覆盖什么，"
         "方便看清整个考纲地图。"),
        ("目录",
         "九个单元按考纲顺序排列，点标题进入讲义，PDF 是同内容的 A4 打印版；标「计划中」的是还没写的章节。"),
        ("一章怎么读",
         "每章开头有中文导读，下面逐节对照：英文负责考试用语，每个标题下的中文讲这一节真正在说什么；"
         "章末是配套的 TI-Nspire 命令，推导和计算在同一页。"),
        ("新笔记放哪",
         "所有统计知识点都进这个仓（AP 统计优先）：先扩已有章；全新主题就新增一页讲义 + PDF + 目录条目 + "
         "tools/i18n_zh.py 里的中文条目。结构只写在 tools/chapters.py 一处。"),
    ],
    "reference.html": [
        ("这些工具怎么用",
         "先用选择器定方法 → 再查条件 → 最后用计算器算，并回到情境里解释。"),
        ("我该用哪个推断方法？",
         "按「数据结构 + 目标是估计还是检验」查表：先分比例还是均值、一组还是两组、是否配对，再定 z 或 t。"
         "选择器给出的公式和命令都能跳到对应章节。"),
        ("计算器伴生项目",
         "Digital-Nspire-for-Stats 在浏览器里跑真正的 TI-Nspire 统计命令，函数拼写与讲义一致，可以边推公式边算。"),
        ("记号速查表",
         "参数 / 统计量 / 标准误一栏对照。最容易忘的一条：两个独立样本相减时，方差仍然是相加。"),
        ("必背易错点",
         "结论谈参数不谈统计量；方差相加；合并比例 p̂c 只用于检验；Large Counts 检验用 p₀、区间用 p̂；样本量一律向上取整。"),
    ],
    "sampling-distributions.html": [
        ("1. 变量定义：参数 vs 统计量",
         "参数（μ, σ, p）描述总体，是固定但通常未知的数；统计量（x̄, s, p̂）由样本算出，会随样本变化，本身就是随机变量。"
         "写假设、解释区间时只能谈参数，不能谈 x̄ 或 p̂。"),
        ("2. 样本均值的抽样分布",
         "反复抽容量为 n 的 SRS，所有 x̄ 构成的分布满足 E(x̄)=μ、SD(x̄)=σ/√n；σ 未知时用 SE=s/√n。"
         "总体不正态时靠中心极限定理（CLT），一般 n≥30 才近似正态。注意 n 变大只减小变异，不会修正偏差。"),
        ("3. 样本比例的抽样分布",
         "成功数 X~Binomial(n,p)，p̂=X/n。当 np≥10 且 n(1−p)≥10 时可近似正态，中心为 p、标准误为 √(p(1−p)/n)。"
         "检验时代入 p₀，区间里代入 p̂，两者别混。"),
        ("4. 两组抽样分布（差值）",
         "独立样本相减：中心相减、方差相加，即 Var(A−B)=Var(A)+Var(B)，所以 SE=√(s₁²/n₁+s₂²/n₂)。"
         "「两组互相独立」是前提，配对设计不能套这个公式。"),
        ("5. 条件清单（R-I-N）",
         "Random（随机抽样／随机分配）、Independence（10% 条件：n≤0.1N）、Normal（总体正态或 n 够大／Large Counts）。"
         "自由响应题必须把三条用文字写明，只列公式不给分。"),
        ("6. 常见陷阱与计算器语法",
         "别把 σ 与 σ_x̄、s 与 SE 混为一谈，也别用样本统计量表述结论。"
         "Nspire 上 normCdf 求面积、invNorm 求分位数、binomCdf 求二项累积概率 —— 这些都是计算器里的真实命令名。"),
    ],
    "confidence-intervals.html": [
        ("1. 通用结构与变量定义",
         "所有置信区间都是「点估计 ± 临界值 × 标准误」。z* 用于比例或已知 σ，t* 用于均值（σ 未知、df=n−1）。"
         "C% 说的是这个方法长期捕获真参数的比例，不是「这个区间有 95% 概率含参数」。"),
        ("2. 全部标准置信区间公式",
         "按数据类型选：单比例 z、双比例 z、单样本 t、配对 t（对差值 d 做单样本 t）、双样本 t（不合并方差）。"
         "双比例区间用各自的 p̂，绝不能用合并 p̂c —— 合并只在假设检验里出现。"),
        ("3. 求最小样本量 n",
         "由 ME ≥ z*·√(p̂(1−p̂)/n) 反解 n，没有先验信息时保守取 p̂=0.5；结果一律向上取整，保证误差范围不超预算。"),
        ("4. 误差范围与解释模板",
         "n 增大、置信水平降低、总体变异变小都会让 ME 变小。解释必须三件套：置信水平 + 参数（不是统计量）+ 具体情境。"
         "双侧 C% 区间与 α=1−C 的双侧检验等价：原假设值落在区间外就拒绝 H₀。"),
    ],
    "z-tests-proportions.html": [
        ("1. 检验框架与变量定义",
         "H₀ 永远写参数等于某个值（如 p=p₀），Hₐ 用 ≠、< 或 >。检验统计量衡量「观测到的 p̂ 离 H₀ 有多远（以标准误为单位）」。"
         "检验里的标准误要用 p₀，不用 p̂。"),
        ("2. 全部 z 检验公式",
         "单比例 z=(p̂−p₀)/√(p₀(1−p₀)/n)；双比例检验假设 p₁=p₂，因此用合并 p̂c=(X₁+X₂)/(n₁+n₂)；"
         "已知 σ 的均值检验用 z=(x̄−μ₀)/(σ/√n)。"),
        ("3. 计算 p 值与作结论",
         "p 值是在 H₀ 成立的前提下，得到当前或更极端结果的概率。p≤α 拒绝 H₀，否则是「未能拒绝」，不是「接受 H₀」。"
         "结论要回到情境里说参数，并点明 α 与证据强弱。"),
        ("4. 第一类／第二类错误与功效",
         "α=P(第一类错误)=拒掉真的 H₀；β=P(第二类错误)=没拒掉假的 H₀；功效=1−β。降低 α 会抬高 β；"
         "增大 n、增大真实效应、减小变异都能提高功效。"),
    ],
    "t-tests-means.html": [
        ("1. 为什么用 t：变量定义",
         "σ 未知时只能用 s 估计，这份额外不确定性让统计量服从 t 分布（df=n−1），尾部比正态更厚；样本越大 t 越接近 z。"
         "条件仍是随机、10%、总体近似正态或 n≥30（要检查偏态与离群点）。"),
        ("2. 三种 t 检验公式",
         "单样本 t=(x̄−μ₀)/(s/√n)；配对 t 先对每个配对算差 d，再对差值做单样本 t（H₀: μ_d=0）；"
         "双样本 Welch t 用 √(s₁²/n₁+s₂²/n₂)，不合并方差，df 用 Welch 近似或保守取 min(n₁−1, n₂−1)。"),
        ("3. 配对 t vs 双样本 t 怎么选",
         "同一对象前后测、或配对后随机分配 → 配对 t（分析差值，n 是配对数）；两组独立个体 → 双样本 t。"
         "把配对数据当独立样本会丢掉配对带来的降噪，标准误被高估。"),
        ("4. 计算器语法与常见陷阱",
         "invT(0.975, df) 求 t*；tTest 既做单样本也做配对（把差值列表传进去），tTest_2Samp 做独立双样本且默认不合并。"
         "别把区间与检验的条件、配对与独立、s 与 σ 混用。"),
    ],
}

# Injected immediately after the subtitle: a Chinese reading guide per page.
INTRO_HTML: dict[str, str] = {
    "index.html": (
        '<p class="zh zh-lead">中文：这是一本按 AP 统计考纲九个单元分章的讲义 —— 英文公式、符号与 TI 命令原样保留，'
        '中文逐节补充思路、条件和易错点。下面就是目录；右上角可在「双语 / 英文」之间切换。</p>'
    ),
    "reference.html": (
        '<section class="zh zh-intro"><h3>速查页说明（中文）</h3><ul>'
        '<li>推断程序选择器：选「数据结构 + 估计还是检验」，直接给出公式、条件、对应章节与计算器命令。</li>'
        '<li>记号速查表：参数 / 统计量 / 标准误对照。</li>'
        '<li>必背易错点：考试最常踩的五个坑。</li>'
        '<li>完整的章节地图在<a href="index.html">目录页</a>，本附录只放工具。</li>'
        '</ul></section>'
    ),
    "sampling-distributions.html": (
        '<section class="zh zh-intro"><h3>本讲要点（中文）</h3><ul>'
        '<li>参数是固定未知数，统计量是随样本变化的随机变量。</li>'
        '<li>两条抽样分布：x̄ 的中心 μ、标准误 σ/√n；p̂ 的中心 p、标准误 √(p(1−p)/n)。</li>'
        '<li>CLT 只在 n 够大时把非正态总体救回近似正态；R-I-N 三条条件必须写出来。</li>'
        '<li>独立两组相减时方差相加，这是后面所有双样本公式的地基。</li>'
        '</ul></section>'
    ),
    "confidence-intervals.html": (
        '<section class="zh zh-intro"><h3>本讲要点（中文）</h3><ul>'
        '<li>通用骨架：点估计 ± 临界值 × 标准误；比例用 z*，均值（σ 未知）用 t*。</li>'
        '<li>五种区间：单比例、双比例、单样本均值、配对、双样本均值。</li>'
        '<li>双比例区间不用合并 p̂c；合并比例只属于双比例 z 检验。</li>'
        '<li>解释要写「置信水平 + 参数 + 情境」；样本量反解后一律向上取整。</li>'
        '</ul></section>'
    ),
    "z-tests-proportions.html": (
        '<section class="zh zh-intro"><h3>本讲要点（中文）</h3><ul>'
        '<li>H₀ / Hₐ 只写参数；p 值是在 H₀ 成立时看到当前或更极端结果的概率。</li>'
        '<li>单比例用 p₀ 算标准误；双比例检验因为 H₀: p₁=p₂ 才用合并 p̂c。</li>'
        '<li>结论只能说「拒绝」或「未能拒绝 H₀」，不能说「接受 H₀」。</li>'
        '<li>α、β、功效 1−β 三者此消彼长，增大 n 是最干净的提功效办法。</li>'
        '</ul></section>'
    ),
    "t-tests-means.html": (
        '<section class="zh zh-intro"><h3>本讲要点（中文）</h3><ul>'
        '<li>σ 未知 → 用 s → 统计量服从 t 分布，df=n−1，尾部比正态厚。</li>'
        '<li>三种 t：单样本、配对（对差值做单样本）、双样本 Welch（不合并方差）。</li>'
        '<li>先判断「配对还是独立」，选错方法比算错数更常见。</li>'
        '<li>配套命令：invT / tTest / tTest_2Samp / tInterval_2Samp。</li>'
        '</ul></section>'
    ),
}

# Short Chinese hints for the index page's procedure picker, keyed by the
# picker's data value and goal. Consumed by window.STATS_I18N_ZH in index.html.
PICKER_ZH: dict[str, dict[str, str]] = {
    "one-prop": {
        "estimate": "一个分类变量的一组数据 → 单比例 z 区间。条件里的 Large Counts 用 p̂ 检查；结论要谈总体比例 p。",
        "test": "一个分类变量、对标一个声明值 p₀ → 单比例 z 检验。注意标准误和 Large Counts 都用 p₀，不是 p̂。",
    },
    "two-prop": {
        "estimate": "两个独立样本的比例差 → 双比例 z 区间，用各自 p̂ 算标准误，不能合并。",
        "test": "两个独立比例、H₀: p₁=p₂ → 双比例 z 检验，只有这里才用合并 p̂c。",
    },
    "one-mean": {
        "estimate": "一组定量数据、σ 未知 → 单样本 t 区间，df=n−1；检查偏态和离群点。",
        "test": "一组定量数据对标 μ₀ → 单样本 t 检验；条件与区间相同。",
    },
    "paired": {
        "estimate": "同一对象前后测或配对设计 → 先算差值 d，再对差值做配对 t 区间，n 是配对数。",
        "test": "配对数据检验 H₀: μ_d=0；绝不能当成两个独立样本处理。",
    },
    "two-mean": {
        "estimate": "两组独立定量数据 → 双样本 t 区间，方差相加、默认不合并。",
        "test": "两组独立均值比较 → Welch 双样本 t 检验，自由度不要简单当成 n₁+n₂−2。",
    },
}

# Bilingual site chrome. Formulas and command names are intentionally absent
# from these strings -- they never need translating.
UI: dict[str, str] = {
    "home": "首页",
    "contents": "目录",
    "reference": "速查与工具",
    "topics": "专题",
    "picker": "选方法",
    "calculator": "计算器",
    "github": "源码",
    "tagline": "AP 统计 · 小讲义",
    "callout_title": "在 TI-Nspire 上试一下",
    "callout_lead": "中文：下面是该章节对应的真实 TI-Nspire 命令名，直接复制到计算器就能跑。公式与命令一律保持英文。",
    "callout_button": "打开计算器",
    "prev": "上一章",
    "next": "下一章",
    "back_home": "回到目录",
    "start": "开始",
    "end": "已是最后一章",
    "footer": (
        "中文：Stats-CheatSheet 是 AP Statistics 的公式优先讲义，每个专题都有 A4 打印版 PDF；"
        "配套项目 Digital-Nspire-for-Stats 用 TI-Nspire 原生命令跑同样的推断流程。"
    ),
    "lang_both": "双语 · 切到 EN",
    "lang_en": "EN · 显示中文",
}
