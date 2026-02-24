"""تحويلات مساعدة للاختبارات البسيطة"""
from __future__ import annotations

def three_month_annualized_from_pct(r1: float, r2: float, r3: float) -> float:
    """حساب معدل سنوي مبسط من ثلاث قيم (بالنسبة المئوية).

    الصيغة المبسطة: annual = (1 + (r1 + r2 + r3)/100) ** 4 - 1
    حيث يُفترض أن القيم معطاة كنقاط مئوية صغيرة مثل 0.3 (أي 0.3%).
    """
    total_pct = r1 + r2 + r3
    return (1.0 + total_pct / 100.0) ** 4 - 1.0

def level_shock_to_yoy_contribution(level_imp_end_pct: float, realization_share_12m: float) -> float:
    """تحويل صدمة مستوى إلى مساهمة YoY بسيطة.

    يتحقق شرط أن نسبة التحقيق بين 0 و1.
    """
    if realization_share_12m < 0.0 or realization_share_12m > 1.0:
        raise ValueError("realization_share_12m must be between 0 and 1")
    return level_imp_end_pct * realization_share_12m
