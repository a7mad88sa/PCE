"""اختبارات وحدة transforms."""
import pytest
from src.infl_scen.transforms import (
    three_month_annualized_from_pct,
    level_shock_to_yoy_contribution,
)


class TestThreeMonthAnnualized:
    """اختبارات دالة three_month_annualized_from_pct."""
    
    def test_typical_case(self):
        """0.2%, 0.2%, 0.4% => ~3.25% سنوياً."""
        result = three_month_annualized_from_pct(0.2, 0.2, 0.4) * 100.0
        assert 2.5 < result < 4.2
    
    def test_equal_rates(self):
        """معدلات متساوية."""
        result = three_month_annualized_from_pct(0.3, 0.3, 0.3) * 100.0
        assert result == pytest.approx(3.66, rel=0.01)
    
    def test_zero_rates(self):
        """معدلات صفرية."""
        result = three_month_annualized_from_pct(0.0, 0.0, 0.0)
        assert result == pytest.approx(0.0, abs=1e-10)


class TestLevelToYoY:
    """اختبارات دالة level_shock_to_yoy_contribution."""
    
    def test_typical_case(self):
        """0.8 * 0.75 = 0.6."""
        result = level_shock_to_yoy_contribution(0.8, 0.75)
        assert result == pytest.approx(0.6, abs=1e-8)
    
    def test_full_realization(self):
        """تحقق كامل الصدمة (100%)."""
        result = level_shock_to_yoy_contribution(1.0, 1.0)
        assert result == pytest.approx(1.0, abs=1e-8)
    
    def test_no_realization(self):
        """عدم تحقق الصدمة (0%)."""
        result = level_shock_to_yoy_contribution(1.0, 0.0)
        assert result == pytest.approx(0.0, abs=1e-8)
    
    def test_partial_realization(self):
        """تحقق جزئي."""
        result = level_shock_to_yoy_contribution(2.0, 0.5)
        assert result == pytest.approx(1.0, abs=1e-8)
    
    def test_invalid_realization_above_one(self):
        """نسبة تحقق أكبر من 1."""
        with pytest.raises(ValueError):
            level_shock_to_yoy_contribution(0.8, 1.5)
    
    def test_invalid_realization_negative(self):
        """نسبة تحقق سالبة."""
        with pytest.raises(ValueError):
            level_shock_to_yoy_contribution(0.8, -0.1)
