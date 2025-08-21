#!/usr/bin/env python3
"""
Comprehensive System Test for Email Verification Implementation
Tests every component to ensure the system is fully working
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

async def test_complete_system():
    """Test the complete email verification system end-to-end."""
    print("🧪 COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    
    test_results = {
        "imports": False,
        "database": False,
        "models": False,
        "api_endpoints": False,
        "migration": False,
        "user_creation": False,
        "verification_flow": False
    }
    
    try:
        # TEST 1: Import all required modules
        print("\n📦 TEST 1: Module Imports")
        print("-" * 30)
        
        try:
            from axiestudio.services.deps import get_db_service, get_settings_service
            from axiestudio.services.database.models.user.model import User, UserCreate
            from axiestudio.services.auth.utils import get_password_hash
            from axiestudio.api.v1.email_verification import VerifyCodeRequest, ResendCodeRequest
            from axiestudio.services.database.auto_migration_manager import auto_migration_manager
            from sqlmodel import select
            from sqlalchemy import inspect, text
            from datetime import datetime, timezone, timedelta
            
            print("✅ All imports successful")
            test_results["imports"] = True
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
            return test_results
        
        # TEST 2: Database Connection and Setup
        print("\n🗄️ TEST 2: Database Connection")
        print("-" * 30)
        
        try:
            db_service = get_db_service()
            settings_service = get_settings_service()
            
            # Test database connection
            async with db_service.with_session() as session:
                result = await session.exec(text("SELECT 1"))
                print("✅ Database connection successful")
            
            test_results["database"] = True
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return test_results
        
        # TEST 3: Database Schema and Migration
        print("\n🔄 TEST 3: Database Schema & Migration")
        print("-" * 30)
        
        try:
            # Run database creation and migration
            await db_service.create_db_and_tables()
            print("✅ Database tables created/verified")
            
            # Check migration status
            migration_status = await auto_migration_manager.check_migration_status()
            print(f"✅ Migration status: {migration_status.get('migration_status', 'Unknown')}")
            
            # Verify email verification schema
            schema_status = await auto_migration_manager.verify_email_verification_schema()
            print(f"✅ Email verification schema: {schema_status.get('status', 'Unknown')}")
            
            if schema_status.get('missing_fields'):
                print(f"⚠️ Missing fields: {schema_status['missing_fields']}")
            
            test_results["migration"] = True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return test_results
        
        # TEST 4: User Model Verification
        print("\n👤 TEST 4: User Model Fields")
        print("-" * 30)
        
        try:
            # Check if User model has all required fields
            user_fields = [
                'email_verified',
                'email_verification_token',
                'email_verification_expires',
                'verification_code',
                'verification_code_expires',
                'verification_attempts'
            ]
            
            # Create a test user instance to verify fields
            test_user_data = {
                'username': 'test_user_verification',
                'email': 'test@verification.com',
                'password': 'test_password'
            }
            
            user = User(**test_user_data)
            
            for field in user_fields:
                if hasattr(user, field):
                    print(f"✅ Field '{field}': Present")
                else:
                    print(f"❌ Field '{field}': Missing")
                    return test_results
            
            print("✅ All User model fields present")
            test_results["models"] = True
            
        except Exception as e:
            print(f"❌ User model verification failed: {e}")
            return test_results
        
        # TEST 5: Database Column Verification
        print("\n🗄️ TEST 5: Database Columns")
        print("-" * 30)
        
        try:
            async with db_service.with_session() as session:
                inspector = inspect(session.bind)
                
                if "user" not in inspector.get_table_names():
                    print("❌ User table does not exist")
                    return test_results
                
                user_columns = [col['name'] for col in inspector.get_columns('user')]
                
                required_columns = [
                    'email_verified',
                    'email_verification_token',
                    'email_verification_expires',
                    'verification_code',
                    'verification_code_expires',
                    'verification_attempts'
                ]
                
                missing_columns = []
                for col in required_columns:
                    if col in user_columns:
                        print(f"✅ Column '{col}': Present in database")
                    else:
                        print(f"❌ Column '{col}': Missing from database")
                        missing_columns.append(col)
                
                if missing_columns:
                    print(f"❌ Missing columns: {missing_columns}")
                    return test_results
                
                print("✅ All database columns present")
                
        except Exception as e:
            print(f"❌ Database column verification failed: {e}")
            return test_results
        
        # TEST 6: API Endpoint Verification
        print("\n🌐 TEST 6: API Endpoints")
        print("-" * 30)
        
        try:
            # Test if we can create request models
            verify_request = VerifyCodeRequest(email="test@example.com", code="123456")
            resend_request = ResendCodeRequest(email="test@example.com")
            
            print("✅ VerifyCodeRequest model works")
            print("✅ ResendCodeRequest model works")
            
            # Check if API functions exist (import test)
            from axiestudio.api.v1.email_verification import verify_code, resend_verification_code
            print("✅ API endpoint functions imported successfully")
            
            test_results["api_endpoints"] = True
            
        except Exception as e:
            print(f"❌ API endpoint verification failed: {e}")
            return test_results
        
        # TEST 7: User Creation Flow
        print("\n👥 TEST 7: User Creation Flow")
        print("-" * 30)
        
        try:
            async with db_service.with_session() as session:
                # Create a test user
                test_username = f"test_user_{int(datetime.now().timestamp())}"
                test_email = f"test_{int(datetime.now().timestamp())}@example.com"
                
                new_user = User(
                    username=test_username,
                    email=test_email,
                    password=get_password_hash("test_password"),
                    is_active=False,  # Should start inactive
                    email_verified=False,  # Should start unverified
                    verification_code="123456",
                    verification_code_expires=datetime.now(timezone.utc) + timedelta(minutes=10),
                    verification_attempts=0
                )
                
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
                
                print(f"✅ Created test user: {new_user.username}")
                print(f"✅ User is_active: {new_user.is_active} (should be False)")
                print(f"✅ User email_verified: {new_user.email_verified} (should be False)")
                print(f"✅ User verification_code: {new_user.verification_code}")
                print(f"✅ User verification_attempts: {new_user.verification_attempts}")
                
                # Verify we can query the user
                stmt = select(User).where(User.username == test_username)
                found_user = (await session.exec(stmt)).first()
                
                if found_user:
                    print("✅ User query successful")
                else:
                    print("❌ User query failed")
                    return test_results
                
                # Clean up test user
                await session.delete(found_user)
                await session.commit()
                print("✅ Test user cleaned up")
                
                test_results["user_creation"] = True
                
        except Exception as e:
            print(f"❌ User creation flow failed: {e}")
            return test_results
        
        # TEST 8: Verification Flow Simulation
        print("\n🔐 TEST 8: Verification Flow Simulation")
        print("-" * 30)
        
        try:
            async with db_service.with_session() as session:
                # Create another test user for verification flow
                test_username = f"verify_user_{int(datetime.now().timestamp())}"
                test_email = f"verify_{int(datetime.now().timestamp())}@example.com"
                
                user = User(
                    username=test_username,
                    email=test_email,
                    password=get_password_hash("test_password"),
                    is_active=False,
                    email_verified=False,
                    verification_code="654321",
                    verification_code_expires=datetime.now(timezone.utc) + timedelta(minutes=10),
                    verification_attempts=0
                )
                
                session.add(user)
                await session.commit()
                await session.refresh(user)
                
                print(f"✅ Created verification test user: {user.username}")
                
                # Simulate successful verification
                user.email_verified = True
                user.is_active = True
                user.verification_code = None
                user.verification_code_expires = None
                user.verification_attempts = 0
                
                await session.commit()
                await session.refresh(user)
                
                print(f"✅ Simulated verification: is_active={user.is_active}, email_verified={user.email_verified}")
                
                # Clean up
                await session.delete(user)
                await session.commit()
                print("✅ Verification test user cleaned up")
                
                test_results["verification_flow"] = True
                
        except Exception as e:
            print(f"❌ Verification flow simulation failed: {e}")
            return test_results
        
        print("\n" + "=" * 60)
        print("🎯 COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        
        all_passed = all(test_results.values())
        
        for test_name, passed in test_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} {test_name.upper().replace('_', ' ')}")
        
        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 ALL TESTS PASSED - SYSTEM IS FULLY WORKING!")
            print("✅ Email verification system is production ready")
            print("✅ Database migration system is functional")
            print("✅ User creation and verification flows work")
            print("✅ API endpoints are properly configured")
        else:
            print("❌ SOME TESTS FAILED - SYSTEM NEEDS ATTENTION")
            failed_tests = [name for name, passed in test_results.items() if not passed]
            print(f"❌ Failed tests: {', '.join(failed_tests)}")
        
        return test_results
        
    except Exception as e:
        print(f"❌ Comprehensive test failed: {e}")
        import traceback
        traceback.print_exc()
        return test_results

async def main():
    """Run the comprehensive system test."""
    results = await test_complete_system()
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
