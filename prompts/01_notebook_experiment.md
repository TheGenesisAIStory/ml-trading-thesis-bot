# Universal Research Notebook Experiment Standard

Every research notebook must use exactly these H2 markdown sections in order:

1. `## 0. Setup & Config`
2. `## 1. Data Ingestion`
3. `## 2. Cleaning & Alignment`
4. `## 3. Feature Engineering`
5. `## 4. Targets & Labels`
6. `## 5. Descriptive Stats`
7. `## 6. Exploratory / Event Study`
8. `## 7. Single-Factor Diagnostics`
9. `## 8. Statistical Models (regressions / econometrics)`
10. `## 9. ML Walk-Forward`
11. `## 10. Feature Ablation`
12. `## 11. Backtest / Strategy Evaluation`
13. `## 12. Interpretability`
14. `## 13. Robustness Checks`
15. `## 14. Final Summary`

Each section starts with a markdown description, a `| Cell | What it does | Output |` table, relevant formulas, and economic/scientific intuition.

Core rules:
- Section 0 contains silent pip installs, imports, `EXPERIMENT`, universe/entity dicts, output folders, logging, seed, color palette, matplotlib/seaborn style.
- Real data first; synthetic fallback must be realistic, logged as WARNING, and marked with `_synthetic` columns.
- No silent `try/except`; every exception handler logs WARNING or ERROR.
- No look-ahead: rolling/lagged features must shift before use.
- Walk-forward only; never random train/test split.
- Ablation uses feature blocks and compares to controls-only.
- Figures are saved before `plt.show()` and use `COLORS`.
- Tables are saved as CSV and include sample size where applicable.
- Section 13 includes subperiod, placebo, and sensitivity checks.
- Section 14 ends with the standard experiment-complete artifact counter.
