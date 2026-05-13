# PEAD European Banks IFRS9 Full Experiment

Notebook e codice dedicati all'esperimento **Post-Earnings Announcement Drift / IFRS9 European Banks**.

Il notebook è costruito secondo lo standard universale richiesto per i research notebook:

- sezioni `0`–`14` con header H2 ordinati;
- ingestion real-data-first con fallback sintetico realistico e loggato;
- feature blocks espliciti in `EXPERIMENT["feature_blocks"]`;
- target PEAD multi-orizzonte;
- walk-forward cronologico con embargo;
- ablation per blocchi;
- backtest long/short netto costi;
- interpretability e robustness;
- dashboard HTML finale.

## Collegamento con Untitled2 / Database Finanziario

La funzione `load_pead_data_from_db()` in `src/pead_data_loader.py` è pronta per riusare gli oggetti già creati dal notebook centrale Untitled2 / Company Valuation:

- `DB_ROOT`
- `FILE_MAP`
- `load_file`

Quando questi oggetti sono disponibili nello stesso runtime Colab, il notebook PEAD carica i prezzi dal Database Finanziario. Se il database o i risk factors non sono disponibili, il notebook tenta il web fallback e infine genera dati sintetici realistici marcati con colonne `_synthetic`.

## Struttura

```text
pead_european_banks_ifrs9/
├── notebooks/
│   └── PEAD_EuropeanBanks_IFRS9_FullExperiment.ipynb
├── src/
│   ├── __init__.py
│   └── pead_data_loader.py
├── output/
│   ├── tables/.gitkeep
│   ├── figures/.gitkeep
│   ├── logs/.gitkeep
│   └── dashboard/.gitkeep
├── requirements.txt
└── README.md
```

## Output principali

- `Table_1_data_source_summary.csv`
- `Table_feature_missingness.csv`
- `Table_II_event_study.csv`
- `Table_V_walk_forward.csv`
- `Table_ablation.csv`
- `Table_VI_backtest.csv`
- `Table_VII_robustness.csv`
- `Figure_1_event_study.png`
- `Figure_3_ablation.png`
- `Figure_4_equity_curve.png`
- `Figure_6_sensitivity_heatmap.png`
- `pead_european_banks_ifrs9_dashboard.html`

## Esecuzione locale

```bash
python -m pip install -r pead_european_banks_ifrs9/requirements.txt
jupyter notebook pead_european_banks_ifrs9/notebooks/PEAD_EuropeanBanks_IFRS9_FullExperiment.ipynb
```
