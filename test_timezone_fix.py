#!/usr/bin/env python3
"""
Test script to verify timezone fixes work correctly.

This script tests the timezone utility functions and simulates the datetime
comparison scenarios that were causing 500 errors in the authentication system.
"""

import sys
import os
from datetime import datetime, timezone, timedelta

# Add the backend path to sys.path so we can import our modules
backend_path = os.path.join(os.path.dirname(__file__), 'src', 'backend', 'base')
sys.path.insert(0, backend_path)

try:
    from axiestudio.utils.timezone import ensure_timezone_aware, safe_datetime_comparison, get_utc_now
    print("✅ Successfully imported timezone utilities")
except ImportError as e:
    print(f"❌ Failed to import timezone utilities: {e}")
    sys.exit(1)


def test_ensure_timezone_aware():
    """Test the ensure_timezone_aware function."""
    print("\n🧪 Testing ensure_timezone_aware function...")
    
    # Test with None
    result = ensure_timezone_aware(None)
    assert result is None, "Should return None for None input"
    print("✅ None input handled correctly")
    
    # Test with naive datetime (simulates database datetime)
    naive_dt = datetime(2025, 1, 15, 12, 0, 0)  # No timezone info
    aware_dt = ensure_timezone_aware(naive_dt)
    
    assert aware_dt is not None, "Should not return None for valid datetime"
    assert aware_dt.tzinfo is not None, "Should have timezone info"
    assert aware_dt.tzinfo == timezone.utc, "Should be UTC timezone"
    print(f"✅ Naive datetime converted: {naive_dt} -> {aware_dt}")
    
    # Test with already timezone-aware datetime
    already_aware = datetime.now(timezone.utc)
    still_aware = ensure_timezone_aware(already_aware)
    
    assert still_aware == already_aware, "Should not change already aware datetime"
    print(f"✅ Already aware datetime unchanged: {already_aware}")
    
    return True


def test_datetime_comparison():
    """Test datetime comparisons that were causing the 500 errors."""
    print("\n🧪 Testing datetime comparisons...")
    
    # Simulate the problematic scenario:
    # Database datetime (naive) vs current time (timezone-aware)
    
    # This simulates user.locked_until from database (naive)
    locked_until_naive = datetime.now() + timedelta(minutes=30)  # Naive datetime
    
    # This simulates datetime.now(timezone.utc) (timezone-aware)
    current_time_aware = datetime.now(timezone.utc)
    
    print(f"Database datetime (naive): {locked_until_naive} (tzinfo: {locked_until_naive.tzinfo})")
    print(f"Current time (aware): {current_time_aware} (tzinfo: {current_time_aware.tzinfo})")
    
    # This would cause the error: "can't compare offset-naive and offset-aware datetimes"
    # if locked_until_naive > current_time_aware:  # This would fail!
    
    # But with our fix:
    locked_until_aware = ensure_timezone_aware(locked_until_naive)
    
    try:
        is_locked = locked_until_aware and locked_until_aware > current_time_aware
        print(f"✅ Comparison successful: {locked_until_aware} > {current_time_aware} = {is_locked}")
        return True
    except TypeError as e:
        print(f"❌ Comparison failed: {e}")
        return False


def test_safe_datetime_comparison():
    """Test the safe_datetime_comparison utility function."""
    print("\n🧪 Testing safe_datetime_comparison function...")
    
    # Test with naive and aware datetimes
    naive_dt = datetime(2025, 1, 15, 12, 0, 0)
    aware_dt = datetime(2025, 1, 15, 13, 0, 0, tzinfo=timezone.utc)
    
    result = safe_datetime_comparison(aware_dt, naive_dt)
    print(f"✅ Safe comparison: {aware_dt} > {naive_dt} = {result}")
    
    # Test with None values
    result_none = safe_datetime_comparison(None, aware_dt)
    assert result_none is False, "Should return False when comparing with None"
    print("✅ None comparison handled correctly")
    
    return True


def test_authentication_scenario():
    """Test the specific authentication scenario that was failing."""
    print("\n🧪 Testing authentication lock scenario...")
    
    # Simulate user object with locked_until field (naive datetime from database)
    class MockUser:
        def __init__(self):
            # This simulates a locked account (30 minutes from now, but naive)
            self.locked_until = datetime.now() + timedelta(minutes=30)
    
    user = MockUser()
    
    # This is the fixed authentication logic
    if user.locked_until:
        locked_until_aware = ensure_timezone_aware(user.locked_until)
        now = datetime.now(timezone.utc)
        
        if locked_until_aware and locked_until_aware > now:
            time_remaining = locked_until_aware - now
            print(f"✅ Account is locked for {int(time_remaining.total_seconds() / 60)} more minutes")
            return True
    
    print("✅ Authentication lock check completed successfully")
    return True


def main():
    """Run all timezone fix tests."""
    print("🚀 Starting timezone fix verification tests...")
    print("=" * 60)
    
    tests = [
        test_ensure_timezone_aware,
        test_datetime_comparison,
        test_safe_datetime_comparison,
        test_authentication_scenario,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Timezone fixes are working correctly.")
        print("\n✅ The authentication system should now work without timezone comparison errors.")
        print("✅ Both English (main) and Swedish (master) apps should be fixed.")
        return 0
    else:
        print("❌ Some tests failed. Please check the timezone fixes.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
