# 📊 Inflation Scenario Engine
## محرك سيناريوهات التضخم

أداة متكاملة لحساب متغيرات تشغيلية (صدمات الرسوم، زخم Core PCE، مساهمة الرسوم في تضخم 12 شهراً، نطاق PCE متوقع، واحتمال 3.5–4%، ومروحة فائدة تايلور).

## ✅ المتطلبات

- Python 3.10+
- pandas >= 2.2.0
- openpyxl >= 3.1.0
- pyyaml >= 6.0.0

## 🚀 التشغيل السريع

```bash
pip install -r requirements.txt
pip install -e .

infl-scen \
  --tariffs-xlsx "data/TBL-Data-February-21-Tariff-Update-202602.xlsx" \
  --tariffs-sheet "T1" \
  --corepce-csvs "data/Table2_Personal_consumption_expenditures.csv" \
  --current-pce-yoy 2.9 \
  --t5yie 2.40 \
  --t5yifr 2.12 \
  --level-imp-end 0.6 \
  --verbose
```
