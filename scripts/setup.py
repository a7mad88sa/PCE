"""سكريبت إعداد المشروع."""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """تشغيل أمر وطباعة حالته."""
    print(f"\n{'='*50}")
    print(f"📌 {description}")
    print(f"{'='*50}")
    print(f"$ {cmd}\n")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - SUCCESS")
    else:
        print(f"❌ {description} - FAILED")
    
    return result.returncode == 0

def main():
    """الدالة الرئيسية."""
    print("\n" + "="*50)
    print("🚀 Inflation Scenario Engine - Setup")
    print("="*50 + "\n")
    
    # 1. إنشاء البيئة
    run_command(
        "python -m venv .venv",
        "Creating virtual environment"
    )
    
    # 2. تحديد أمر تفعيل البيئة حسب النظام
    activate_cmd = ". .venv/bin/activate &&" if sys.platform != "win32" else ".venv\\Scripts\\activate &&"
    
    # 3. تثبيت المتطلبات
    run_command(
        f"{activate_cmd} pip install --upgrade pip",
        "Upgrading pip"
    )
    
    run_command(
        f"{activate_cmd} pip install -r requirements.txt",
        "Installing dependencies"
    )
    
    # 4. تثبيت الحزمة
    run_command(
        f"{activate_cmd} pip install -e .",
        "Installing package"
    )
    
    # 5. إنشاء المجلدات
    print("\n📁 Creating directories...")
    for directory in ["data", "outputs", "configs", ".fred_cache"]:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")
    
    # 6. الملخص النهائي
    print("\n" + "="*50)
    print("✅ Setup Complete!")
    print("="*50)
    print("\n📋 Next Steps:")
    print("1. Activate environment:")
    if sys.platform == "win32":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("\n2. Add your data files to: data/")
    print("\n3. Run analysis:")
    print("   infl-scen --tariffs-xlsx ... --corepce-csvs ... (see README)")
    print("\n4. View dashboard:")
    if sys.platform == "darwin":
        print("   open outputs/dashboard.html")
    elif sys.platform == "win32":
        print("   start outputs/dashboard.html")
    else:
        print("   xdg-open outputs/dashboard.html")

if __name__ == "__main__":
    main()
