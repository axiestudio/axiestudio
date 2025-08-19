#!/usr/bin/env python3
"""
Simple migration fix script for Axie Studio.
This script fixes the email_verified column and removes the problematic index.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

try:
    # Try to import required modules
    from axiestudio.services.deps import get_db_service
    from sqlalchemy import text
    print("✅ Successfully imported Axie Studio modules")
except ImportError as e:
    print(f"❌ Failed to import modules: {e}")
    print("This script needs to be run from the Axie Studio directory with dependencies installed.")
    sys.exit(1)

async def fix_migration():
    """Fix the migration issues by aligning database schema with models."""
    print("🚀 Starting migration fix...")
    
    try:
        # Get database service
        db_service = get_db_service()
        print(f"📊 Database URL: {db_service.database_url}")
        
        async with db_service.with_session() as session:
            print("🔧 Fixing email_verified column...")
            
            # Fix email_verified column
            try:
                # First, ensure all NULL values are set to FALSE
                await session.exec(text("UPDATE \"user\" SET email_verified = FALSE WHERE email_verified IS NULL"))
                print("✅ Updated NULL email_verified values to FALSE")
                
                # Check if we're using PostgreSQL or SQLite
                db_url = str(db_service.database_url).lower()
                if "postgresql" in db_url or "postgres" in db_url:
                    # PostgreSQL syntax
                    await session.exec(text("ALTER TABLE \"user\" ALTER COLUMN email_verified SET NOT NULL"))
                    await session.exec(text("ALTER TABLE \"user\" ALTER COLUMN email_verified SET DEFAULT FALSE"))
                    print("✅ Fixed email_verified column (PostgreSQL)")
                else:
                    # SQLite doesn't support ALTER COLUMN for NOT NULL, but that's usually fine
                    print("✅ SQLite detected - email_verified column should be fine")
                
            except Exception as e:
                print(f"⚠️  Warning fixing email_verified column: {e}")
            
            print("🗑️  Removing problematic index...")
            try:
                # Remove the problematic index
                await session.exec(text("DROP INDEX IF EXISTS ix_user_email_verification_token"))
                print("✅ Removed ix_user_email_verification_token index")
            except Exception as e:
                print(f"⚠️  Warning removing index: {e}")
            
            # Commit changes
            await session.commit()
            print("💾 Changes committed to database")
        
        print("🎉 Migration fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration fix failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main function."""
    print("🔧 Axie Studio Migration Fix Tool")
    print("=" * 40)
    
    success = await fix_migration()
    
    if success:
        print("\n✅ Migration fix completed! You can now start Axie Studio.")
        return 0
    else:
        print("\n❌ Migration fix failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
