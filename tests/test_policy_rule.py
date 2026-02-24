"""اختبارات وحدة policy_rule."""
import pytest
from src.infl_scen.policy_rule import (
    TaylorParams,
    taylor_rate,
    rate_fan,
    rate_neutral,
)


class TestTaylorParams:
    """اختبارات فئة TaylorParams."""
    
    def test_default_params(self):
        """اختبر المعاملات الافتراضية."""
        params = TaylorParams()
        assert params.r_star == 0.5
        assert params.pi_star == 2.0


class TestTaylorRate:
    """اختبارات دالة taylor_rate."""
    
    def test_neutral_rate(self):
        """اختبر المعدل المحايد."""
        rate = taylor_rate(pi=2.0, u=4.2)
        assert rate == pytest.approx(2.5, abs=0.01)
    
    def test_higher_inflation(self):
        """اختبر معدل أعلى مع تضخم أعلى."""
        rate_low = taylor_rate(pi=2.0, u=4.2)
        rate_high = taylor_rate(pi=3.0, u=4.2)
        assert rate_high > rate_low
