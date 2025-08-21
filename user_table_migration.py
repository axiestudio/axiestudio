#!/usr/bin/env python3
"""
Simple User Table Migration Script
Runs the exact SQL commands you specified for user table updates
"""

import asyncio
import sys
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

from axiestudio.services.deps import get_db_service
from sqlalchemy import text
from loguru import logger

# Your exact SQL commands
MIGRATION_COMMANDS = [
    {
        "step": 1,
        "description": "Add Email Column",
        "sql": 'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email VARCHAR;'
    },
    {
        "step": 2,
        "description": "Add Stripe Customer ID",
        "sql": 'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR;'
    },
    {
        "step": 3,
        "description": "Add Subscription Status (with default)",
        "sql": "ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS subscription_status VARCHAR DEFAULT 'trial';"
    },
    {
        "step": 4,
        "description": "Add Subscription ID",
        "sql": 'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_id VARCHAR;'
    },
    {
        "step": 5,
        "description": "Add Trial Start Date",
        "sql": 'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS trial_start TIMESTAMP;'
    },
    {
        "step": 6,
        "description": "Add Trial End Date",
        "sql": 'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS trial_end TIMESTAMP;'
    },
    {
        "step": 7,
        "description": "Add Subscription Start Date",
        "sql": 'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_start TIMESTAMP;'
    },
    {
        "step": 8,
        "description": "Add Subscription End Date",
        "sql": 'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_end TIMESTAMP;'
    },
    {
        "step": 9,
        "description": "Create Email Index for Performance",
        "sql": 'CREATE INDEX IF NOT EXISTS ix_user_email ON "user" (email);'
    },
    {
        "step": 10,
        "description": "Update Existing Users with Trial Status",
        "sql": """UPDATE "user"
SET subscription_status = 'trial',
    trial_start = NOW()
WHERE subscription_status IS NULL;"""
    },
    {
        "step": 11,
        "description": "Add Email Verification Column (Required for Email Verification)",
        "sql": 'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT false;'
    },
    {
        "step": 12,
        "description": "Add Active Status Column (Required for User Activation)",
        "sql": 'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS active BOOLEAN DEFAULT true;'
    },
    {
        "step": 13,
        "description": "Set Default Email Verified Status for Existing Users",
        "sql": """UPDATE "user"
SET email_verified = false
WHERE email_verified IS NULL;"""
    },
    {
        "step": 14,
        "description": "Set Default Active Status for Existing Users",
        "sql": """UPDATE "user"
SET active = true
WHERE active IS NULL;"""
    },
    {
        "step": 15,
        "description": "Create Email Verification Index for Performance",
        "sql": 'CREATE INDEX IF NOT EXISTS ix_user_email_verified ON "user" (email_verified);'
    },
    {
        "step": 16,
        "description": "Create Active Status Index for Performance",
        "sql": 'CREATE INDEX IF NOT EXISTS ix_user_active ON "user" (active);'
    }
]

VERIFICATION_COMMANDS = [
    {
        "description": "Verify Email Verification Setup",
        "sql": """SELECT email, email_verified, active
FROM "user"
LIMIT 5;"""
    },
    {
        "description": "Verify Migration Success",
        "sql": """SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user' AND table_schema = 'public'
ORDER BY ordinal_position;"""
    }
]


async def run_user_table_migration():
    """Run the exact user table migration commands you specified."""
    
    print("🔧 AxieStudio User Table Migration")
    print("=" * 50)
    print("Running your exact SQL commands...")
    print()
    
    db_service = get_db_service()
    
    try:
        async with db_service.with_session() as session:
            async with session.bind.connect() as connection:
                
                # Run migration commands
                for command in MIGRATION_COMMANDS:
                    print(f"Step {command['step']}: {command['description']}")
                    try:
                        await connection.execute(text(command['sql']))
                        print(f"✅ Success")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                        logger.error(f"Migration step {command['step']} failed: {e}")
                    print()
                
                # Commit all changes
                await connection.commit()
                print("💾 All changes committed to database")
                print()
                
                # Run verification commands
                print("🔍 Verification Results:")
                print("-" * 30)
                
                for verification in VERIFICATION_COMMANDS:
                    print(f"\n📋 {verification['description']}:")
                    try:
                        result = await connection.execute(text(verification['sql']))
                        rows = result.fetchall()
                        
                        if rows:
                            # Print column headers
                            columns = result.keys()
                            print("   " + " | ".join(str(col) for col in columns))
                            print("   " + "-" * (len(" | ".join(str(col) for col in columns))))
                            
                            # Print rows
                            for row in rows:
                                print("   " + " | ".join(str(val) for val in row))
                        else:
                            print("   No results")
                            
                    except Exception as e:
                        print(f"   ❌ Error: {e}")
                
                print("\n🎉 User table migration completed!")
                
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        logger.error(f"User table migration failed: {e}")
        return False
    
    return True


async def show_current_user_table():
    """Show current user table structure."""
    
    print("📋 Current User Table Structure")
    print("=" * 40)
    
    db_service = get_db_service()
    
    try:
        async with db_service.with_session() as session:
            async with session.bind.connect() as connection:
                
                # Get table structure
                result = await connection.execute(text("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_name = 'user' AND table_schema = 'public'
                    ORDER BY ordinal_position;
                """))
                
                rows = result.fetchall()
                
                if rows:
                    print("Column Name          | Data Type    | Nullable | Default")
                    print("-" * 60)
                    for row in rows:
                        col_name = str(row[0]).ljust(20)
                        data_type = str(row[1]).ljust(12)
                        nullable = str(row[2]).ljust(8)
                        default = str(row[3] or "").ljust(10)
                        print(f"{col_name} | {data_type} | {nullable} | {default}")
                else:
                    print("❌ User table not found")
                
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Main function."""
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "migrate":
            success = await run_user_table_migration()
            return 0 if success else 1
        elif command == "status":
            await show_current_user_table()
            return 0
        elif command == "help":
            print("""
🔧 AxieStudio User Table Migration Script

Commands:
  migrate  - Run the exact SQL migration commands
  status   - Show current user table structure
  help     - Show this help message

Examples:
  python user_table_migration.py migrate
  python user_table_migration.py status
            """)
            return 0
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'help' to see available commands")
            return 1
    else:
        # Default: run migration
        success = await run_user_table_migration()
        return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
