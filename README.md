# Statistics Cheat Sheet 📊📘

Formula-first study sheets for **AP Statistics / Introductory Statistics**, written in **HTML** (interactive browser reading & GitHub Pages) paired with exact matching **print-ready A4 PDFs**.

🌐 **Online lecture:** <https://franky100-pig.github.io/Stats-CheatSheet/> — a contents page, one chapter per AP Statistics unit, and a fixed unit sidebar on every sheet. Deployed from `main` by `.github/workflows/pages.yml`, the same pattern as LA-Helper.

🧮 **Calculator companion:** <https://franky100-pig.github.io/Digital-Nspire-for-Stats/> — [Digital-Nspire-for-Stats](https://github.com/Franky100-pig/Digital-Nspire-for-Stats) runs the same procedures with the TI-Nspire's own function names. The two sites link to each other; every sheet ends with a *Try it on the TI-Nspire* box of commands that really exist in that project's catalogue.

Every sheet focuses on:
- **Exact Formulas** (stacked fractions, radicals, standard error vs. standard deviation)
- **Complete Variable Definitions** (parameter vs. statistic, subscripts, degrees of freedom)
- **Required Conditions** (Random, 10% Independence, Normal / Large Counts)
- **Exam Traps & Calculator Syntax**

🌏 **Bilingual site, English exam sheets.** The web version is bilingual: formulas,
symbols and TI-Nspire command names stay in English (the language of the AP exam),
while every section gets a Chinese heading and a short Chinese explanation of the
idea, the conditions and the traps. A **双语 / EN** button in the navigation switches
to an English-only exam view; the choice is remembered, and `?lang=en` gives a
shareable English-only link. The A4 PDFs and the root `*.html` sheets stay
English-only. 中文说明集中在 `tools/i18n_zh.py`，不写进讲义正文。

---

## 📚 Structure: the AP Statistics course framework, Fall 2026

The chapters follow the **AP Statistics Course and Exam Description, effective Fall 2026**: five
units, 55 topics. [`tools/chapters.py`](./tools/chapters.py) is the **only** place that structure is
written down — every unit, every topic, its Chinese knowledge points and the sheets that cover it.
The contents page, the sidebar on every sheet, the breadcrumbs, the in-page outlines and the
previous/next links are all generated from it.

| Unit | Unit title | Topics | AP weight | Pacing | Sheets |
|---|---|---|---|---|---|
| 01 | Exploring One-Variable Data and Collecting Data | 1.1–1.13 | 20–30% | ~26 periods | — |
| 02 | Probability, Random Variables, and Probability Distributions | 2.1–2.12 | 15–25% | ~24 periods | **2.12** Sampling Distributions |
| 03 | Inference for Categorical Data: Proportions | 3.1–3.15 | 15–25% | ~30 periods | **3.2–3.4, 3.10–3.11** Confidence Intervals · **3.5–3.8, 3.12–3.13** z-Tests |
| 04 | Inference for Quantitative Data: Means | 4.1–4.10 | 10–20% | ~18 periods | **4.2–4.3, 4.7–4.8** Confidence Intervals · **4.4–4.5, 4.9–4.10** t-Tests |
| 05 | Regression Analysis | 5.1–5.5 | 10–20% | ~9 periods | — |
| A | **Appendix — [Quick Reference & Tools](./reference.html)**: inference procedure picker, notation table, exam traps | — | — | — | ✅ |

Two things changed with the Fall 2026 framework, and the outline follows the document rather than the
older memory of it: the units were renumbered (Probability is Unit 2, Sampling Distributions are
Topic 2.12, Inference for Proportions Unit 3, Inference for Means Unit 4, Regression Unit 5), and
**there is no topic on inference for a regression slope** — Unit 5 stops at least-squares regression
(Topic 5.5).

### Unit 2 · Topic 2.12 — Sampling Distributions and the Central Limit Theorem
Population parameters vs. sample statistics ($\mu, \sigma, p$ vs. $\bar{x}, s, \hat{p}$), sampling distributions of $\bar{x}$ and $\hat{p}$, Central Limit Theorem (CLT), two-sample differences ($\bar{x}_1 - \bar{x}_2$, $\hat{p}_1 - \hat{p}_2$), and the R-I-N conditions.

### Unit 3 · Topics 3.3–3.11 — Confidence Intervals ($z$ & $t$)
Universal interval structure ($\text{PE} \pm \text{ME}$), critical values $z^*$ vs. $t^*$, 1-Prop / 2-Prop $z$-intervals, 1-Sample / Paired / 2-Sample $t$-intervals, minimum sample size $n$ formulas, and exam-safe interpretation templates.

### Unit 3 · Topics 3.5–3.13 — Hypothesis Testing & $z$-Tests
Null/alternative hypotheses ($H_0, H_a$), 1-Proportion and 2-Proportion $z$-tests (including pooled $\hat{p}_c$), known-$\sigma$ 1-Sample $z$-test, $p$-value rules, Type I / Type II error matrix ($\alpha, \beta$), and statistical power ($1 - \beta$).

### Unit 4 · Topics 4.4–4.10 — $t$-Tests for Means & Paired Data
Student's $t$-distribution vs. Normal, 1-Sample $t$-test, Matched Pairs $t$-test ($\bar{d}, s_d$), Welch 2-Sample $t$-test (unpooled SE & $df$), and a decision table comparing Matched Pairs vs. 2-Sample $t$-tests.

