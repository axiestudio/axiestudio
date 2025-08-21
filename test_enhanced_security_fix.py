#!/usr/bin/env python3
"""
Test Enhanced Security Fix
Verifies that the enhanced security columns are properly added to the database
"""

import asyncio
import sys
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

async def test_enhanced_security_fix():
    """Test if enhanced security columns are properly added."""
    
    print("🔐 Testing Enhanced Security Fix")
    print("=" * 50)
    
    try:
        from axiestudio.services.startup.enhanced_security_setup import initialize_enhanced_security
        
        print("✅ Enhanced security module imported successfully")
        
        # Run the enhanced security setup
        print("🚀 Running enhanced security initialization...")
        success = await initialize_enhanced_security()
        
        if success:
            print("✅ Enhanced security initialization completed successfully!")
            print("🎉 The app should now start without database migration errors!")
            return True
        else:
            print("❌ Enhanced security initialization failed!")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def verify_columns_exist():
    """Verify that the enhanced security columns exist in the database."""
    
    print("\n🔍 Verifying Enhanced Security Columns")
    print("-" * 40)
    
    try:
        from axiestudio.services.deps import get_db_service
        from sqlalchemy import text
        
        db_service = get_db_service()
        
        async with db_service.with_session() as session:
            # Check if we're using SQLite or PostgreSQL
            db_url = str(db_service.database_url).lower()
            is_sqlite = "sqlite" in db_url
            
            print(f"📊 Database type: {'SQLite' if is_sqlite else 'PostgreSQL'}")
            
            # Get existing columns
            if is_sqlite:
                result = await session.exec(text("PRAGMA table_info(user)"))
                existing_columns = [row[1] for row in result.fetchall()]
            else:
                result = await session.exec(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'user' AND table_schema = 'public'
                """))
                existing_columns = [row[0] for row in result.fetchall()]
            
            print(f"📋 Total columns in user table: {len(existing_columns)}")
            
            # Check required enhanced security columns
            required_columns = [
                "login_attempts",
                "locked_until", 
                "last_login_ip",
                "password_changed_at",
                "failed_login_attempts",
                "last_failed_login"
            ]
            
            print("\n🔐 Enhanced Security Columns Status:")
            all_exist = True
            for column in required_columns:
                if column in existing_columns:
                    print(f"  ✅ {column}: EXISTS")
                else:
                    print(f"  ❌ {column}: MISSING")
                    all_exist = False
            
            if all_exist:
                print("\n🎉 All enhanced security columns exist!")
                print("✅ Database migration issue should be resolved!")
                return True
            else:
                print("\n⚠️ Some enhanced security columns are missing!")
                return False
                
    except Exception as e:
        print(f"❌ Error verifying columns: {e}")
        return False


async def main():
    """Main test function."""
    
    print("🧪 ENHANCED SECURITY FIX TEST")
    print("=" * 60)
    print("This test will verify that the enhanced security columns")
    print("are properly added to the database to fix the startup issue.")
    print()
    
    # Step 1: Test enhanced security setup
    setup_success = await test_enhanced_security_fix()
    
    if not setup_success:
        print("\n❌ Enhanced security setup failed!")
        return 1
    
    # Step 2: Verify columns exist
    verify_success = await verify_columns_exist()
    
    if not verify_success:
        print("\n❌ Column verification failed!")
        return 1
    
    print("\n" + "=" * 60)
    print("🎉 ENHANCED SECURITY FIX TEST PASSED!")
    print("=" * 60)
    print("✅ All enhanced security columns are properly configured")
    print("✅ Database migration errors should be resolved")
    print("✅ The app should now start successfully!")
    print("\n🚀 You can now restart AxieStudio!")
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
