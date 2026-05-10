# Project Optimization Tracker

Questo tracker coordina il consolidamento locale del repository. Non contiene segreti e non implica pubblicazione automatica.

## Regole operative

- Nessun push o pubblicazione senza conferma esplicita.
- Le credenziali restano solo in `.env.local` o `.env`, entrambi ignorati da git.
- Dataset grandi, raw data, cache, `.DS_Store`, virtual environment e file binari generati restano fuori da git.
- Ogni notebook definitivo deve essere validabile con `nbconvert --execute` quando i dati richiesti sono disponibili.
- Le API moderne passano da registry riusabili, non da chiavi hardcoded nei notebook.

## Stato corrente

| Area | Stato | Note |
|---|---:|---|
| `data` | In ripristino | Catalogo API/dataset e private API layer ricreati |
| `02_market_and_fundamental_data` | In ripristino | Registry provider/API ricreato; notebook ITCH recuperato |
| `03_alternative_data` | Da consolidare | Prossima tranche: catalogo fonti alternative moderne |
| `04_alpha_factor_research` | In ripristino | Utility alpha factor e notebook ML walk-forward in ricostruzione |
| `05_strategy_evaluation` | Completato | Notebook modernizzati ed eseguiti senza Zipline/Pyfolio legacy |
| `06_machine_learning_process` | Completato | Notebook modernizzati ed eseguiti senza Yellowbrick |
| `07_linear_models` | Completato | Notebook modernizzati ed eseguiti senza statsmodels/linearmodels/alphalens/talib |
| `08_ml4t_workflow` | Completato | Workflow vettoriale/ML eseguito senza Backtrader/Zipline runtime |
| `09_time_series_models` | Completato | Notebook modernizzati ed eseguiti senza pandas_datareader/statsmodels/pykalman obbligatori |
| `10_bayesian_machine_learning` | Completato | Notebook modernizzati ed eseguiti senza PyMC3/Theano/pandas_datareader obbligatori |
| `11_decision_trees_random_forests` | Completato | Notebook modernizzati ed eseguiti senza LightGBM/Alphalens/Zipline obbligatori |
| `12_gradient_boosting_machines` | Completato | Notebook modernizzati ed eseguiti senza LightGBM/CatBoost/SHAP/Zipline obbligatori |
| `13_unsupervised_learning` | Completato | Notebook modernizzati ed eseguiti senza UMAP/HDBSCAN/fastcluster obbligatori |
| `14_working_with_text_data` | Completato | Notebook modernizzati ed eseguiti senza spaCy/TextBlob/NLTK/VADER obbligatori |
| `15_topic_modeling` | Completato | Notebook modernizzati ed eseguiti senza Gensim/pyLDAvis obbligatori |
| `16_word_embeddings` | Completato | Notebook modernizzati ed eseguiti senza TensorFlow/Gensim/pretrained downloads obbligatori |
| `17_deep_learning` | Completato | Notebook modernizzati ed eseguiti senza TensorFlow/PyTorch/Keras/Zipline obbligatori |
| `18_convolutional_neural_nets` | Completato | Notebook modernizzati ed eseguiti senza TensorFlow/PyTorch/OpenCV/download immagini obbligatori |
| `19_recurrent_neural_nets` | Completato | Notebook modernizzati ed eseguiti senza TensorFlow/Keras/download testo obbligatori |
| `20_autoencoders_for_conditional_risk_factors` | Completato | Notebook modernizzati ed eseguiti senza TensorFlow/Keras/Alphalens obbligatori |
| `21_gans_for_synthetic_time_series` | Completato | Notebook modernizzati ed eseguiti senza TensorFlow/PyTorch obbligatori |
| `22_deep_reinforcement_learning` | Completato | Notebook modernizzati ed eseguiti senza Gym/Gymnasium/TensorFlow/PyTorch obbligatori |
| `24_alpha_factor_library` | Completato | Notebook modernizzati ed eseguiti senza TA-Lib/Alphalens/SHAP obbligatori |
| Database locale market data | Completato | SQLite locale smoke testato; full build 7 anni disponibile; dati pesanti esclusi da git |

## Comandi sicuri

```bash
python3.11 data/private_api_activation.py
cd data
python3.11 -m nbconvert --to notebook --execute --inplace 01_private_active_api_services.ipynb
python3.11 -m nbconvert --to notebook --execute --inplace 00_data_api_services_catalog_definitive.ipynb
python3.11 -m nbconvert --to notebook --execute --inplace create_datasets_definitive.ipynb
```
