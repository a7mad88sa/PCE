from __future__ import annotations
from dataclasses import dataclass
from .expectations import MarketExpectations


@dataclass
class PriceImpactAssumptions:
    level_impact_end_pct: float
    realization_share_12m: float

    def __post_init__(self):
        if self.level_impact_end_pct < 0.0:
            raise ValueError("level_impact_end_pct must be non-negative")
        if self.realization_share_12m < 0.0 or self.realization_share_12m > 1.0:
            raise ValueError("realization_share_12m must be between 0 and 1")


@dataclass
class ScenarioInputs:
    current_pce_yoy: float
    core_pce_3m_ann: float
    price_impact: PriceImpactAssumptions
    expectations: MarketExpectations


@dataclass
class ScenarioOutputs:
    yoy_contrib_from_tariffs_pp: float = 0.0


def compute_outputs(inputs: ScenarioInputs) -> ScenarioOutputs:
    """حساب مخرجات مبسطة: مساهمة الرسوم تساوي level * realization."""
    contrib = inputs.price_impact.level_impact_end_pct * inputs.price_impact.realization_share_12m
    return ScenarioOutputs(yoy_contrib_from_tariffs_pp=contrib)


def prior_probability_35_40(*args, **kwargs):
    # placeholder
    return 0.0
