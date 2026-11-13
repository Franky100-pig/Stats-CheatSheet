# Statistics Cheat Sheet 📊📘

Formula-first study sheets for **AP Statistics / Introductory Statistics**, written in **HTML** (interactive browser reading & GitHub Pages ready via `index.html`) paired with exact matching **print-ready A4 PDFs**.

Every sheet focuses on:
- **Exact Formulas** (stacked fractions, radicals, standard error vs. standard deviation)
- **Complete Variable Definitions** (parameter vs. statistic, subscripts, degrees of freedom)
- **Required Conditions** (Random, 10% Independence, Normal / Large Counts)
- **Exam Traps & Calculator Syntax**

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

## 🛠️ Notes for Contributing / Next Topics

### Regenerating PDFs from HTML
All topic sheets share [`styles.css`](./styles.css) (including CSS math helpers `.m`, `.xbar`, `.hat-wrap`, `.frac`, `.radic` and A4 `@page` print rules). After adding or editing any `<topic>.html`, regenerate all matching `.pdf` files with:
```bash
python3 build_pdfs.py
```

### Suggested Next Topics to Add
- `topic-05`: **Chi-Square ($\chi^2$) Tests** — Goodness-of-Fit, Homogeneity, Independence, expected counts $E = \frac{\text{row total} \times \text{col total}}{n}$, and $df$.
- `topic-06`: **Linear Regression & Inference for Slope** — LSRL ($\hat{y} = a + bx$), $r, r^2, s, SE_b$, and $t$-test / CI for slope $\beta$.
- `topic-07`: **Probability, Random Variables & Distributions** — Conditional probability, independence, Binomial ($\mu = np, \sigma = \sqrt{np(1-p)}$), Geometric, and linear combinations.
- `topic-08`: **Experimental Design & Sampling Methods** — SRS, stratified vs. cluster, blocking, confounding, scope of inference (generalizability vs. causation).
