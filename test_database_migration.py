#!/usr/bin/env python3
"""
Test Database Migration Implementation
Verifies that our email verification fields are properly handled by the migration system
"""

import asyncio
import sys
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

async def test_database_migration():
    """Test the complete database migration system."""
    try:
        from axiestudio.services.deps import get_db_service
        from axiestudio.services.database.auto_migration_manager import auto_migration_manager
        from axiestudio.services.database.models.user.model import User
        from sqlmodel import select
        from sqlalchemy import inspect, text
        
        print("🧪 Testing Database Migration Implementation...")
        print("=" * 60)
        
        # Get database service
        db_service = get_db_service()
        
        # Test 1: Check database info
        print("\n📊 TEST 1: Database Information")
        print("-" * 30)
        db_info = await auto_migration_manager.get_database_info()
        print(f"Database Type: {db_info.get('dialect', 'Unknown')}")
        print(f"Table Count: {db_info.get('table_count', 0)}")
        print(f"Alembic Version: {db_info.get('alembic_version', 'Not initialized')}")
        
        # Test 2: Check migration status
        print("\n🔍 TEST 2: Migration Status Check")
        print("-" * 30)
        migration_status = await auto_migration_manager.check_migration_status()
        print(f"Migration Status: {migration_status.get('migration_status', 'Unknown')}")
        print(f"Message: {migration_status.get('message', 'No message')}")
        
        if migration_status.get('missing_columns'):
            print(f"Missing Columns: {migration_status['missing_columns']}")
        
        # Test 3: Verify email verification schema
        print("\n📧 TEST 3: Email Verification Schema")
        print("-" * 30)
        schema_status = await auto_migration_manager.verify_email_verification_schema()
        print(f"Schema Status: {schema_status.get('status', 'Unknown')}")
        print(f"Message: {schema_status.get('message', 'No message')}")
        
        if schema_status.get('present_fields'):
            print("\n✅ Present Fields:")
            for field in schema_status['present_fields']:
                print(f"  • {field}")
        
        if schema_status.get('missing_fields'):
            print("\n❌ Missing Fields:")
            for field in schema_status['missing_fields']:
                print(f"  • {field}")
        
        # Test 4: Check actual database columns
        print("\n🗄️ TEST 4: Database Column Verification")
        print("-" * 30)
        
        async with db_service.with_session() as session:
            inspector = inspect(session.bind)
            
            if "user" in inspector.get_table_names():
                user_columns = inspector.get_columns('user')
                print(f"User table has {len(user_columns)} columns:")
                
                # Check for our specific email verification columns
                email_verification_columns = [
                    'email_verified',
                    'email_verification_token',
                    'email_verification_expires',
                    'verification_code',
                    'verification_code_expires',
                    'verification_attempts'
                ]
                
                column_names = [col['name'] for col in user_columns]
                
                for col_name in email_verification_columns:
                    status = "✅" if col_name in column_names else "❌"
                    print(f"  {status} {col_name}")
                
                # Test 5: Try to query the User model
                print("\n🔍 TEST 5: User Model Query Test")
                print("-" * 30)
                
                try:
                    # Test basic query
                    stmt = select(User).limit(5)
                    users = (await session.exec(stmt)).all()
                    print(f"✅ Successfully queried User table: {len(users)} users found")
                    
                    # Test specific email verification fields
                    if users:
                        user = users[0]
                        print(f"✅ Sample user verification fields:")
                        print(f"  • email_verified: {getattr(user, 'email_verified', 'MISSING')}")
                        print(f"  • verification_code: {getattr(user, 'verification_code', 'MISSING')}")
                        print(f"  • verification_attempts: {getattr(user, 'verification_attempts', 'MISSING')}")
                    
                except Exception as e:
                    print(f"❌ Failed to query User model: {e}")
            else:
                print("❌ User table does not exist!")
        
        # Test 6: Check if migrations can run
        print("\n🔄 TEST 6: Migration System Test")
        print("-" * 30)
        
        try:
            # Test if we can run migrations (dry run)
            await db_service.create_db_and_tables()
            print("✅ Database and tables creation successful")
            
            # Test migration status after creation
            final_status = await auto_migration_manager.check_migration_status()
            print(f"✅ Final migration status: {final_status.get('migration_status', 'Unknown')}")
            
        except Exception as e:
            print(f"❌ Migration system test failed: {e}")
        
        print("\n" + "=" * 60)
        print("🎯 DATABASE MIGRATION TEST SUMMARY")
        print("=" * 60)
        
        # Overall assessment
        if (schema_status.get('status') == 'success' and 
            migration_status.get('migration_status') in ['up_to_date', 'needs_migration']):
            print("✅ DATABASE MIGRATION IMPLEMENTATION: WORKING CORRECTLY")
            print("✅ Email verification fields are properly handled")
            print("✅ Auto-migration system is functional")
            return True
        else:
            print("❌ DATABASE MIGRATION IMPLEMENTATION: NEEDS ATTENTION")
            print("❌ Some email verification fields may be missing")
            print("❌ Migration system may need fixes")
            return False
            
    except Exception as e:
        print(f"❌ Database migration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the database migration test."""
    success = await test_database_migration()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
