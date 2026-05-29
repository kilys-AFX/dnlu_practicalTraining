"""
Simple verification script for Phase 2 completion
Check if all required files exist and have no syntax errors
"""

import os
import sys
import ast

def check_file_exists(filepath):
    """Check if file exists"""
    if os.path.exists(filepath):
        print(f"✅ File exists: {filepath}")
        return True
    else:
        print(f"❌ File missing: {filepath}")
        return False

def check_python_syntax(filepath):
    """Check Python file syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print(f"✅ Syntax OK: {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax Error in {filepath}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Could not check {filepath}: {e}")
        return False

def main():
    """Main verification function"""
    print("=" * 60)
    print("Phase 2 Verification Script")
    print("=" * 60)
    
    # Define required files
    required_files = [
        "app.py",
        "pages/realtime_dashboard.py",
        "pages/anomaly_detection.py",
        "pages/ai_assistant.py",
        "pages/pdf_export.py",
        "utils/pdf_generator.py",
        "utils/data_processor.py",
        "config/settings.py",
        "data/database.py",
    ]
    
    print("\n📂 Checking required files...")
    all_exist = True
    for filepath in required_files:
        if not check_file_exists(filepath):
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some required files are missing!")
        return False
    
    print("\n🔍 Checking Python syntax...")
    all_syntax_ok = True
    for filepath in required_files:
        if not check_python_syntax(filepath):
            all_syntax_ok = False
    
    if not all_syntax_ok:
        print("\n❌ Some files have syntax errors!")
        return False
    
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    print("✅ All required files exist")
    print("✅ All Python files have valid syntax")
    print("✅ Phase 2 implementation looks complete")
    
    print("\n📋 Next Steps:")
    print("1. Run: streamlit run app.py")
    print("2. Click 'Generate Mock Data' to create test data")
    print("3. Navigate to different modules to test functionality")
    print("4. Check real-time dashboard, anomaly detection, AI assistant, PDF export")
    
    print("\n🎉 Phase 2 verification completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
