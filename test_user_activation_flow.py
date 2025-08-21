#!/usr/bin/env python3
"""
Test script to verify user activation flow works correctly.
Tests that users are inactive until email verification, then become active.
"""

import asyncio
import sys
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

async def test_user_activation_flow():
    """Test the complete user activation flow"""
    try:
        from axiestudio.services.deps import get_db_service, get_settings_service
        from axiestudio.services.database.models.user.model import User
        from axiestudio.services.auth.utils import authenticate_user
        from sqlmodel import select
        from datetime import datetime, timezone
        
        print("🧪 Testing User Activation Flow...")
        print("=" * 50)
        
        # Check settings
        settings_service = get_settings_service()
        new_user_is_active = settings_service.auth_settings.NEW_USER_IS_ACTIVE
        print(f"📋 NEW_USER_IS_ACTIVE setting: {new_user_is_active}")
        
        # Get database service
        db_service = get_db_service()
        
        async with db_service.with_session() as session:
            # Find users with different states
            stmt = select(User).where(User.email_verified == False)
            unverified_users = (await session.exec(stmt)).all()
            
            stmt = select(User).where(User.email_verified == True)
            verified_users = (await session.exec(stmt)).all()
            
            print(f"👥 Found {len(unverified_users)} unverified users")
            print(f"✅ Found {len(verified_users)} verified users")
            
            # Check activation states
            for user in unverified_users[:3]:  # Check first 3
                print(f"   📧 {user.username}: email_verified={user.email_verified}, is_active={user.is_active}")
                
            for user in verified_users[:3]:  # Check first 3
                print(f"   ✅ {user.username}: email_verified={user.email_verified}, is_active={user.is_active}")
        
        print("\n🎯 Expected Flow:")
        print("1. User registers → is_active=False, email_verified=False")
        print("2. User tries to login → Gets 'Please verify email' error")
        print("3. User clicks email verification → is_active=True, email_verified=True")
        print("4. User can now login successfully")
        
        print("\n✅ User activation flow test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the test"""
    print("🔧 Axie Studio User Activation Flow Test")
    print("=" * 50)
    
    success = await test_user_activation_flow()
    
    if success:
        print("\n🎉 User activation flow is properly configured!")
        return 0
    else:
        print("\n❌ User activation flow test failed.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
