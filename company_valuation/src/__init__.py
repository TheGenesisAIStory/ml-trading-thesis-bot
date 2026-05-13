"""Reusable helpers for the company valuation research pipeline."""

__version__ = "0.1.0"

from .company_valuation_utils import (
    normalize_ticker,
    safe_rank,
    latest_per_ticker,
    performance_stats_from_returns,
    estimate_intrinsic_value,
    build_output_dirs,
)
from .sws_company_analysis_model import (
    SWSModelConfig,
    CheckResult,
    analyze_company,
    score_companies,
    estimate_sws_fair_value,
    two_stage_fcf_value_per_share,
    dividend_discount_value_per_share,
    excess_returns_value_per_share,
    relative_value_per_share,
    weighted_linear_growth,
)

__all__ = [
    "__version__",
    "normalize_ticker",
    "safe_rank",
    "latest_per_ticker",
    "performance_stats_from_returns",
    "estimate_intrinsic_value",
    "build_output_dirs",
    "SWSModelConfig",
    "CheckResult",
    "analyze_company",
    "score_companies",
    "estimate_sws_fair_value",
    "two_stage_fcf_value_per_share",
    "dividend_discount_value_per_share",
    "excess_returns_value_per_share",
    "relative_value_per_share",
    "weighted_linear_growth",
]
