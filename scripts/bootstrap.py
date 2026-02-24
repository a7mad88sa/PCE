#!/usr/bin/env python3
"""
سكريبت إعداد وتشغيل مشروع Inflation Scenario Engine بالكامل
يقوم بكل شيء تلقائياً بدون تدخل يدوي
"""

import os
import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime

# ألوان للإخراج
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """اطبع رأس قسم"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_step(step_num, text):
    """اطبع خطوة"""
    print(f"{Colors.CYAN}[{step_num}]{Colors.END} {Colors.BOLD}{text}{Colors.END}")

def print_success(text):
    """اطبع رسالة نجاح"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """اطبع رسالة خطأ"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """اطبع تحذير"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def run_command(cmd, description, show_output=True):
    """تشغيل أمر في Terminal"""
    print_step("CMD", description)
    print(f"{Colors.WHITE}$ {cmd}{Colors.END}")
    
    try:
        if show_output:
            result = subprocess.run(cmd, shell=True, check=True)
        else:
            result = subprocess.run(cmd, shell=True, check=True, 
                                  capture_output=True, text=True)
        print_success(description)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} - فشل!")
        print(f"{Colors.RED}{e}{Colors.END}")
        return False

def create_file(path, content, description):
    """إنشاء ملف بمحتوى"""
    print_step("FILE", f"Creating {path}")
    
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        print_success(f"Created: {path}")
        return True
    except Exception as e:
        print_error(f"Failed to create {path}: {e}")
        return False

def create_directory(path):
    """إنشاء مجلد"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        print_success(f"Created directory: {path}")
        return True
    except Exception as e:
        print_error(f"Failed to create directory {path}: {e}")
        return False

def setup_directories():
    """إنشاء هيكل المجلدات"""
    print_header("📁 إنشاء هيكل المجلدات")
    
    directories = [
        'src',
        'src/infl_scen',
        'tests',
        'configs',
        'data',
        'outputs',
        '.fred_cache',
    ]
    
    for directory in directories:
        create_directory(directory)

def setup_init_files():
    """إنشاء ملفات __init__.py"""
    print_header("📝 إنشاء ملفات __init__.py")
    
    init_content = '"""Inflation Scenario Engine Package"""\n'
    
    files = [
        'src/__init__.py',
        'tests/__init__.py',
    ]
    
    for file in files:
        create_file(file, init_content, f"Creating {file}")

def setup_test_files():
    """إنشاء ملفات الاختبارات"""
    print_header("🧪 إنشاء ملفات الاختبارات")
    
    # test_transforms.py
    test_transforms = '''"""اختبارات وحدة transforms."""
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
'''
    
    create_file('tests/test_transforms.py', test_transforms, "Creating test_transforms.py")
    
    # test_scenarios.py
    test_scenarios = '''"""اختبارات وحدة scenarios."""
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
'''
    
    create_file('tests/test_scenarios.py', test_scenarios, "Creating test_scenarios.py")
    
    # test_policy_rule.py
    test_policy_rule = '''"""اختبارات وحدة policy_rule."""
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
'''
    
    create_file('tests/test_policy_rule.py', test_policy_rule, "Creating test_policy_rule.py")

def create_requirements():
    """إنشاء requirements.txt"""
    print_header("📦 إنشاء requirements.txt")
    
    requirements = """pandas>=2.2.0
openpyxl>=3.1.0
pyyaml>=6.0.0
pytest>=7.0.0
pytest-cov>=4.0.0
"""
    
    create_file('requirements.txt', requirements, "Creating requirements.txt")

def create_pyproject():
    """إنشاء pyproject.toml"""
    print_header("⚙️  إنشاء pyproject.toml")
    
    pyproject = """[project]
name = "inflation-scenario-engine"
version = "0.1.0"
description = "محرك سيناريوهات التضخم - Inflation Scenario Engine"
authors = [{name = "Inflation Analysis Team"}]
requires-python = ">=3.10"
dependencies = [
    "pandas>=2.2.0",
    "openpyxl>=3.1.0",
    "pyyaml>=6.0.0"
]

[project.scripts]
infl-scen = "src.infl_scen.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
"""
    
    create_file('pyproject.toml', pyproject, "Creating pyproject.toml")

def create_gitignore():
    """إنشاء .gitignore"""
    print_header("🔒 إنشاء .gitignore")
    
    gitignore = """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/
htmlcov/
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
outputs/
data/
*.xlsx
*.csv
!configs/
.env
.venv
venv/
.fred_cache/
"""
    
    create_file('.gitignore', gitignore, "Creating .gitignore")

def create_readme():
    """إنشاء README.md"""
    print_header("📖 إنشاء README.md")
    
    readme = """# 📊 Inflation Scenario Engine
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

infl-scen \\
  --tariffs-xlsx "data/TBL-Data-February-21-Tariff-Update-202602.xlsx" \\
  --tariffs-sheet "T1" \\
  --corepce-csvs "data/Table2_Personal_consumption_expenditures.csv" \\
  --current-pce-yoy 2.9 \\
  --t5yie 2.40 \\
  --t5yifr 2.12 \\
  --level-imp-end 0.6 \\
  --verbose
```
"""
    
    create_file('README.md', readme, "Creating README.md")

def main():
    print_header("Inflation Scenario Engine - Bootstrap")
    setup_directories()
    setup_init_files()
    setup_test_files()
    create_requirements()
    create_pyproject()
    create_gitignore()
    create_readme()
    print_success("Bootstrap completed. Run 'pip install -r requirements.txt' inside a venv to continue.")

if __name__ == '__main__':
    main()
