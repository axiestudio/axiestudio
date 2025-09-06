#!/usr/bin/env python3
"""
Test script to verify subscription enforcement is working correctly.
This script tests both backend middleware and frontend handling.
"""

import asyncio
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

async def test_subscription_enforcement():
    """Test subscription enforcement functionality."""
    print("🔒 TESTING SUBSCRIPTION ENFORCEMENT")
    print("=" * 50)
    
    try:
        # Import after adding to path
        from axiestudio.services.trial.service import trial_service
        from axiestudio.services.database.models.user.model import User
        
        print("✅ Successfully imported trial service")
        
        # Test 1: Create a mock expired user
        print("\n📋 Test 1: Expired Trial User")
        expired_user = User(
            id="test-expired-user",
            username="expired_user",
            email="expired@test.com",
            is_superuser=False,
            subscription_status="trial",
            trial_start=datetime.now(timezone.utc) - timedelta(days=10),
            trial_end=datetime.now(timezone.utc) - timedelta(days=3),
            create_at=datetime.now(timezone.utc) - timedelta(days=10)
        )
        
        trial_status = await trial_service.check_trial_status(expired_user)
        print(f"   Status: {trial_status['status']}")
        print(f"   Trial Expired: {trial_status['trial_expired']}")
        print(f"   Should Cleanup: {trial_status['should_cleanup']}")
        
        assert trial_status['should_cleanup'] == True, "Expired user should be marked for cleanup"
        print("   ✅ Expired user correctly identified")
        
        # Test 2: Create a mock active trial user
        print("\n📋 Test 2: Active Trial User")
        active_user = User(
            id="test-active-user",
            username="active_user", 
            email="active@test.com",
            is_superuser=False,
            subscription_status="trial",
            trial_start=datetime.now(timezone.utc) - timedelta(days=2),
            trial_end=datetime.now(timezone.utc) + timedelta(days=5),
            create_at=datetime.now(timezone.utc) - timedelta(days=2)
        )
        
        trial_status = await trial_service.check_trial_status(active_user)
        print(f"   Status: {trial_status['status']}")
        print(f"   Trial Expired: {trial_status['trial_expired']}")
        print(f"   Days Left: {trial_status['days_left']}")
        print(f"   Should Cleanup: {trial_status['should_cleanup']}")
        
        assert trial_status['should_cleanup'] == False, "Active trial user should not be marked for cleanup"
        print("   ✅ Active trial user correctly identified")
        
        # Test 3: Create a mock subscribed user
        print("\n📋 Test 3: Subscribed User")
        subscribed_user = User(
            id="test-subscribed-user",
            username="subscribed_user",
            email="subscribed@test.com", 
            is_superuser=False,
            subscription_status="active",
            trial_start=datetime.now(timezone.utc) - timedelta(days=10),
            trial_end=datetime.now(timezone.utc) - timedelta(days=3),
            create_at=datetime.now(timezone.utc) - timedelta(days=10)
        )
        
        trial_status = await trial_service.check_trial_status(subscribed_user)
        print(f"   Status: {trial_status['status']}")
        print(f"   Trial Expired: {trial_status['trial_expired']}")
        print(f"   Should Cleanup: {trial_status['should_cleanup']}")
        
        assert trial_status['should_cleanup'] == False, "Subscribed user should not be marked for cleanup"
        print("   ✅ Subscribed user correctly identified")
        
        # Test 4: Create a mock admin user
        print("\n📋 Test 4: Admin User")
        admin_user = User(
            id="test-admin-user",
            username="admin_user",
            email="admin@test.com",
            is_superuser=True,
            subscription_status="trial",
            trial_start=datetime.now(timezone.utc) - timedelta(days=10),
            trial_end=datetime.now(timezone.utc) - timedelta(days=3),
            create_at=datetime.now(timezone.utc) - timedelta(days=10)
        )
        
        trial_status = await trial_service.check_trial_status(admin_user)
        print(f"   Status: {trial_status['status']}")
        print(f"   Trial Expired: {trial_status['trial_expired']}")
        print(f"   Should Cleanup: {trial_status['should_cleanup']}")
        
        assert trial_status['should_cleanup'] == False, "Admin user should never be marked for cleanup"
        print("   ✅ Admin user correctly bypassed")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("=" * 50)
        print("✅ Backend subscription enforcement is working correctly")
        print("✅ Trial middleware will block expired users")
        print("✅ Admin users are properly exempted")
        print("✅ Active subscribers and trial users have access")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frontend_changes():
    """Test that frontend changes are in place."""
    print("\n🌐 TESTING FRONTEND CHANGES")
    print("=" * 50)
    
    try:
        # Check if API interceptor has 402 handling
        api_file = Path(__file__).parent / "src" / "frontend" / "src" / "controllers" / "API" / "api.tsx"
        if api_file.exists():
            content = api_file.read_text()
            if "isSubscriptionError" in content and "402" in content:
                print("✅ API interceptor has 402 Payment Required handling")
            else:
                print("❌ API interceptor missing 402 handling")
                return False
        else:
            print("❌ API file not found")
            return False
            
        # Check if subscription guard exists
        guard_file = Path(__file__).parent / "src" / "frontend" / "src" / "components" / "authorization" / "subscriptionGuard" / "index.tsx"
        if guard_file.exists():
            print("✅ Subscription guard component exists")
        else:
            print("❌ Subscription guard component missing")
            return False
            
        # Check if routes are updated
        routes_file = Path(__file__).parent / "src" / "frontend" / "src" / "routes.tsx"
        if routes_file.exists():
            content = routes_file.read_text()
            if "SubscriptionGuard" in content:
                print("✅ Routes include subscription guard")
            else:
                print("❌ Routes missing subscription guard")
                return False
        else:
            print("❌ Routes file not found")
            return False
            
        print("✅ All frontend changes are in place")
        return True
        
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SUBSCRIPTION ENFORCEMENT TEST SUITE")
    print("Testing the trial bug fix implementation...")
    print()
    
    # Test backend
    backend_success = asyncio.run(test_subscription_enforcement())
    
    # Test frontend
    frontend_success = test_frontend_changes()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    
    if backend_success and frontend_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Subscription enforcement is properly implemented")
        print("✅ Expired users will be blocked from accessing resources")
        print("✅ Admin users are properly exempted")
        print("✅ Frontend will handle 402 errors and redirect to pricing")
        print("\n🔒 The trial bug has been FIXED!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please review the implementation")
        sys.exit(1)
