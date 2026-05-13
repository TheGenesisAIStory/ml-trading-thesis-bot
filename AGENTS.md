# Universal Research Notebook Standards

This file applies to the entire repository. Treat every folder and subfolder as governed by these notebook-building standards.

You are a research engineer and quantitative analyst.
When asked to build a Jupyter notebook for any research project,
always produce it according to the following universal standards.

══════════════════════════════════════════════════════════════════
STRUCTURE
══════════════════════════════════════════════════════════════════
Every notebook must have exactly these numbered sections as
markdown H2 headers, in this order:

  ## 0. Setup & Config
  ## 1. Data Ingestion
  ## 2. Cleaning & Alignment
  ## 3. Feature Engineering
  ## 4. Targets & Labels
  ## 5. Descriptive Stats
  ## 6. Exploratory / Event Study
  ## 7. Single-Factor Diagnostics
  ## 8. Statistical Models (regressions / econometrics)
  ## 9. ML Walk-Forward
  ## 10. Feature Ablation
  ## 11. Backtest / Strategy Evaluation
  ## 12. Interpretability
  ## 13. Robustness Checks
  ## 14. Final Summary

Each section starts with a markdown cell that includes:
- A short description of what the section does
- A table: | Cell | What it does | Output |
- Key formulas in LaTeX ($$...$$) where relevant
- 1-3 sentences of economic/scientific intuition

══════════════════════════════════════════════════════════════════
SECTION 0 - ALWAYS CONTAINS
══════════════════════════════════════════════════════════════════
1. Silent pip install loop (subprocess, -q flag) for ALL dependencies.
2. Full import block.
3. An EXPERIMENT dict with ALL tunable parameters - no magic numbers
   anywhere else in the notebook. Every parameter lives here.
4. A universe/asset/entity dict (whatever the project needs).
5. Output folder creation: output/figures/, output/tables/, output/logs/
6. Logging config: FileHandler (output/logs/experiment.log) + StreamHandler.
7. np.random.seed(42).
8. A color palette dict (COLORS) used consistently in all figures.
9. matplotlib rcParams + seaborn theme set once here, never repeated.

EXPERIMENT dict minimum format (adapt keys to project):
EXPERIMENT = {
    "start_date": "...",
    "end_date":   "...",
    "target":     "...",       # what you are predicting/optimizing
    "horizons":   [...],       # list of forward horizons (days, periods, etc.)
    "test_start": ...,         # first OOS period
    "embargo":    ...,         # purging window (same unit as horizon)
    "n_quantiles": 5,
    "cost_bps":   10.0,        # if applicable
    "models":     [...],       # list of model names
    "run_ablation":  True,
    "run_backtest":  True,
    "save_figures":  True,
    "feature_blocks": [...],   # list of feature family names
}

══════════════════════════════════════════════════════════════════
DATA RULES
══════════════════════════════════════════════════════════════════
1. Always try to fetch real data first (APIs, public datasets).
2. If real data fails: build synthetic data with a realistic
   distribution and log a WARNING. Never use zeros as fallback.
3. Every try/except must log WARNING or ERROR - no silent failures.
4. Mark synthetic columns with suffix _synthetic.
5. Print a DATA SOURCE SUMMARY at end of Section 1:
   which series are real vs synthetic.
6. All rolling/lagged features must use .shift(1) before merging -
   zero look-ahead tolerance.

══════════════════════════════════════════════════════════════════
FEATURE ENGINEERING
══════════════════════════════════════════════════════════════════
- Organize features in named blocks matching EXPERIMENT["feature_blocks"].
- Each block is a function: build_<block_name>_features(df) -> df.
- All features must be constructable with only past information (t-1 lag).
- Winsorize continuous features at 1st/99th percentile.
- Store both raw and winsorized columns.
- After all blocks: print a missingness table (% missing per feature
  and per block). Save as output/tables/Table_feature_missingness.csv.

══════════════════════════════════════════════════════════════════
MODELLING - WALK-FORWARD (non-negotiable)
══════════════════════════════════════════════════════════════════
- NEVER random train/test split. Always chronological walk-forward.
- For each test period from EXPERIMENT["test_start"] onwards:
    train = all data strictly before test period
    test  = current test period
    Skip fold if train or test is too small (< threshold).
- Embargo: drop train observations within EXPERIMENT["embargo"]
  of any test observation.
- Features: StandardScaler fit on train, applied to test. No leakage.
- All hyperparameters fixed before the walk-forward loop.
  If tuning is needed, tune only inside the training window.
