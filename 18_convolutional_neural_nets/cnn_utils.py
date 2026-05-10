"""Modern CNN fallback helpers for chapter 18 notebooks."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import convolve2d
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler


def ensure_output_dir(path: str | Path = "../data/convolutional_neural_nets") -> Path:
    output = Path(path)
    output.mkdir(parents=True, exist_ok=True)
    return output


def edge_filter(image: np.ndarray) -> np.ndarray:
    kernel = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    return convolve2d(image, kernel, mode="same", boundary="symm")


def digit_data():
    digits = load_digits()
    X = digits.data / 16.0
    y = digits.target
    return X, y, digits.images


def train_digit_classifier(model_type: str = "mlp") -> tuple[object, float]:
    X, y, _ = digit_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    model = MLPClassifier(hidden_layer_sizes=(64,), max_iter=300, random_state=42, early_stopping=True) if model_type == "mlp" else LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)
    return model, accuracy_score(y_test, model.predict(X_test))


def make_time_series(samples: int = 900, lookback: int = 20, seed: int = 18):
    rng = np.random.default_rng(seed)
    x = np.sin(np.linspace(0, 35, samples)) + rng.normal(0, 0.15, samples)
    X, y = [], []
    for i in range(lookback, samples - 1):
        X.append(x[i - lookback:i])
        y.append(x[i + 1])
    return pd.DataFrame(X), pd.Series(y, name="target")


def train_sequence_regressor() -> tuple[MLPRegressor, float]:
    X, y = make_time_series()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, shuffle=False)
    model = MLPRegressor(hidden_layer_sizes=(32,), max_iter=300, random_state=42, early_stopping=True)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return model, float(np.sqrt(np.mean((y_test - pred) ** 2)))


def trading_image_features(n_samples: int = 400, seed: int = 1818) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    images = rng.normal(size=(n_samples, 8, 8))
    signal = images[:, :4, :4].mean(axis=(1, 2)) - images[:, 4:, 4:].mean(axis=(1, 2))
    y = (signal > np.median(signal)).astype(int)
    return images.reshape(n_samples, -1), y


def train_trading_image_model() -> tuple[MLPClassifier, float]:
    X, y = trading_image_features()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    model = MLPClassifier(hidden_layer_sizes=(32,), max_iter=300, random_state=42, early_stopping=True)
    model.fit(X_train, y_train)
    return model, accuracy_score(y_test, model.predict(X_test))


def bottleneck_features(X: np.ndarray, components: int = 12) -> pd.DataFrame:
    pca = PCA(n_components=components, random_state=42)
    return pd.DataFrame(pca.fit_transform(X), columns=[f"feature_{i}" for i in range(components)])


def synthetic_object_boxes(n: int = 10) -> pd.DataFrame:
    return pd.DataFrame({"image_id": range(n), "x": np.linspace(5, 40, n).astype(int), "y": np.linspace(8, 36, n).astype(int), "width": 12, "height": 10, "label": "digit_like"})
