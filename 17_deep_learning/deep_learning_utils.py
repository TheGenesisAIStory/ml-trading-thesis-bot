"""Modern deep-learning fallback helpers for chapter 17 notebooks."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler


def ensure_output_dir(path: str | Path = "../data/deep_learning") -> Path:
    output = Path(path)
    output.mkdir(parents=True, exist_ok=True)
    return output


def make_trading_dataset(samples: int = 1200, features: int = 12, seed: int = 17):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(samples, features))
    weights = rng.normal(size=features)
    signal = X @ weights + 0.5 * np.sin(X[:, 0] * X[:, 1])
    y_reg = signal / 100 + rng.normal(0, 0.02, samples)
    y_cls = (signal > np.median(signal)).astype(int)
    columns = [f"feature_{i:02d}" for i in range(features)]
    return pd.DataFrame(X, columns=columns), pd.Series(y_reg, name="forward_return"), pd.Series(y_cls, name="direction")


def fit_mlp_classifier(seed: int = 42, hidden=(32, 16)) -> tuple[MLPClassifier, pd.DataFrame, float]:
    X, _, y = make_trading_dataset(seed=seed)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=seed, stratify=y)
    scaler = StandardScaler().fit(X_train)
    model = MLPClassifier(hidden_layer_sizes=hidden, alpha=1e-3, max_iter=300, random_state=seed, early_stopping=True)
    model.fit(scaler.transform(X_train), y_train)
    pred = model.predict(scaler.transform(X_test))
    scored = X_test.copy()
    scored["target"] = y_test.to_numpy()
    scored["prediction"] = pred
    scored["score"] = model.predict_proba(scaler.transform(X_test))[:, 1]
    return model, scored, accuracy_score(y_test, pred)


def fit_mlp_regressor(seed: int = 42, hidden=(32, 16)) -> tuple[MLPRegressor, pd.DataFrame, float]:
    X, y, _ = make_trading_dataset(seed=seed)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=seed)
    scaler = StandardScaler().fit(X_train)
    model = MLPRegressor(hidden_layer_sizes=hidden, alpha=1e-3, max_iter=300, random_state=seed, early_stopping=True)
    model.fit(scaler.transform(X_train), y_train)
    pred = model.predict(scaler.transform(X_test))
    scored = X_test.copy()
    scored["target"] = y_test.to_numpy()
    scored["prediction"] = pred
    return model, scored, float(np.sqrt(mean_squared_error(y_test, pred)))


def architecture_search() -> pd.DataFrame:
    rows = []
    for hidden in [(16,), (32,), (32, 16), (64, 32)]:
        _, _, acc = fit_mlp_classifier(seed=171, hidden=hidden)
        rows.append({"hidden_layers": str(hidden), "accuracy": acc})
    return pd.DataFrame(rows).sort_values("accuracy", ascending=False)


def vector_backtest(scored: pd.DataFrame) -> pd.DataFrame:
    frame = scored.copy()
    frame["strategy_return"] = np.where(frame["score"] > 0.55, 0.01, np.where(frame["score"] < 0.45, -0.01, 0.0)) * np.where(frame["target"] == 1, 1, -1)
    frame["equity_curve"] = (1 + frame["strategy_return"]).cumprod()
    return frame[["strategy_return", "equity_curve"]]