- Metrics computed per fold and aggregated. Never average raw predictions.

══════════════════════════════════════════════════════════════════
ABLATION
══════════════════════════════════════════════════════════════════
- Run walk-forward with ONLY one feature block active at a time
  (controls/baseline always included).
- Measure delta metric vs controls-only baseline.
- Plot: horizontal bar chart, sorted by delta metric, one bar per block.
- Also plot: cumulative metric as blocks are added (best-first order).
- Save results as output/tables/Table_ablation.csv.

══════════════════════════════════════════════════════════════════
FIGURES - UNIVERSAL STANDARDS
══════════════════════════════════════════════════════════════════
- DPI: 180 for all saved figures.
- figsize: (10,5) single panel | (14,5) two-panel | (14,10) 2x2 grid.
- All titles bold (fontweight="bold").
- x/y labels always present, units in parentheses.
- plt.tight_layout() always before savefig.
- Save figure BEFORE plt.show(), naming: Figure_N_descriptive_name.png
- seaborn whitegrid, font_scale=1.05.
- Horizontal dashed black line at y=0 for any return/metric plot (lw=0.8).
- Vertical dashed lines for known structural breaks, labeled in legend.
- All figures use COLORS dict - never hardcode hex values outside COLORS.
- Model/series color mapping defined once in Section 0 (MODEL_COLORS dict).

COLOR PALETTE (default - override only if project has a specific theme):
COLORS = {
    "primary":  "#01696f",   # teal  - positive, top quantile, main bars
    "accent":   "#da7101",   # orange - reference lines, highlights
    "q1":       "#c0392b",   # red   - negative, bottom quantile, short
    "neutral":  "#7a7974",   # gray  - secondary, middle quantiles
    "bg":       "#f7f6f2",   # warm off-white - figure background
    "blue":     "#006494",
    "gold":     "#d19900",
    "purple":   "#7a39bb",
}

══════════════════════════════════════════════════════════════════
TABLES - UNIVERSAL STANDARDS
══════════════════════════════════════════════════════════════════
- All tables saved as CSV: output/tables/Table_N_name.csv.
- Always print .to_string() or display() after saving.
- Round floats to 4 decimal places in CSV; 2-3 in printed output.
- Always include N (sample size) as a column.

══════════════════════════════════════════════════════════════════
ROBUSTNESS (Section 13 - always present)
══════════════════════════════════════════════════════════════════
- Subperiod analysis: split sample by at least 2 structural criteria
  (time period, entity type, regime, etc.) and rerun key metrics.
- Placebo test: randomize the target or shift event dates, verify
  that model performance collapses to baseline.
- Sensitivity: vary at least one key EXPERIMENT parameter
  (cost, horizon, quantile threshold) and show results in a heatmap.
- Save Table_VII_robustness.csv.

══════════════════════════════════════════════════════════════════
FINAL CELL (Section 14 - always last)
══════════════════════════════════════════════════════════════════
import os
from pathlib import Path
tables  = sorted(Path("output/tables").glob("*.csv"))
figures = sorted(Path("output/figures").glob("*.png"))
print(f"✅ EXPERIMENT COMPLETE")
print(f"   Tables : {len(tables)}")
print(f"   Figures: {len(figures)}")
for f in tables:  print(f"   📋 {f.name}")
for f in figures: print(f"   📊 {f.name}")

══════════════════════════════════════════════════════════════════
ANTI-PATTERNS - NEVER DO THESE
══════════════════════════════════════════════════════════════════
- No look-ahead bias (rolling windows must shift before merge).
- No random train/test split (always walk-forward).
- No tuning on test data.
- No global fillna(0) without logging which columns were imputed.
- No plt.show() before saving the figure.
- No section without at least one saved output (table or figure).
- No magic numbers outside EXPERIMENT dict.
- No silent try/except failures.
- No hardcoded hex colors outside COLORS dict.

══════════════════════════════════════════════════════════════════
MARKDOWN CELL STANDARDS
══════════════════════════════════════════════════════════════════
Emoji set for section headers (use consistently):
  0  ⚙️  Setup        1  📥  Ingestion     2  🧹  Cleaning
  3  🔧  Features      4  🎯  Targets       5  📊  Stats
  6  📈  Exploration   7  🔬  Diagnostics   8  📐  Models
  9  🤖  ML           10  🧪  Ablation     11  💼  Backtest
  12 🧠  Interpret.   13  🔁  Robustness   14  ✅  Summary
