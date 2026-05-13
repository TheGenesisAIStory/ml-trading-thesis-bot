# Research Project Folders

This repository now contains dedicated GitHub-ready research folders:

| Folder | Purpose | Main notebook |
|---|---|---|
| `company_valuation/` | Company valuation, FMP fundamentals, SWS-style scoring, fair-value estimates, and dashboard | `company_valuation/notebooks/Company_Valuatio.ipynb` |
| `pead_european_banks_ifrs9/` | PEAD / IFRS9 European banks experiment using the central Untitled2 database ingestion pattern | `pead_european_banks_ifrs9/notebooks/PEAD_EuropeanBanks_IFRS9_FullExperiment.ipynb` |
| `portfolio_analysis/` | SWS-style portfolio analysis model with holdings, returns, snowflake aggregation, Excel export and dashboard | `portfolio_analysis/notebooks/SWS_Portfolio_Analysis_Model.ipynb` |
| `prompts/` | Reusable notebook and dashboard production standards | `prompts/01_notebook_experiment.md`, `prompts/02_report_dashboard.md` |

## Sync to Google Drive

When running in Colab with Drive mounted, sync the research folders with:

```bash
python scripts/sync_research_to_drive.py
```

Default destination:

```text
/content/drive/MyDrive/ml-trading-thesis-bot_research_exports
```

Outside Colab, the script exits with a warning instead of failing silently.
