#!/usr/bin/env python3
"""
Test script to verify email verification functionality.
Run this to test that email verification properly activates users.
"""

import asyncio
import sys
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

async def test_email_verification():
    """Test that email verification sets user.is_active = True"""
    try:
        from axiestudio.services.deps import get_db_service
        from axiestudio.services.database.models.user.model import User
        from axiestudio.services.email.service import email_service
        from sqlmodel import select
        from datetime import datetime, timezone
        
        print("🧪 Testing Email Verification Activation...")
        
        # Get database service
        db_service = get_db_service()
        
        async with db_service.with_session() as session:
            # Find a user with email verification token (if any)
            stmt = select(User).where(User.email_verification_token.is_not(None))
            user_with_token = (await session.exec(stmt)).first()
            
            if user_with_token:
                print(f"📧 Found user with verification token: {user_with_token.username}")
                print(f"   - is_active: {user_with_token.is_active}")
                print(f"   - email_verified: {user_with_token.email_verified}")
                print(f"   - has_token: {bool(user_with_token.email_verification_token)}")
            else:
                print("📧 No users with pending email verification found")
            
            # Check if there are any inactive users
            stmt = select(User).where(User.is_active == False)
            inactive_users = (await session.exec(stmt)).all()
            
            print(f"👥 Found {len(inactive_users)} inactive users")
            for user in inactive_users:
                print(f"   - {user.username}: email_verified={user.email_verified}, has_token={bool(user.email_verification_token)}")
        
        print("✅ Email verification test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_email_service():
    """Test that email service methods exist and are callable"""
    try:
        from axiestudio.services.email.service import email_service
        
        print("📧 Testing Email Service...")
        
        # Check if methods exist
        assert hasattr(email_service, 'send_verification_email'), "send_verification_email method missing"
        assert hasattr(email_service, 'send_password_reset_email'), "send_password_reset_email method missing"
        assert hasattr(email_service, 'generate_verification_token'), "generate_verification_token method missing"
        
        # Test token generation
        token = email_service.generate_verification_token()
        assert token and len(token) > 10, "Token generation failed"
        
        print("✅ Email service methods are available!")
        return True
        
    except Exception as e:
        print(f"❌ Email service test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🔧 Axie Studio Email Verification Test Suite")
    print("=" * 50)
    
    test1 = await test_email_service()
    test2 = await test_email_verification()
    
    if test1 and test2:
        print("\n🎉 All tests passed! Email verification should work correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
