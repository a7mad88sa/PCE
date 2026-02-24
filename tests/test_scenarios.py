"""اختبارات وحدة scenarios."""
import pytest
from src.infl_scen.scenarios import (
    PriceImpactAssumptions,
    ScenarioInputs,
    compute_outputs,
    prior_probability_35_40,
)
from src.infl_scen.expectations import MarketExpectations


class TestPriceImpactAssumptions:
    """اختبارات فئة PriceImpactAssumptions."""
    
    def test_valid_creation(self):
        """اختبر إنشاء صحيح."""
        assumptions = PriceImpactAssumptions(0.8, 0.7)
        assert assumptions.level_impact_end_pct == 0.8
        assert assumptions.realization_share_12m == 0.7
    
    def test_invalid_negative_impact(self):
        """اختبر رفض تأثير سالب."""
        with pytest.raises(ValueError):
            PriceImpactAssumptions(-0.5, 0.7)


class TestScenarioInputs:
    """اختبارات فئة ScenarioInputs."""
    
    def test_valid_creation(self):
        """اختبر إنشاء صحيح."""
        inputs = ScenarioInputs(
            current_pce_yoy=2.8,
            core_pce_3m_ann=2.5,
            price_impact=PriceImpactAssumptions(0.8, 0.7),
            expectations=MarketExpectations(t5yie=2.5, t5yifr=2.3)
        )
        assert inputs.current_pce_yoy == 2.8


class TestComputeOutputs:
    """اختبارات دالة compute_outputs."""
    
    def test_basic_scenario(self):
        """اختبر سيناريو أساسي."""
        inputs = ScenarioInputs(
            current_pce_yoy=2.8,
            core_pce_3m_ann=2.5,
            price_impact=PriceImpactAssumptions(0.8, 0.7),
            expectations=MarketExpectations(t5yie=2.5, t5yifr=2.3)
        )
        outputs = compute_outputs(inputs)
        
        assert outputs.yoy_contrib_from_tariffs_pp == pytest.approx(0.56, rel=0.01)
