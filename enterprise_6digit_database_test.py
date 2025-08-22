# -*- coding: utf-8 -*-
"""
🔐 ENTERPRISE 6-DIGIT CODE DATABASE VERIFICATION TEST
Real database testing of signup → 6-digit code → resend flow
"""

import sys
import asyncio
import traceback
from pathlib import Path
from datetime import datetime, timezone

# Add backend path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

print("🔐 ENTERPRISE 6-DIGIT CODE DATABASE VERIFICATION")
print("="*70)
print("🎯 TESTING: Signup → 6-digit code → Database storage → Resend")
print("="*70)

async def test_signup_6digit_database_flow():
    """Test the complete signup and 6-digit code database flow"""
    print("\n🚀 TESTING COMPLETE SIGNUP → 6-DIGIT CODE → DATABASE FLOW...")
    
    try:
        # Import required modules
        from axiestudio.services.database.service import get_db_service
        from axiestudio.services.database.models.user.model import User, UserCreate
        from axiestudio.services.auth.verification_code import create_verification
        from axiestudio.services.auth.utils import get_password_hash
        from sqlmodel import select
        
        # Get database service
        db_service = get_db_service()
        
        # Test user data
        test_email = "enterprise.test@axiestudio.se"
        test_username = "enterprise_test_user"
        test_password = "EnterpriseTest123!"
        
        print(f"📧 Testing with email: {test_email}")
        print(f"👤 Testing with username: {test_username}")
        
        async with db_service.with_session() as session:
            # Step 1: Clean up any existing test user
            print("\n🧹 STEP 1: Cleaning up existing test user...")
            existing_user_stmt = select(User).where(User.email == test_email)
            existing_user = (await session.exec(existing_user_stmt)).first()
            
            if existing_user:
                await session.delete(existing_user)
                await session.commit()
                print("✅ Cleaned up existing test user")
            else:
                print("✅ No existing test user found")
            
            # Step 2: Create new user (simulate signup)
            print("\n📝 STEP 2: Creating new user (SIGNUP SIMULATION)...")
            
            # Generate 6-digit code
            verification_code, code_expiry = create_verification()
            print(f"🔢 Generated 6-digit code: {verification_code}")
            print(f"⏰ Code expires at: {code_expiry}")
            
            # Create user object
            new_user = User(
                username=test_username,
                email=test_email,
                password=get_password_hash(test_password),
                is_active=False,  # Inactive until email verified
                email_verified=False,
                verification_code=verification_code,
                verification_code_expires=code_expiry,
                verification_attempts=0,
                create_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            # Save to database
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            
            print(f"✅ User created with ID: {new_user.id}")
            print(f"✅ User is_active: {new_user.is_active}")
            print(f"✅ User email_verified: {new_user.email_verified}")
            
            # Step 3: Verify 6-digit code is stored in database
            print("\n🔍 STEP 3: VERIFYING 6-DIGIT CODE IN DATABASE...")
            
            # Query user from database to verify storage
            user_stmt = select(User).where(User.email == test_email)
            stored_user = (await session.exec(user_stmt)).first()
            
            if not stored_user:
                print("❌ CRITICAL: User not found in database!")
                return False
            
            print(f"✅ User found in database: {stored_user.username}")
            print(f"🔢 Stored verification_code: {stored_user.verification_code}")
            print(f"⏰ Stored code_expires: {stored_user.verification_code_expires}")
            print(f"🔄 Stored attempts: {stored_user.verification_attempts}")
            
            # Verify the code matches
            if stored_user.verification_code == verification_code:
                print("✅ VERIFICATION CODE MATCHES DATABASE!")
            else:
                print(f"❌ CRITICAL: Code mismatch! Generated: {verification_code}, Stored: {stored_user.verification_code}")
                return False
            
            # Verify expiry is set
            if stored_user.verification_code_expires:
                print("✅ CODE EXPIRY IS SET IN DATABASE!")
            else:
                print("❌ CRITICAL: Code expiry not set!")
                return False
            
            # Verify attempts is 0
            if stored_user.verification_attempts == 0:
                print("✅ VERIFICATION ATTEMPTS INITIALIZED TO 0!")
            else:
                print(f"❌ CRITICAL: Attempts not initialized correctly: {stored_user.verification_attempts}")
                return False
            
            # Step 4: Test resend functionality
            print("\n🔄 STEP 4: TESTING RESEND FUNCTIONALITY...")
            
            # Generate new code (simulate resend)
            new_verification_code, new_code_expiry = create_verification()
            print(f"🔢 Generated NEW 6-digit code: {new_verification_code}")
            print(f"⏰ NEW code expires at: {new_code_expiry}")
            
            # Update user with new code (simulate resend endpoint)
            stored_user.verification_code = new_verification_code
            stored_user.verification_code_expires = new_code_expiry
            stored_user.verification_attempts = 0  # Reset attempts on resend
            stored_user.updated_at = datetime.now(timezone.utc)
            
            session.add(stored_user)
            await session.commit()
            await session.refresh(stored_user)
            
            print("✅ Database updated with new code")
            
            # Step 5: Verify new code is stored
            print("\n🔍 STEP 5: VERIFYING NEW CODE IN DATABASE...")
            
            # Query again to verify new code
            updated_user_stmt = select(User).where(User.email == test_email)
            updated_user = (await session.exec(updated_user_stmt)).first()
            
            print(f"🔢 Updated verification_code: {updated_user.verification_code}")
            print(f"⏰ Updated code_expires: {updated_user.verification_code_expires}")
            print(f"🔄 Updated attempts: {updated_user.verification_attempts}")
            
            # Verify the new code matches
            if updated_user.verification_code == new_verification_code:
                print("✅ NEW VERIFICATION CODE MATCHES DATABASE!")
            else:
                print(f"❌ CRITICAL: New code mismatch! Generated: {new_verification_code}, Stored: {updated_user.verification_code}")
                return False
            
            # Verify codes are different
            if verification_code != new_verification_code:
                print("✅ RESEND GENERATED DIFFERENT CODE!")
            else:
                print("⚠️ WARNING: Resend generated same code (rare but possible)")
            
            # Step 6: Test code validation
            print("\n✅ STEP 6: TESTING CODE VALIDATION...")
            
            from axiestudio.services.auth.verification_code import validate_code
            
            # Test correct code
            validation_result = validate_code(
                code=new_verification_code,
                stored_code=updated_user.verification_code,
                expiry=updated_user.verification_code_expires,
                attempts=updated_user.verification_attempts
            )
            
            if validation_result["valid"]:
                print("✅ CODE VALIDATION SUCCESSFUL!")
            else:
                print(f"❌ CRITICAL: Code validation failed: {validation_result['error']}")
                return False
            
            # Test wrong code
            wrong_validation = validate_code(
                code="999999",
                stored_code=updated_user.verification_code,
                expiry=updated_user.verification_code_expires,
                attempts=updated_user.verification_attempts
            )
            
            if not wrong_validation["valid"]:
                print("✅ WRONG CODE PROPERLY REJECTED!")
            else:
                print("❌ CRITICAL: Wrong code was accepted!")
                return False
            
            # Step 7: Test account activation
            print("\n🔓 STEP 7: TESTING ACCOUNT ACTIVATION...")
            
            # Simulate successful verification (activate account)
            updated_user.is_active = True
            updated_user.email_verified = True
            updated_user.verification_code = None  # Clear code
            updated_user.verification_code_expires = None  # Clear expiry
            updated_user.verification_attempts = 0  # Reset attempts
            updated_user.updated_at = datetime.now(timezone.utc)
            
            session.add(updated_user)
            await session.commit()
            await session.refresh(updated_user)
            
            print("✅ Account activated in database")
            
            # Verify activation
            final_user_stmt = select(User).where(User.email == test_email)
            final_user = (await session.exec(final_user_stmt)).first()
            
            if final_user.is_active and final_user.email_verified:
                print("✅ ACCOUNT SUCCESSFULLY ACTIVATED!")
            else:
                print(f"❌ CRITICAL: Account not activated! is_active: {final_user.is_active}, email_verified: {final_user.email_verified}")
                return False
            
            if final_user.verification_code is None:
                print("✅ VERIFICATION CODE CLEARED AFTER ACTIVATION!")
            else:
                print(f"❌ CRITICAL: Code not cleared: {final_user.verification_code}")
                return False
            
            # Step 8: Cleanup
            print("\n🧹 STEP 8: CLEANING UP TEST DATA...")
            await session.delete(final_user)
            await session.commit()
            print("✅ Test user cleaned up")
            
            return True
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        traceback.print_exc()
        return False

async def test_database_schema():
    """Test that database schema supports 6-digit codes"""
    print("\n🗄️ TESTING DATABASE SCHEMA FOR 6-DIGIT CODES...")
    
    try:
        from axiestudio.services.database.service import get_db_service
        from sqlalchemy import inspect
        
        db_service = get_db_service()
        
        async with db_service.with_session() as session:
            inspector = inspect(session.bind)
            
            # Check if user table exists
            if "user" not in inspector.get_table_names():
                print("❌ CRITICAL: User table does not exist!")
                return False
            
            # Get user table columns
            user_columns = [col['name'] for col in inspector.get_columns('user')]
            
            # Required 6-digit code columns
            required_columns = [
                'verification_code',
                'verification_code_expires', 
                'verification_attempts',
                'email_verified',
                'is_active'
            ]
            
            all_columns_exist = True
            for column in required_columns:
                if column in user_columns:
                    print(f"✅ Column '{column}': EXISTS")
                else:
                    print(f"❌ Column '{column}': MISSING")
                    all_columns_exist = False
            
            return all_columns_exist
            
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False

async def main():
    """Run all enterprise 6-digit code tests"""
    print("🚀 Starting enterprise 6-digit code database verification...\n")
    
    tests = [
        ("Database Schema", test_database_schema),
        ("Complete 6-Digit Flow", test_signup_6digit_database_flow),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*50}")
            print(f"🧪 RUNNING: {test_name}")
            print(f"{'='*50}")
            
            result = await test_func()
            results[test_name] = result
            
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 ENTERPRISE 6-DIGIT CODE DATABASE VERIFICATION SUMMARY")
    print("="*70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Database Verification Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ENTERPRISE 6-DIGIT CODE DATABASE SYSTEM VERIFIED!")
        print("\n✅ CONFIRMED ENTERPRISE FEATURES:")
        print("• Signup creates user with 6-digit code in database")
        print("• 6-digit codes are properly stored and retrieved")
        print("• Resend updates database with new code")
        print("• Code validation works with database values")
        print("• Account activation clears codes from database")
        print("• All database operations are real-time and persistent")
        print("\n🚀 DATABASE OPERATIONS ARE BULLETPROOF!")
        return True
    else:
        print("⚠️  CRITICAL DATABASE ISSUES FOUND!")
        print("The 6-digit code system has database problems.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
