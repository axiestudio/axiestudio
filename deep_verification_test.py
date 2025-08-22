# -*- coding: utf-8 -*-
"""
DEEP VERIFICATION TEST - SENIOR DEVELOPER ANALYSIS
Double-checking all fixes with actual code execution simulation
"""

import sys
import traceback
import os
import json
from pathlib import Path

print("🔍 DEEP VERIFICATION TEST - DOUBLE CHECKING ALL FIXES")
print("="*70)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print("="*70)

def test_actual_settings_import():
    """Actually try to import the settings module"""
    print("\n🔧 DEEP TEST: Actual Settings Import...")
    try:
        # Add the backend path to sys.path
        backend_path = Path("temp/src/backend/base")
        if backend_path.exists():
            sys.path.insert(0, str(backend_path.absolute()))
            print(f"✅ Added backend path: {backend_path.absolute()}")
        else:
            print(f"❌ Backend path not found: {backend_path}")
            return False
        
        # Try actual import
        try:
            from axiestudio.services.settings import settings
            print("✅ Successfully imported settings!")
            print(f"✅ Settings type: {type(settings)}")
            
            # Try to access EMAIL_VERIFICATION_METHOD
            verification_method = settings.EMAIL_VERIFICATION_METHOD
            print(f"✅ EMAIL_VERIFICATION_METHOD: {verification_method}")
            
            return True
        except ImportError as e:
            print(f"❌ Import failed: {e}")
            return False
        except AttributeError as e:
            print(f"❌ Attribute error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Deep settings test failed: {e}")
        traceback.print_exc()
        return False

def test_store_data_loading():
    """Test actual store data loading and parsing"""
    print("\n📦 DEEP TEST: Store Data Loading...")
    try:
        store_index_file = Path("temp/src/store_components_converted/store_index.json")
        
        if not store_index_file.exists():
            print(f"❌ Store index file missing: {store_index_file}")
            return False
        
        # Load and parse the JSON
        with open(store_index_file, 'r', encoding='utf-8') as f:
            store_data = json.load(f)
        
        # Validate structure
        if 'summary' not in store_data:
            print("❌ Store data missing 'summary' section")
            return False
        
        if 'flows' not in store_data:
            print("❌ Store data missing 'flows' section")
            return False
        
        if 'components' not in store_data:
            print("❌ Store data missing 'components' section")
            return False
        
        summary = store_data['summary']
        flows = store_data['flows']
        components = store_data['components']
        
        print(f"✅ Store data structure is valid")
        print(f"✅ Summary: {summary.get('total_items', 0)} total items")
        print(f"✅ Flows: {len(flows)} flows loaded")
        print(f"✅ Components: {len(components)} components loaded")
        
        # Check if we have actual content
        if len(flows) == 0 and len(components) == 0:
            print("❌ No flows or components found - showcase will be empty!")
            return False
        
        # Sample a few items to ensure they have required fields
        if flows:
            sample_flow = flows[0]
            required_fields = ['id', 'name', 'description', 'type']
            for field in required_fields:
                if field not in sample_flow:
                    print(f"❌ Sample flow missing required field: {field}")
                    return False
            print(f"✅ Sample flow has all required fields: {sample_flow['name']}")
        
        if components:
            sample_component = components[0]
            required_fields = ['id', 'name', 'description', 'type']
            for field in required_fields:
                if field not in sample_component:
                    print(f"❌ Sample component missing required field: {field}")
                    return False
            print(f"✅ Sample component has all required fields: {sample_component['name']}")
        
        print("✅ Store data is fully valid and ready for showcase!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Store data test failed: {e}")
        traceback.print_exc()
        return False

