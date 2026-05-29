"""
Test Installation - Verify all dependencies
"""
import sys
import os

# Set encoding to UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

def test_imports():
    """Test all necessary imports"""
    print("=" * 50)
    print("Testing imports...")
    print("=" * 50)
    
    tests = []
    
    # Test streamlit
    try:
        import streamlit as st
        tests.append(("OK", "Streamlit", st.__version__))
    except ImportError as e:
        tests.append(("FAIL", "Streamlit", str(e)))
    
    # Test pandas
    try:
        import pandas as pd
        tests.append(("OK", "Pandas", pd.__version__))
    except ImportError as e:
        tests.append(("FAIL", "Pandas", str(e)))
    
    # Test plotly
    try:
        import plotly as px
        tests.append(("OK", "Plotly", px.__version__))
    except ImportError as e:
        tests.append(("FAIL", "Plotly", str(e)))
    
    # Test sklearn
    try:
        import sklearn
        tests.append(("OK", "Scikit-learn", sklearn.__version__))
    except ImportError as e:
        tests.append(("FAIL", "Scikit-learn", str(e)))
    
    # Test sqlite3
    try:
        import sqlite3
        tests.append(("OK", "SQLite3", sqlite3.sqlite_version))
    except ImportError as e:
        tests.append(("FAIL", "SQLite3", str(e)))
    
    # Test openpyxl
    try:
        import openpyxl
        tests.append(("OK", "Openpyxl", openpyxl.__version__))
    except ImportError as e:
        tests.append(("FAIL", "Openpyxl", str(e)))
    
    # Print results
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    
    for status, name, version in tests:
        print(f"[{status}] {name}: {version}")
    
    print("\n" + "=" * 50)
    
    # Check for failures
    failed = [t for t in tests if t[0] == "FAIL"]
    
    if failed:
        print(f"\n[FAIL] {len(failed)} tests failed")
        return False
    else:
        print("\n[SUCCESS] All tests passed!")
        return True


def test_database():
    """Test database initialization"""
    print("\n" + "=" * 50)
    print("Testing database...")
    print("=" * 50)
    
    try:
        from data.database import init_database, execute_query
        
        # Initialize database
        init_database()
        
        # Test query
        result = execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        
        print(f"[OK] Database initialized successfully")
        print(f"     Created {len(result)} tables: {result['name'].tolist()}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Database test failed: {e}")
        return False


def test_data_generator():
    """Test data generator"""
    print("\n" + "=" * 50)
    print("Testing data generator...")
    print("=" * 50)
    
    try:
        from data.data_generator import generate_users, generate_products
        
        # Generate test data
        users = generate_users(10)
        products = generate_products(5)
        
        print(f"[OK] Data generator works")
        print(f"     Generated {len(users)} users")
        print(f"     Generated {len(products)} products")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Data generator failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Retail Analytics System - Installation Test")
    print("=" * 50)
    
    # Test imports
    import_success = test_imports()
    
    if import_success:
        # Test database
        db_success = test_database()
        
        # Test data generator
        data_success = test_data_generator()
        
        if db_success and data_success:
            print("\n" + "=" * 50)
            print("[SUCCESS] All tests passed! Ready to run.")
            print("=" * 50)
            print("\nRun command:")
            print("  cd d:\\codebuddy\\education\\retail_analytics")
            print("  streamlit run app.py")
        else:
            print("\n[FAIL] Some tests failed. Check errors above.")
    else:
        print("\n[FAIL] Import tests failed. Check dependencies.")
        print("\nReinstall:")
        print("  pip install -r requirements.txt")
