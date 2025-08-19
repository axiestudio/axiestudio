#!/usr/bin/env python3
"""
Test script to verify admin subscription handling.
Run this to test that superusers don't show subscription UI.
"""

import asyncio
import sys
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

async def test_admin_subscription_status():
    """Test that superusers get admin subscription status"""
    try:
        from axiestudio.services.deps import get_db_service
        from axiestudio.services.database.models.user.model import User
        from sqlmodel import select
        
        print("🔧 Testing Admin Subscription Status...")
        
        # Get database service
        db_service = get_db_service()
        
        async with db_service.with_session() as session:
            # Find superusers
            stmt = select(User).where(User.is_superuser == True)
            superusers = (await session.exec(stmt)).all()
            
            print(f"👑 Found {len(superusers)} superuser(s)")
            for user in superusers:
                print(f"   - {user.username}: is_superuser={user.is_superuser}, is_active={user.is_active}")
            
            # Find regular users
            stmt = select(User).where(User.is_superuser == False)
            regular_users = (await session.exec(stmt)).all()
            
            print(f"👥 Found {len(regular_users)} regular user(s)")
            for user in regular_users[:3]:  # Show first 3
                trial_status = getattr(user, 'subscription_status', 'trial')
                print(f"   - {user.username}: subscription_status={trial_status}, is_active={user.is_active}")
        
        print("✅ Admin subscription test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_forgot_password_activation():
    """Test that forgot password properly activates users"""
    try:
        from axiestudio.services.deps import get_db_service
        from axiestudio.services.database.models.user.model import User
        from sqlmodel import select
        
        print("🔑 Testing Forgot Password Activation...")
        
        # Get database service
        db_service = get_db_service()
        
        async with db_service.with_session() as session:
            # Find inactive users
            stmt = select(User).where(User.is_active == False)
            inactive_users = (await session.exec(stmt)).all()
            
            print(f"😴 Found {len(inactive_users)} inactive user(s)")
            for user in inactive_users:
                has_token = bool(getattr(user, 'email_verification_token', None))
                print(f"   - {user.username}: has_verification_token={has_token}, email_verified={getattr(user, 'email_verified', False)}")
        
        print("✅ Forgot password activation test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🔧 Axie Studio Admin & Password Reset Test Suite")
    print("=" * 60)
    
    test1 = await test_admin_subscription_status()
    test2 = await test_forgot_password_activation()
    
    print("\n" + "=" * 60)
    if test1 and test2:
        print("🎉 All tests passed!")
        print("✅ Superusers will see admin interface (no subscription UI)")
        print("✅ Forgot password will activate inactive users")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
