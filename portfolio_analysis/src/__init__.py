"""Portfolio analysis utilities inspired by the public SWS Portfolio Analysis Model."""

from .portfolio_analysis_model import (
    PortfolioConfig,
    normalize_transactions,
    build_holdings_from_transactions,
    make_equal_weight_watchlist,
    portfolio_snowflake,
    portfolio_intrinsic_value,
    dollar_weighted_return,
    time_weighted_returns,
    portfolio_metric_summary,
    analyze_portfolio,
    export_portfolio_analysis,
)

__all__ = [
    "PortfolioConfig",
    "normalize_transactions",
    "build_holdings_from_transactions",
    "make_equal_weight_watchlist",
    "portfolio_snowflake",
    "portfolio_intrinsic_value",
    "dollar_weighted_return",
    "time_weighted_returns",
    "portfolio_metric_summary",
    "analyze_portfolio",
    "export_portfolio_analysis",
]
