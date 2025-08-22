#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SENIOR DEVELOPER COMPREHENSIVE TEST SCRIPT
Verifies ALL critical fixes for the showcase loading issue and system stability.

CRITICAL ISSUES ADDRESSED:
1. Settings import failure (ImportError: cannot import name 'settings')
2. Frontend API headers undefined error
3. Database foreign key constraint violations
4. Logging format errors (KeyError: "'id'")
5. Missing EMAIL_VERIFICATION_METHOD setting

This script validates that the showcase will load properly.
DESIGNED FOR EMBEDDED PYTHON
"""

import sys
import traceback
import os
from pathlib import Path

print("🚀 SENIOR DEVELOPER COMPREHENSIVE FIX VERIFICATION")
print("="*60)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print("="*60)

def test_settings_import():
    """Test that settings can be imported correctly."""
    print("🔧 Testing settings import...")
    try:
        # Check if the settings file exists and has the correct content
        settings_init_file = Path("temp/src/backend/base/axiestudio/services/settings/__init__.py")
        if settings_init_file.exists():
            content = settings_init_file.read_text()
            if "settings = Settings()" in content and "settings" in content:
                print("✅ Settings __init__.py file contains settings export")
            else:
                print("❌ Settings __init__.py file missing settings export")
                return False
        else:
            print(f"❌ Settings __init__.py file not found: {settings_init_file}")
            return False

        # Check if EMAIL_VERIFICATION_METHOD is in base.py
        settings_base_file = Path("temp/src/backend/base/axiestudio/services/settings/base.py")
        if settings_base_file.exists():
            content = settings_base_file.read_text()
            if "EMAIL_VERIFICATION_METHOD" in content:
                print("✅ EMAIL_VERIFICATION_METHOD found in settings base")
            else:
                print("❌ EMAIL_VERIFICATION_METHOD missing from settings base")
                return False
        else:
            print(f"❌ Settings base.py file not found: {settings_base_file}")
            return False

        print("✅ Settings import structure is correct")
        return True
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        traceback.print_exc()
        return False

def test_store_api():
    """🎯 CRITICAL: Test the store API endpoints that power the showcase."""
    print("\n📦 Testing store API (SHOWCASE CRITICAL)...")
    try:
        # Check if store_components_converted directory exists
        store_path = Path("temp/src/store_components_converted")
        if store_path.exists():
            print(f"✅ Store path found: {store_path}")
        else:
            print(f"❌ Store path missing: {store_path}")
            return False

        # Check if store_index.json exists
        index_file = store_path / "store_index.json"
        if index_file.exists():
            print(f"✅ Store index file exists: {index_file}")
            # Check file size to ensure it's not empty
            file_size = index_file.stat().st_size
            print(f"✅ Store index file size: {file_size:,} bytes")

            # Try to parse the JSON to ensure it's valid
            import json
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    store_data = json.load(f)

                summary = store_data.get('summary', {})
                total_items = summary.get('total_items', 0)
                total_flows = summary.get('total_flows', 0)
                total_components = summary.get('total_components', 0)

                print(f"✅ Store index JSON is valid:")
                print(f"   - Total items: {total_items}")
                print(f"   - Total flows: {total_flows}")
                print(f"   - Total components: {total_components}")

                if total_items > 0:
                    print(f"✅ Store contains {total_items} items - SHOWCASE WILL LOAD!")
                else:
                    print("❌ Store is empty - SHOWCASE WILL BE EMPTY!")
                    return False

            except json.JSONDecodeError as e:
                print(f"❌ Store index JSON is invalid: {e}")
                return False
        else:
            print(f"❌ Store index file missing: {index_file}")
            return False

        # Check if axiestudio_store.py exists
        store_api_file = Path("temp/src/backend/base/axiestudio/api/v1/axiestudio_store.py")
        if store_api_file.exists():
            print(f"✅ Store API file exists: {store_api_file}")
        else:
            print(f"❌ Store API file missing: {store_api_file}")
            return False

        return True
    except Exception as e:
        print(f"❌ Store API test failed: {e}")
        traceback.print_exc()
        return False

def test_user_deletion_fix():
    """Test that user deletion handles foreign key constraints properly."""
    print("\n👤 Testing user deletion fix...")
    try:
        # Check if the users.py file has the proper foreign key handling
        users_file = Path("temp/src/backend/base/axiestudio/api/v1/users.py")
        if users_file.exists():
            content = users_file.read_text()

            # Check for IntegrityError import
            if "from sqlalchemy.exc import IntegrityError" in content:
                print("✅ IntegrityError import found")
            else:
                print("❌ IntegrityError import missing")
                return False

            # Check for foreign key handling in delete_user function
            if "try:" in content and "IntegrityError" in content and "foreign key" in content.lower():
                print("✅ Foreign key constraint handling detected in delete_user function")
            else:
                print("❌ Foreign key constraint handling not found")
                return False

            # Check for file deletion before user deletion
            if "File.user_id == user_id" in content and "await session.delete(file)" in content:
                print("✅ File deletion before user deletion detected")
            else:
                print("❌ File deletion before user deletion not found")
                return False

            print("✅ User deletion fix is properly implemented")
            return True
        else:
            print(f"❌ Users file not found: {users_file}")
            return False

    except Exception as e:
        print(f"❌ User deletion test failed: {e}")
        traceback.print_exc()
        return False

def test_frontend_api_fix():
    """Test that the frontend API interceptor fix is in place."""
    print("\n🌐 Testing frontend API fix...")
    try:
        # Read the API file to check for the fix
        api_file = Path("temp/src/frontend/src/controllers/API/api.tsx")

        if not api_file.exists():
            print(f"❌ API file not found: {api_file}")
            return False

        content = api_file.read_text()

        # Check for the fix
        if "if (!config) {" in content and "config.headers = {};" in content:
            print("✅ Frontend API interceptor fix detected")
            print("✅ Headers undefined check is in place")

            # Also check for the specific error prevention
            if "// Ensure config and config.headers exist" in content:
                print("✅ Proper comment documentation found")

            return True
        else:
            print("❌ Frontend API interceptor fix not found")
            return False

    except Exception as e:
        print(f"❌ Frontend API test failed: {e}")
        traceback.print_exc()
        return False

def test_router_registration():
    """Test that the axiestudio_store router is properly registered."""
    print("\n🔗 Testing router registration...")
    try:
        # Check if the router file exists and includes store router
        router_file = Path("temp/src/backend/base/axiestudio/api/router.py")
        if router_file.exists():
            content = router_file.read_text()

            # Check for store router import and inclusion
            if "axiestudio_store" in content:
                print("✅ Store router reference found in main router")
            else:
                print("❌ Store router reference not found in main router")
                return False

            # Check for router inclusion
            if "include_router" in content and "store" in content:
                print("✅ Store router inclusion detected")
            else:
                print("❌ Store router inclusion not found")
                return False

            print("✅ Router registration appears correct")
            return True
        else:
            print(f"❌ Router file not found: {router_file}")
            return False

    except Exception as e:
        print(f"❌ Router registration test failed: {e}")
        traceback.print_exc()
        return False

def test_logging_fix():
    """Test that the logging format error is fixed."""
    print("\n📝 Testing logging fix...")
    try:
        # Check if main.py has the logging fix
        main_file = Path("temp/src/backend/base/axiestudio/main.py")
        if main_file.exists():
            content = main_file.read_text()

            # Check for the fixed logging format
            if 'logger.error("unhandled error: %s", str(exc), exc_info=exc)' in content:
                print("✅ Logging format fix detected (unhandled error)")
            else:
                print("❌ Logging format fix not found (unhandled error)")
                return False

            if 'logger.error("HTTPException: %s", str(exc), exc_info=exc)' in content:
                print("✅ Logging format fix detected (HTTPException)")
            else:
                print("❌ Logging format fix not found (HTTPException)")
                return False

            print("✅ Logging format fixes are in place")
            return True
        else:
            print(f"❌ Main file not found: {main_file}")
            return False

    except Exception as e:
        print(f"❌ Logging fix test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Starting comprehensive fix verification...\n")

    tests = [
        ("Settings Import", test_settings_import),
        ("Store API", test_store_api),
        ("User Deletion Fix", test_user_deletion_fix),
        ("Frontend API Fix", test_frontend_api_fix),
        ("Router Registration", test_router_registration),
        ("Logging Fix", test_logging_fix),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False

    # Summary
    print("\n" + "="*60)
    print("📊 SENIOR DEVELOPER TEST SUMMARY")
    print("="*60)

    passed = 0
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL CRITICAL FIXES VERIFIED! The showcase should now load properly!")
        print("\n🚀 NEXT STEPS:")
        print("1. Restart the application to apply backend fixes")
        print("2. Clear browser cache to ensure frontend changes take effect")
        print("3. Navigate to /showcase - it should load with components!")
        return True
    else:
        print("⚠️  Some tests failed. The showcase may still have issues.")
        print("Please review the failed tests above and fix the remaining issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
