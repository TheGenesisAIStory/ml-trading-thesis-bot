"""Modern synthetic time-series helpers for chapter 21 notebooks."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


def ensure_output_dir(path: str | Path = "../data/gans_synthetic_time_series") -> Path:
    output = Path(path); output.mkdir(parents=True, exist_ok=True); return output


def real_returns(periods: int = 1000, seed: int = 21) -> pd.Series:
    rng = np.random.default_rng(seed)
    vol = 0.008 + 0.012 * (rng.random(periods) > 0.88)
    return pd.Series(rng.normal(0.0002, vol), name="real_return")


def synthetic_bootstrap(series: pd.Series, periods: int | None = None, seed: int = 42) -> pd.Series:
    rng = np.random.default_rng(seed)
    periods = periods or len(series)
    return pd.Series(rng.choice(series.to_numpy(), size=periods, replace=True), name="synthetic_return")


def synthetic_ar(series: pd.Series, seed: int = 43) -> pd.Series:
    rng = np.random.default_rng(seed)
    x = series.to_numpy()
    phi = np.corrcoef(x[1:], x[:-1])[0, 1]
    out = [x[0]]
    for _ in range(1, len(x)):
        out.append(phi * out[-1] + rng.normal(x.mean(), x.std()))
    return pd.Series(out, name="synthetic_ar_return")


def evaluate(real: pd.Series, synthetic: pd.Series) -> pd.DataFrame:
    return pd.DataFrame({"metric": ["mean", "std", "skew", "rmse_sorted"], "real": [real.mean(), real.std(), real.skew(), np.nan], "synthetic": [synthetic.mean(), synthetic.std(), synthetic.skew(), np.nan], "difference": [synthetic.mean()-real.mean(), synthetic.std()-real.std(), synthetic.skew()-real.skew(), np.sqrt(mean_squared_error(np.sort(real), np.sort(synthetic)))]})
