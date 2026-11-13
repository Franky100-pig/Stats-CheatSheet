# Statistics Cheat Sheet 📊📘

Formula-first study sheets for **AP Statistics / Introductory Statistics**, written in **HTML** (interactive browser reading & GitHub Pages) paired with exact matching **print-ready A4 PDFs**.

🌐 **Online mini lecture:** <https://franky100-pig.github.io/Stats-CheatSheet/> — deployed from `main` by `.github/workflows/pages.yml`, the same pattern as LA-Helper.

🧮 **Calculator companion:** <https://franky100-pig.github.io/Digital-Nspire-for-Stats/> — [Digital-Nspire-for-Stats](https://github.com/Franky100-pig/Digital-Nspire-for-Stats) runs the same procedures with the TI-Nspire's own function names. The two sites link to each other; every topic sheet ends with a *Try it on the TI-Nspire* box of commands that really exist in that project's catalogue.

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

## 🏠 House rule: all statistics notes live here

**Every statistics knowledge point goes into this repository — AP Statistics first.** This is the single home for stats notes, not a scratch pad in another project and not a loose file.

- A new idea that belongs to an existing topic → extend that topic's `.html`, then regenerate its PDF.
- A genuinely new topic → add `topic-NN.html` (or a descriptive slug), a matching `.pdf`, a card in `index.html`, a row in the procedure picker if it is an inference procedure, **and the matching Chinese entries in `tools/i18n_zh.py`** (英文正文 + 中文逐节对照，两者都要写).
- A calculator trick → it goes in [Digital-Nspire-for-Stats](https://github.com/Franky100-pig/Digital-Nspire-for-Stats), and is linked from the relevant sheet here.
- Order is whatever `index.html` links: the site builder reads that list to generate previous/next navigation.

---

## 📑 Documents & Direct Downloads

### 1. Sampling Distributions & Central Limit Theorem
Population parameters vs. sample statistics ($\mu, \sigma, p$ vs. $\bar{x}, s, \hat{p}$), sampling distributions of $\bar{x}$ and $\hat{p}$, Central Limit Theorem (CLT), two-sample differences ($\bar{x}_1 - \bar{x}_2$, $\hat{p}_1 - \hat{p}_2$), and the R-I-N conditions:
- 🌐 **HTML**: **[sampling-distributions.html](./sampling-distributions.html)**
- 📄 **PDF**: **[sampling-distributions.pdf](./sampling-distributions.pdf)** (Print-ready A4)

---

### 2. Confidence Intervals ($z$-Interval & $t$-Interval)
Universal interval structure ($\text{PE} \pm \text{ME}$), critical values $z^*$ vs. $t^*$, 1-Prop / 2-Prop $z$-intervals, 1-Sample / Paired / 2-Sample $t$-intervals, minimum sample size $n$ formulas, and exam-safe interpretation templates:
- 🌐 **HTML**: **[confidence-intervals.html](./confidence-intervals.html)**
- 📄 **PDF**: **[confidence-intervals.pdf](./confidence-intervals.pdf)** (Print-ready A4)

---

### 3. Hypothesis Testing & $z$-Tests
Null/alternative hypotheses ($H_0, H_a$), 1-Proportion and 2-Proportion $z$-tests (including pooled $\hat{p}_c$), known-$\sigma$ 1-Sample $z$-test, $p$-value rules, Type I / Type II error matrix ($\alpha, \beta$), and statistical power ($1 - \beta$):
- 🌐 **HTML**: **[z-tests-proportions.html](./z-tests-proportions.html)**
- 📄 **PDF**: **[z-tests-proportions.pdf](./z-tests-proportions.pdf)** (Print-ready A4)

---

### 4. $t$-Tests for Means & Paired Data
Student's $t$-distribution vs. Normal, 1-Sample $t$-test, Matched Pairs $t$-test ($\bar{d}, s_d$), Welch 2-Sample $t$-test (unpooled SE & $df$), and a decision table comparing Matched Pairs vs. 2-Sample $t$-tests:
- 🌐 **HTML**: **[t-tests-means.html](./t-tests-means.html)**
- 📄 **PDF**: **[t-tests-means.pdf](./t-tests-means.pdf)** (Print-ready A4)

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
`tools/build_site.py` copies the root sheets into `public/` and adds the site chrome — navigation, previous/next pager, *Try it on the TI-Nspire* callouts and a footer. The root HTML files stay untouched, so `build_pdfs.py` still prints clean sheets and the repository itself remains readable without a build step.

```bash
python3 tools/build_site.py            # writes public/
python3 tools/build_site.py --serve    # build + preview on http://127.0.0.1:8000
```

`.github/workflows/pages.yml` runs the same builder on every push to `main` and deploys `public/` with `actions/deploy-pages`. Pages must be set to the **GitHub Actions** source once in Settings → Pages. The site is fully static: no CDN, no tracking, no runtime downloads.

All Chinese text lives in [`tools/i18n_zh.py`](./tools/i18n_zh.py): `SECTION_ZH` holds
one `(中文小标题, 中文导读)` pair per `<h2>`, `INTRO_HTML` holds the per-topic reading guide,
and `PICKER_ZH` holds the procedure-picker hints. **When you add a new `<h2>` to a sheet,
add its Chinese pair too** — the builder checks the counts and fails the deploy rather than
shipping a half-translated page. `tools/site.js` drives the language switch; `tools/site.css`
hides every `.zh` element in English-only mode and in print.

### Regenerating PDFs from HTML
All topic sheets share [`styles.css`](./styles.css) (including CSS math helpers `.m`, `.xbar`, `.hat-wrap`, `.frac`, `.radic` and A4 `@page` print rules). After adding or editing any `<topic>.html`, regenerate all matching `.pdf` files with:

```bash
python3 build_pdfs.py
```

The builder warns if a topic linked from `index.html` is missing its HTML or its PDF, so a half-added topic fails the deploy rather than shipping a broken link.

### Suggested Next Topics to Add
- `topic-05`: **Chi-Square ($\chi^2$) Tests** — Goodness-of-Fit, Homogeneity, Independence, expected counts $E = \frac{\text{row total} \times \text{col total}}{n}$, and $df$.
- `topic-06`: **Linear Regression & Inference for Slope** — LSRL ($\hat{y} = a + bx$), $r, r^2, s, SE_b$, and $t$-test / CI for slope $\beta$.
- `topic-07`: **Probability, Random Variables & Distributions** — Conditional probability, independence, Binomial ($\mu = np, \sigma = \sqrt{np(1-p)}$), Geometric, and linear combinations.
- `topic-08`: **Experimental Design & Sampling Methods** — SRS, stratified vs. cluster, blocking, confounding, scope of inference (generalizability vs. causation).
