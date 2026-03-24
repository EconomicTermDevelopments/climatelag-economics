"""
Climatelag: computational implementation for environmental/climate economics analysis.

Climatelag refers to temporal delay between greenhouse gas emissions and resulting climate impacts creating intertemporal externalities. This module provides a reproducible calculator that validates the canonical channels, normalizes each series, computes a weighted index, and supports simple counterfactual policy simulation. The design is intentionally transparent so researchers can inspect how the concept moves from definition to code. Typical uses include comparative diagnostics, notebook-based scenario testing, and integration into empirical pipelines where consistent measurement matters as much as prediction.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

# Climatelag channels track the observable anatomy of the canonical definition.
TERM_CHANNELS = [
    "emission_flow",  # Emission flow captures a distinct economic channel.
    "atmospheric_stock",  # Atmospheric stock captures a distinct economic channel.
    "response_delay",  # Response delay captures a distinct economic channel.
    "damage_realization_lag",  # Damage realization lag captures a distinct economic channel.
    "policy_delay",  # Policy delay captures a distinct economic channel.
    "discounting_bias",  # Discounting bias captures a distinct economic channel.
    "adaptation_capacity",  # Adaptation capacity mitigates exposure when it is high.
]

# Weighted channels preserve the repository's existing score logic.
WEIGHTED_CHANNELS = [
    "emission_flow",
    "atmospheric_stock",
    "response_delay",
    "damage_realization_lag",
    "policy_delay",
    "discounting_bias",
    "adaptation_capacity",
]

# Default weights encode the relative economic importance of each weighted channel.
DEFAULT_WEIGHTS: dict[str, float] = {
    "emission_flow": 0.16,  # Emission flow captures a distinct economic channel.
    "atmospheric_stock": 0.18,  # Atmospheric stock captures a distinct economic channel.
    "response_delay": 0.18,  # Response delay captures a distinct economic channel.
    "damage_realization_lag": 0.16,  # Damage realization lag captures a distinct economic channel.
    "policy_delay": 0.14,  # Policy delay captures a distinct economic channel.
    "discounting_bias": 0.1,  # Discounting bias captures a distinct economic channel.
    "adaptation_capacity": 0.08,  # Adaptation capacity mitigates exposure when it is high.
}


class ClimatelagCalculator:
    """
    Compute Climatelag index scores from tabular data.

    Parameters
    ----------
    weights : dict[str, float] | None
        Optional weights overriding DEFAULT_WEIGHTS. Keys must match
        WEIGHTED_CHANNELS and values must sum to 1.0.
    """

    def __init__(self, weights: Optional[dict[str, float]] = None) -> None:
        # Alternative weights are useful for robustness checks across specifications.
        self.weights = weights or DEFAULT_WEIGHTS.copy()

        # Exact key matching prevents silent omission of economically relevant channels.
        if set(self.weights) != set(WEIGHTED_CHANNELS):
            raise ValueError(f"Weights must include exactly these channels: {WEIGHTED_CHANNELS}")

        # Unit-sum weights keep the index interpretable across datasets.
        if abs(sum(self.weights.values()) - 1.0) >= 1e-6:
            raise ValueError("Weights must sum to 1.0")

    @staticmethod
    def _normalise(series: pd.Series) -> pd.Series:
        """
        Return min-max normalized values on the unit interval.
        """
        lo = float(series.min())
        hi = float(series.max())
        if hi == lo:
            # Degenerate channels should not create spurious variation.
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - lo) / (hi - lo)

    def calculate_climatelag(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute normalized channels, composite scores, and qualitative bands.
        """
        # Full channel validation keeps the score tied to the canonical definition.
        missing = [channel for channel in TERM_CHANNELS if channel not in df.columns]
        if missing:
            raise ValueError(f"Missing Climatelag channels: {missing}")

        out = df.copy()
        for channel in TERM_CHANNELS:
            out[f"{channel}_norm"] = self._normalise(out[channel])

        # Positive channels intensify the mechanism while negative channels offset it.
        out["climatelag_index"] = (
            + self.weights["emission_flow"] * out["emission_flow_norm"]
            + self.weights["atmospheric_stock"] * out["atmospheric_stock_norm"]
            + self.weights["response_delay"] * out["response_delay_norm"]
            + self.weights["damage_realization_lag"] * out["damage_realization_lag_norm"]
            + self.weights["policy_delay"] * out["policy_delay_norm"]
            + self.weights["discounting_bias"] * out["discounting_bias_norm"]
            + self.weights["adaptation_capacity"] * (1.0 - out["adaptation_capacity_norm"])
        )

        # Three bands keep the metric usable in audits, papers, and dashboards.
        out["climatelag_band"] = pd.cut(
            out["climatelag_index"],
            bins=[-np.inf, 0.33, 0.66, np.inf],
            labels=["low", "moderate", "high"],
        )
        return out

    def simulate_policy(self, df: pd.DataFrame, channel: str, reduction: float = 0.2) -> pd.DataFrame:
        """
        Simulate a policy shock that reduces one observed channel.
        """
        if channel not in TERM_CHANNELS:
            raise ValueError(f"Unknown Climatelag channel: {channel}")
        if reduction < 0.0 or reduction > 1.0:
            raise ValueError("reduction must be between 0.0 and 1.0")

        # Counterfactual shocks translate reforms into score movements.
        df_policy = df.copy()
        df_policy[channel] = df_policy[channel] * (1 - reduction)
        return self.calculate_climatelag(df_policy)


if __name__ == "__main__":
    sample = pd.read_csv("climatelag_dataset.csv")
    calc = ClimatelagCalculator()
    print(calc.calculate_climatelag(sample)[["climatelag_index", "climatelag_band"]].head(10).to_string(index=False))

    scenario = calc.simulate_policy(sample, channel="emission_flow", reduction=0.15)
    print("\nPolicy Scenario Mean Index:")
    print(float(scenario["climatelag_index"].mean()))