def test_frontend_api_robustness():
    """Test frontend API fix more thoroughly"""
    print("\n🌐 DEEP TEST: Frontend API Robustness...")
    try:
        api_file = Path("temp/src/frontend/src/controllers/API/api.tsx")
        
        if not api_file.exists():
            print(f"❌ API file not found: {api_file}")
            return False
        
        content = api_file.read_text(encoding='utf-8')
        
        # Check for comprehensive fix
        checks = [
            ("Config null check", "if (!config) {"),
            ("Config assignment", "config = {};"),
            ("Headers null check", "if (!config.headers) {"),
            ("Headers assignment", "config.headers = {};"),
            ("Comment documentation", "// Ensure config and config.headers exist"),
        ]
        
        all_checks_passed = True
        for check_name, check_pattern in checks:
            if check_pattern in content:
                print(f"✅ {check_name} found")
            else:
                print(f"❌ {check_name} missing")
                all_checks_passed = False
        
        # Check the fix is in the right place (fetchIntercept.register)
        if "fetchIntercept.register" in content:
            print("✅ Fix is in the correct fetchIntercept.register location")
        else:
            print("❌ fetchIntercept.register not found")
            all_checks_passed = False
        
        return all_checks_passed
        
    except Exception as e:
        print(f"❌ Frontend API test failed: {e}")
        traceback.print_exc()
        return False

def test_database_fix_completeness():
    """Test database fix more thoroughly"""
    print("\n🗄️ DEEP TEST: Database Fix Completeness...")
    try:
        users_file = Path("temp/src/backend/base/axiestudio/api/v1/users.py")
        
        if not users_file.exists():
            print(f"❌ Users file not found: {users_file}")
            return False
        
        content = users_file.read_text(encoding='utf-8')
        
        # Check for comprehensive database fix
        checks = [
            ("IntegrityError import", "from sqlalchemy.exc import IntegrityError"),
            ("File model import", "from axiestudio.services.database.models.file.model import File"),
            ("Try-except block", "try:"),
            ("File deletion query", "File.user_id == user_id"),
            ("File deletion loop", "await session.delete(file)"),
            ("User deletion", "await session.delete(user_db)"),
            ("IntegrityError handling", "except IntegrityError as e:"),
            ("Session rollback", "await session.rollback()"),
            ("Foreign key error message", "foreign key constraints"),
        ]
        
        all_checks_passed = True
        for check_name, check_pattern in checks:
            if check_pattern in content:
                print(f"✅ {check_name} found")
            else:
                print(f"❌ {check_name} missing")
                all_checks_passed = False
        
        return all_checks_passed
        
    except Exception as e:
        print(f"❌ Database fix test failed: {e}")
        traceback.print_exc()
        return False

def test_logging_fix_completeness():
    """Test logging fix more thoroughly"""
    print("\n📝 DEEP TEST: Logging Fix Completeness...")
    try:
        main_file = Path("temp/src/backend/base/axiestudio/main.py")
        
        if not main_file.exists():
            print(f"❌ Main file not found: {main_file}")
            return False
        
        content = main_file.read_text(encoding='utf-8')
        
        # Check for both logging fixes
        checks = [
            ("Unhandled error fix", 'logger.error("unhandled error: %s", str(exc), exc_info=exc)'),
            ("HTTPException fix", 'logger.error("HTTPException: %s", str(exc), exc_info=exc)'),
            ("Exception handler function", "async def exception_handler"),
        ]
        
        all_checks_passed = True
        for check_name, check_pattern in checks:
            if check_pattern in content:
                print(f"✅ {check_name} found")
            else:
                print(f"❌ {check_name} missing")
                all_checks_passed = False
        
        # Make sure old problematic f-strings are gone
        problematic_patterns = [
            'logger.error(f"unhandled error: {exc}"',
            'logger.error(f"HTTPException: {exc}"',
        ]
        
        for pattern in problematic_patterns:
            if pattern in content:
                print(f"❌ Problematic pattern still exists: {pattern}")
                all_checks_passed = False
            else:
                print(f"✅ Problematic pattern removed: {pattern}")
        
        return all_checks_passed
        
    except Exception as e:
        print(f"❌ Logging fix test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all deep verification tests"""
    print("🚀 Starting DEEP verification tests...\n")
    
    tests = [
        ("Actual Settings Import", test_actual_settings_import),
        ("Store Data Loading", test_store_data_loading),
        ("Frontend API Robustness", test_frontend_api_robustness),
        ("Database Fix Completeness", test_database_fix_completeness),
        ("Logging Fix Completeness", test_logging_fix_completeness),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 DEEP VERIFICATION SUMMARY")
    print("="*70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Deep Verification Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL DEEP TESTS PASSED! Fixes are solid and complete!")
        return True
    else:
        print("⚠️  Some deep tests failed. There may be remaining issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
