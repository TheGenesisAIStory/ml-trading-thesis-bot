"""Reusable ingestion helpers for the PEAD European banks IFRS9 notebook.

The functions are designed to reuse the database objects from the user's central
Untitled2 / valuation notebook environment (`DB_ROOT`, `FILE_MAP`, `load_file`)
when available, while remaining importable from scripts and tests.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
import pandas as pd


def normalize_price_panel(raw: pd.DataFrame, logger: logging.Logger | None = None) -> pd.DataFrame:
    """Normalize a raw market panel to ticker/date/OHLCV columns."""
    logger = logger or logging.getLogger("pead_loader")
    if raw is None or raw.empty:
        raise ValueError("raw price panel is empty")

    df = raw.copy()
    cols_lower = {str(c).lower(): c for c in df.columns}
    date_col = next((cols_lower[c] for c in ["date", "datetime", "timestamp"] if c in cols_lower), None)
    ticker_col = next((cols_lower[c] for c in ["ticker", "symbol", "asset"] if c in cols_lower), None)
    price_col = next((cols_lower[c] for c in ["adj_close", "adj close", "close", "price", "adjusted"] if c in cols_lower), None)
    volume_col = next((c for c in df.columns if "vol" in str(c).lower()), None)

    missing = [name for name, col in {"date": date_col, "ticker": ticker_col, "close": price_col}.items() if col is None]
    if missing:
        raise ValueError(f"price panel missing columns: {missing}")

    rename = {date_col: "date", ticker_col: "ticker", price_col: "close"}
    if volume_col:
        rename[volume_col] = "volume"
    df = df.rename(columns=rename)
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.tz_localize(None)
    df["ticker"] = df["ticker"].astype(str).str.strip().str.upper()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    if "volume" in df.columns:
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce")
    else:
        df["volume"] = np.nan

    for col in ["open", "high", "low"]:
        if col not in df.columns:
            df[col] = df["close"]
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(df["close"])

    df = df.dropna(subset=["date", "ticker", "close"])
    df = df[df["close"] > 0].copy()
    df = df.sort_values(["ticker", "date"]).drop_duplicates(["ticker", "date"], keep="last")
    logger.info("normalized price panel shape=%s tickers=%s", df.shape, df["ticker"].nunique())
    return df[["ticker", "date", "open", "high", "low", "close", "volume"]].reset_index(drop=True)


def make_synthetic_bank_prices(
    bank_tickers: Iterable[str],
    start_date: str,
    end_date: str,
    seed: int = 42,
) -> pd.DataFrame:
    """Create realistic synthetic daily bank prices for fallback runs."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start_date, end_date)
    frames = []
    market = rng.normal(0.00015, 0.010, len(dates))
    for idx, ticker in enumerate(bank_tickers):
        beta = rng.normal(1.15, 0.18)
        idio = rng.normal(0.00002, 0.014 + idx * 0.0007, len(dates))
        ret = beta * market + idio
        close = (35 + idx * 4) * np.exp(np.cumsum(ret))
        volume = np.exp(rng.normal(14.5, 0.35, len(dates)))
        frame = pd.DataFrame({"ticker": ticker, "date": dates, "close": close, "volume": volume})
        frame["open"] = frame["close"] * (1 + rng.normal(0, 0.002, len(frame)))
        frame["high"] = frame[["open", "close"]].max(axis=1) * (1 + np.abs(rng.normal(0, 0.004, len(frame))))
        frame["low"] = frame[["open", "close"]].min(axis=1) * (1 - np.abs(rng.normal(0, 0.004, len(frame))))
        frame["prices_synthetic"] = True
        frames.append(frame[["ticker", "date", "open", "high", "low", "close", "volume", "prices_synthetic"]])
    return pd.concat(frames, ignore_index=True)


def load_pead_data_from_db(
    bank_tickers: list[str],
    start_date: str,
    end_date: str,
    db_root: str | Path | None = None,
    file_map: dict | None = None,
    load_file: Callable[[Path], pd.DataFrame] | None = None,
    logger: logging.Logger | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame | None]:
    """Load PEAD prices and optional risk factors from the central financial DB.

    Parameters mirror the objects created by the user's Untitled2 notebook. The
    function raises clear errors instead of silently falling back; the notebook
    decides whether to call synthetic fallback after logging the failure.
    """
    logger = logger or logging.getLogger("pead_loader")
    if db_root is None:
        raise RuntimeError("DB_ROOT not provided; mount/load the central financial database first")
    if load_file is None:
        raise RuntimeError("load_file callable not provided from Untitled2 environment")

    db_root = Path(db_root)
    candidate_paths = [
        db_root / "ml_trading_market_prices_csv",
        db_root / "ml_trading_market_prices_csv.csv",
        db_root / "ml_trading_market_prices.csv",
        db_root / "ml_trading_market_prices.parquet",
    ]
    price_path = next((path for path in candidate_paths if path.exists()), None)
    if price_path is None:
        raise FileNotFoundError("ml_trading_market_prices file not found in DB_ROOT")

    raw_prices = load_file(price_path)
    prices = normalize_price_panel(raw_prices, logger=logger)
    prices = prices[prices["ticker"].isin([t.upper() for t in bank_tickers])].copy()
    prices = prices[(prices["date"] >= pd.Timestamp(start_date)) & (prices["date"] <= pd.Timestamp(end_date))]
    if prices.empty:
        raise RuntimeError("price panel loaded but no requested bank tickers/date range matched")

    ff_factors = None
    ff_path = None
    if file_map and "risk_factors" in file_map:
        local = file_map["risk_factors"].get("local") if isinstance(file_map["risk_factors"], dict) else file_map["risk_factors"]
        ff_path = Path(local) if local else None
    if ff_path and ff_path.exists():
        try:
            ff = load_file(ff_path)
            date_col = next((c for c in ff.columns if str(c).lower() in ["date", "datetime"]), None)
            if date_col:
                ff = ff.rename(columns={date_col: "date"})
            ff["date"] = pd.to_datetime(ff["date"], errors="coerce")
            ff_factors = ff.dropna(subset=["date"]).set_index("date").sort_index()
            logger.info("loaded risk factors shape=%s", ff_factors.shape)
        except Exception as exc:
            logger.warning("risk factors unavailable from DB: %s", exc)

    logger.info("PEAD DB prices shape=%s tickers=%s", prices.shape, prices["ticker"].nunique())
    return prices.reset_index(drop=True), ff_factors
