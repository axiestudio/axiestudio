#!/usr/bin/env python3
"""Manual migration script to add subscription columns to Neon database."""

import asyncio
import os
import sys
from datetime import datetime
import asyncpg

# Database connection details from .env
DATABASE_URL = "postgresql://neondb_owner:npg_q2kVnHXNDW1E@ep-sparkling-smoke-a268ipa2-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"

async def add_subscription_columns():
    """Add subscription columns to the user table."""
    print("🚀 Starting manual subscription migration...")
    
    try:
        # Connect to the database
        print("📡 Connecting to Neon database...")
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Check if columns already exist
        print("🔍 Checking existing columns...")
        existing_columns = await conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'user' AND table_schema = 'public'
        """)
        
        existing_column_names = [row['column_name'] for row in existing_columns]
        print(f"📋 Existing columns: {existing_column_names}")
        
        # Define the columns we need to add
        columns_to_add = [
            ("email", "VARCHAR"),
            ("stripe_customer_id", "VARCHAR"),
            ("subscription_status", "VARCHAR DEFAULT 'trial'"),
            ("subscription_id", "VARCHAR"),
            ("trial_start", "TIMESTAMP"),
            ("trial_end", "TIMESTAMP"),
            ("subscription_start", "TIMESTAMP"),
            ("subscription_end", "TIMESTAMP")
        ]
        
        # Add missing columns
        for column_name, column_type in columns_to_add:
            if column_name not in existing_column_names:
                print(f"➕ Adding column: {column_name}")
                await conn.execute(f"""
                    ALTER TABLE "user" 
                    ADD COLUMN {column_name} {column_type}
                """)
            else:
                print(f"✅ Column {column_name} already exists")
        
        # Add email index if it doesn't exist
        try:
            print("📇 Adding email index...")
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS ix_user_email ON "user" (email)
            """)
            print("✅ Email index created")
        except Exception as e:
            print(f"⚠️  Index creation warning: {e}")
        
        # Update existing users with default trial status
        print("🔄 Updating existing users...")
        await conn.execute("""
            UPDATE "user" 
            SET subscription_status = 'trial', 
                trial_start = NOW() 
            WHERE subscription_status IS NULL
        """)
        
        await conn.close()
        print("🎉 Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

async def main():
    """Run the migration."""
    success = await add_subscription_columns()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