---

## 🏠 House rule: all statistics notes live here

**Every statistics knowledge point goes into this repository — AP Statistics first.** This is the single home for stats notes, not a scratch pad in another project and not a loose file.

- A new idea that belongs to an existing chapter → extend that sheet's `.html`, then regenerate its PDF.
- A genuinely new chapter → add the sheet (`.html`), its `.pdf`, **its entry in `tools/chapters.py`** (unit, topic code, English + Chinese title, the Chinese knowledge points, and which sheet covers it), **a row in the procedure picker** if it is an inference procedure, and **the matching Chinese entries in `tools/i18n_zh.py`** (英文正文 + 中文逐节对照，两者都要写).
- A calculator trick → it goes in [Digital-Nspire-for-Stats](https://github.com/Franky100-pig/Digital-Nspire-for-Stats), and is linked from the relevant sheet here.
- The order of the chapters is the order in `tools/chapters.py`; the site builder derives the contents page, the sidebar and the previous/next links from it, so nothing has to be updated twice.

---

## 🚀 Quick Formula & Notation Traps

1. **Parameters vs. Statistics**: Hypotheses ($H_0, H_a$) and interval interpretations are *always* about **parameters** ($\mu, p, \mu_d, p_1 - p_2$), never sample statistics ($\bar{x}, \hat{p}$).
2. **Variances Always Add**: For independent samples, $\text{Var}(X - Y) = \text{Var}(X) + \text{Var}(Y)$, so $\text{SE}_{\bar{x}_1 - \bar{x}_2} = \sqrt{s_1^2/n_1 + s_2^2/n_2}$.
3. **Pooled $\hat{p}_c$ Usage**: Only use pooled $\hat{p}_c = \frac{X_1 + X_2}{n_1 + n_2}$ for a **2-Prop $z$-Test** ($H_0: p_1 = p_2$), *never* for a 2-Prop $z$-Interval.
4. **1-Prop Test vs. CI Large Counts**: 1-Prop $z$-Test uses $n p_0 \ge 10$ and $n(1 - p_0) \ge 10$ (null value $p_0$); 1-Prop $z$-Interval uses $n\hat{p} \ge 10$ and $n(1 - \hat{p}) \ge 10$.
5. **Sample Size Rounding**: Always round sample size $n$ **up** to the next whole integer to guarantee $\text{ME}$ stays within budget.

---

## 🛠️ Building

### The web version (GitHub Pages)
`tools/build_site.py` copies the root sheets into `public/` and adds everything a *book* needs
that a printable sheet does not: the contents page generated from `tools/chapters.py`, the fixed
unit sidebar with the current chapter marked, the breadcrumb, the in-page outline built from each
sheet's own `<h2>` anchors, the previous/next pager, the *Try it on the TI-Nspire* callouts, and a
footer. The root HTML files stay untouched, so `build_pdfs.py` still prints clean sheets and the
repository itself remains readable without a build step.

```bash
python3 tools/build_site.py            # writes public/
python3 tools/build_site.py --serve    # build + preview on http://127.0.0.1:8000
```

`.github/workflows/pages.yml` runs the same builder on every push to `main` and deploys `public/` with `actions/deploy-pages`. Pages must be set to the **GitHub Actions** source once in Settings → Pages. The site is fully static: no CDN, no tracking, no runtime downloads.

All Chinese text lives in two files: [`tools/i18n_zh.py`](./tools/i18n_zh.py) holds the per-section
glosses (`SECTION_ZH`, one `(中文小标题, 中文导读)` pair per `<h2>`), the per-chapter reading guides
(`INTRO_HTML`) and the procedure-picker hints (`PICKER_ZH`); [`tools/chapters.py`](./tools/chapters.py)
holds the course outline itself, including the Chinese knowledge points for each of the 55 topics.
**When you add a new `<h2>` to a sheet, add its Chinese pair too** — the builder checks the counts
and fails the deploy rather than shipping a half-translated page.

The switch is two-sided: Chinese text sits in `.zh` elements (hidden in English-only mode and in
print), and its English replacement sits in `.en-only` elements (hidden in bilingual mode). Labels
like `已写 / Written` therefore read cleanly in both modes, and the Chinese knowledge-point lists
disappear entirely in the exam view instead of leaking through. The builder also strips every `.zh`
element from the generated HTML and **fails the deploy if any Chinese character survives**, so a new
label can never be added half-switched. `tools/site.js` drives the switch and `?lang=en` gives a
shareable English-only view.

### Regenerating PDFs from HTML
All sheets share [`styles.css`](./styles.css) (including CSS math helpers `.m`, `.xbar`, `.hat-wrap`, `.frac`, `.radic` and A4 `@page` print rules). After adding or editing any sheet, regenerate the matching `.pdf` files with:

```bash
python3 build_pdfs.py
```

`build_pdfs.py` reads the chapter map, so it prints exactly the sheets the site lists — the
contents page and the tools appendix never produce a PDF. The builder warns if a chapter in
`tools/chapters.py` points at a missing sheet or PDF, so a half-added chapter fails the deploy
rather than shipping a broken link.

### What is still to write
The unit map in `tools/chapters.py` is the plan; the units marked *planned* there are next:
chi-square tests (Unit 08), inference for the slope (Unit 09), probability and random variables
(Unit 04), sampling and experiments (Unit 03), and the two data-description units (01–02).
