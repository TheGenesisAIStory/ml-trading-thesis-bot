# Research Export Locations

Use these locations when GitHub says the branch still has conflicts and you need
the research work outside the PR view.

## Local Mac checkout

The current export command mirrors the three research projects and support files
to:

```text
/Users/itsgennymac/GitHub/machine-learning-for-trading
```

Run it from this repository with:

```bash
python scripts/sync_research_projects.py --destination /Users/itsgennymac/GitHub/machine-learning-for-trading --zip
```

After the command finishes, look for:

- `/Users/itsgennymac/GitHub/machine-learning-for-trading/company_valuation/`
- `/Users/itsgennymac/GitHub/machine-learning-for-trading/pead_european_banks_ifrs9/`
- `/Users/itsgennymac/GitHub/machine-learning-for-trading/portfolio_analysis/`
- `/Users/itsgennymac/GitHub/machine-learning-for-trading/Company_Valuatio.ipynb`
- `/Users/itsgennymac/GitHub/machine-learning-for-trading/RESEARCH_EXPORT_MANIFEST.md`
- `/Users/itsgennymac/GitHub/machine-learning-for-trading/ml_trading_research_projects_bundle.zip`

## Google Drive from Colab

Mount Drive first:

```python
from google.colab import drive
drive.mount('/content/drive')
```

Then run:

```bash
python scripts/sync_research_to_drive.py --include-output
```

Default Drive destination:

```text
/content/drive/MyDrive/ml-trading-thesis-bot_research_exports
```

If Drive is not mounted, the script prints a warning instead of creating a fake
Drive folder.
