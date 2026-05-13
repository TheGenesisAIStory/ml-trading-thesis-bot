# Universal Research Dashboard Standard

After the notebook experiment has produced CSV/PNG/HTML artifacts, create a final shareable dashboard/report.

Minimum dashboard requirements:
- KPI cards for sample size, entities, date range, coverage, model/backtest metrics, and warnings.
- One-page executive summary with analyst-style interpretation.
- Interactive charts when Plotly is available; static image fallbacks otherwise.
- Ranked company/entity tables and diagnostic tables.
- Clean section headers and coherent color palette.
- Exportable standalone HTML report.

Preferred flow:
1. Read tables from `output/tables/`.
2. Read figures from `output/figures/`.
3. Build dashboard HTML in `output/dashboard/`.
4. Include links/paths to all artifacts.
5. Save a JSON manifest with table/figure counts and report path.
