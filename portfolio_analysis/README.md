# Portfolio Analysis Model

Implementazione Python e notebook Colab dello **Simply Wall St Portfolio Analysis Model** pubblico.

Il modello portfolio usa i risultati dell'analisi società (`company_valuation`) e li aggrega a livello portafoglio:

- Watchlist / holdings / transaction portfolio.
- Portfolio snowflake come media ponderata degli snowflake societari.
- Best/worst contributor per asse dello snowflake.
- Rendimento dollar-weighted / money-weighted usando capitale e anni medi investiti.
- Time-weighted return e confronto benchmark.
- Intrinsic value di portafoglio come somma dei fair value individuali moltiplicati per le azioni detenute.
- Metriche aggregate Value / Future / Health / Dividend con gestione outlier.
- Esportazione CSV, Excel e dashboard HTML interattiva.

## Notebook

```text
portfolio_analysis/notebooks/SWS_Portfolio_Analysis_Model.ipynb
```

## Uso locale

```bash
python -m pip install -r portfolio_analysis/requirements.txt
jupyter notebook portfolio_analysis/notebooks/SWS_Portfolio_Analysis_Model.ipynb
```

## Output attesi

- `portfolio_overview.csv`
- `portfolio_holdings.csv`
- `portfolio_snowflake.csv`
- `portfolio_contributors.csv`
- `portfolio_metric_summary.csv`
- `portfolio_time_weighted_returns.csv`
- `portfolio_analysis_report.xlsx`
- `portfolio_analysis_dashboard.html`
