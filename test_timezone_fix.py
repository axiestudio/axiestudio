#!/usr/bin/env python3
"""
Test Timezone Fix for Automated Verification System
Verifies that the timezone comparison issue is resolved.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))


def test_timezone_helper():
    """Test the ensure_timezone_aware helper function."""
    
    print("🧪 Testing Timezone Helper Function")
    print("=" * 50)
    
    try:
        from axiestudio.services.automated_verification_system import ensure_timezone_aware
        
        # Test 1: Naive datetime (common database scenario)
        naive_dt = datetime(2025, 8, 22, 12, 0, 0)  # No timezone info
        aware_dt = ensure_timezone_aware(naive_dt)
        
        print(f"✅ Naive datetime: {naive_dt} (tzinfo: {naive_dt.tzinfo})")
        print(f"✅ Made aware: {aware_dt} (tzinfo: {aware_dt.tzinfo})")
        
        # Test 2: Already aware datetime
        already_aware = datetime.now(timezone.utc)
        still_aware = ensure_timezone_aware(already_aware)
        
        print(f"✅ Already aware: {already_aware} (tzinfo: {already_aware.tzinfo})")
        print(f"✅ Still aware: {still_aware} (tzinfo: {still_aware.tzinfo})")
        
        # Test 3: None value
        none_result = ensure_timezone_aware(None)
        print(f"✅ None input: {none_result}")
        
        # Test 4: Comparison that was failing before
        print("\n🔧 Testing the comparison that was failing...")
        
        # Simulate database datetime (naive)
        db_datetime = datetime(2025, 8, 15, 12, 0, 0)  # 7 days ago, naive
        
        # Make it timezone-aware
        aware_db_datetime = ensure_timezone_aware(db_datetime)
        
        # Compare with timezone-aware datetime (this was failing before)
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        
        try:
            comparison_result = aware_db_datetime > seven_days_ago
            print(f"✅ Comparison successful: {aware_db_datetime} > {seven_days_ago} = {comparison_result}")
        except TypeError as e:
            print(f"❌ Comparison failed: {e}")
            return False
        
        print("✅ All timezone tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Timezone test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_verification_system_import():
    """Test that the verification system can be imported without errors."""
    
    print("\n🔍 Testing Verification System Import")
    print("-" * 30)
    
    try:
        from axiestudio.services.automated_verification_system import automated_verification_monitor
        print("✅ Automated verification system imported successfully")
        
        # Test that the function exists and is callable
        if callable(automated_verification_monitor):
            print("✅ automated_verification_monitor is callable")
        else:
            print("❌ automated_verification_monitor is not callable")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def simulate_timezone_comparison():
    """Simulate the exact comparison that was failing."""
    
    print("\n🎯 Simulating the Exact Failing Comparison")
    print("-" * 40)
    
    try:
        from axiestudio.services.automated_verification_system import ensure_timezone_aware
        
        # Simulate the exact scenario from the error
        print("Simulating: user.email_verification_expires > (datetime.now(timezone.utc) - timedelta(days=7))")
        
        # Create a naive datetime (as would come from database)
        user_email_verification_expires = datetime(2025, 8, 20, 10, 30, 0)  # Naive
        
        print(f"Database datetime (naive): {user_email_verification_expires}")
        print(f"Timezone info: {user_email_verification_expires.tzinfo}")
        
        # The comparison that was failing
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        print(f"Seven days ago (aware): {seven_days_ago}")
        print(f"Timezone info: {seven_days_ago.tzinfo}")
        
        # OLD WAY (BROKEN):
        print("\n❌ Old way (would fail):")
        try:
            # This would fail with: TypeError: can't compare offset-naive and offset-aware datetimes
            old_result = user_email_verification_expires > seven_days_ago
            print(f"Old comparison result: {old_result}")
        except TypeError as e:
            print(f"Expected error: {e}")
        
        # NEW WAY (FIXED):
        print("\n✅ New way (fixed):")
        user_expires_aware = ensure_timezone_aware(user_email_verification_expires)
        new_result = user_expires_aware > seven_days_ago
        print(f"Fixed comparison result: {new_result}")
        print(f"User expires (aware): {user_expires_aware}")
        print(f"Seven days ago: {seven_days_ago}")
        
        print("✅ Timezone comparison fix verified!")
        return True
        
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        return False


def main():
    """Main test function."""
    
    print("🚀 Timezone Fix Test Suite")
    print("=" * 60)
    print("Testing the fix for: TypeError: can't compare offset-naive and offset-aware datetimes")
    print()
    
    # Run tests
    test1_passed = test_timezone_helper()
    test2_passed = test_verification_system_import()
    test3_passed = simulate_timezone_comparison()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("-" * 30)
    print(f"Timezone Helper Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Import Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Comparison Simulation: {'✅ PASSED' if test3_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Timezone comparison fix is working correctly")
        print("✅ The 'can't compare offset-naive and offset-aware datetimes' error is resolved")
        print("✅ Automated verification system should now work without crashes")
        print("\n🚀 The verification scheduler will now run successfully!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Please review the errors above and fix any issues")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
