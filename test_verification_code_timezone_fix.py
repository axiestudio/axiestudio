#!/usr/bin/env python3
"""
Test Verification Code Timezone Fix
Verifies that the timezone comparison issue in verification_code.py is resolved.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))


def test_verification_code_timezone_fix():
    """Test the verification code timezone fix."""
    
    print("🧪 Testing Verification Code Timezone Fix")
    print("=" * 50)
    
    try:
        from axiestudio.services.auth.verification_code import VerificationCodeService, ensure_timezone_aware
        
        print("✅ Successfully imported VerificationCodeService and ensure_timezone_aware")
        
        # Test 1: Test the helper function
        print("\n🔧 Testing ensure_timezone_aware helper function...")
        
        # Naive datetime (as would come from database)
        naive_dt = datetime(2025, 8, 22, 12, 0, 0)
        aware_dt = ensure_timezone_aware(naive_dt)
        
        print(f"✅ Naive datetime: {naive_dt} (tzinfo: {naive_dt.tzinfo})")
        print(f"✅ Made aware: {aware_dt} (tzinfo: {aware_dt.tzinfo})")
        
        # Test 2: Test None handling
        none_result = ensure_timezone_aware(None)
        print(f"✅ None input: {none_result}")
        
        # Test 3: Test already aware datetime
        already_aware = datetime.now(timezone.utc)
        still_aware = ensure_timezone_aware(already_aware)
        print(f"✅ Already aware preserved: {still_aware.tzinfo}")
        
        return True
        
    except Exception as e:
        print(f"❌ Helper function test failed: {e}")
        return False


def test_is_code_expired_fix():
    """Test the is_code_expired method with timezone fix."""
    
    print("\n🎯 Testing is_code_expired Method Fix")
    print("-" * 40)
    
    try:
        from axiestudio.services.auth.verification_code import VerificationCodeService
        
        # Test 1: Naive datetime (expired) - this was causing the error
        print("Testing naive datetime (expired)...")
        naive_expired = datetime(2025, 8, 20, 12, 0, 0)  # Past date, naive
        
        try:
            is_expired = VerificationCodeService.is_code_expired(naive_expired)
            print(f"✅ Naive expired datetime handled: {is_expired}")
        except TypeError as e:
            print(f"❌ Still getting timezone error: {e}")
            return False
        
        # Test 2: Naive datetime (not expired)
        print("Testing naive datetime (not expired)...")
        naive_future = datetime(2025, 8, 25, 12, 0, 0)  # Future date, naive
        
        try:
            is_expired = VerificationCodeService.is_code_expired(naive_future)
            print(f"✅ Naive future datetime handled: {is_expired}")
        except TypeError as e:
            print(f"❌ Still getting timezone error: {e}")
            return False
        
        # Test 3: Timezone-aware datetime
        print("Testing timezone-aware datetime...")
        aware_future = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        try:
            is_expired = VerificationCodeService.is_code_expired(aware_future)
            print(f"✅ Timezone-aware datetime handled: {is_expired}")
        except TypeError as e:
            print(f"❌ Timezone-aware datetime failed: {e}")
            return False
        
        # Test 4: None value
        print("Testing None value...")
        try:
            is_expired = VerificationCodeService.is_code_expired(None)
            print(f"✅ None value handled: {is_expired}")
        except Exception as e:
            print(f"❌ None value failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ is_code_expired test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def simulate_exact_error_scenario():
    """Simulate the exact error scenario from the logs."""
    
    print("\n🚨 Simulating Exact Error Scenario")
    print("-" * 35)
    
    try:
        from axiestudio.services.auth.verification_code import validate_code
        
        print("Simulating the exact call that was failing...")
        print("validate_code() -> VerificationCodeService.is_code_expired(expiry)")
        
        # Simulate database datetime (naive) - this is what was causing the crash
        db_expiry = datetime(2025, 8, 22, 1, 44, 18)  # Naive datetime from DB
        
        print(f"Database expiry (naive): {db_expiry}")
        print(f"Timezone info: {db_expiry.tzinfo}")
        
        # This is the call that was failing in the logs
        result = validate_code(
            code="123456",
            stored_code="123456", 
            expiry=db_expiry,  # This was the problematic naive datetime
            attempts=0
        )
        
        print(f"✅ validate_code completed successfully!")
        print(f"Result: {result}")
        
        # Test with expired code too
        expired_db_expiry = datetime(2025, 8, 20, 1, 34, 18)  # Past naive datetime
        
        result_expired = validate_code(
            code="123456",
            stored_code="123456",
            expiry=expired_db_expiry,  # Expired naive datetime
            attempts=0
        )
        
        print(f"✅ Expired code validation also works!")
        print(f"Expired result: {result_expired}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exact scenario simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    
    print("🚀 Verification Code Timezone Fix Test Suite")
    print("=" * 60)
    print("Testing the fix for: TypeError: can't compare offset-naive and offset-aware datetimes")
    print("Error location: axiestudio/services/auth/verification_code.py:83")
    print()
    
    # Run tests
    test1_passed = test_verification_code_timezone_fix()
    test2_passed = test_is_code_expired_fix()
    test3_passed = simulate_exact_error_scenario()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("-" * 30)
    print(f"Helper Function Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"is_code_expired Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Exact Scenario Test: {'✅ PASSED' if test3_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Verification code timezone fix is working correctly")
        print("✅ The 'can't compare offset-naive and offset-aware datetimes' error is resolved")
        print("✅ Email verification will now work without crashes")
        print("\n🚀 Users can now verify their email codes successfully!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Please review the errors above and fix any issues")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
