#!/usr/bin/env python3
"""
🚀 DIRECT WEBHOOK_EVENTS TABLE CREATION
Creates the missing webhook_events table directly using SQL
"""

import os
import sys
import asyncio
import asyncpg


async def create_webhook_events_table():
    """Create the webhook_events table directly using SQL."""
    
    database_url = os.getenv("AXIESTUDIO_DATABASE_URL")
    if not database_url:
        print("❌ ERROR: AXIESTUDIO_DATABASE_URL environment variable not set!")
        return False
    
    print("🚀 STARTING DIRECT WEBHOOK_EVENTS TABLE CREATION")
    print(f"📊 Using database: {database_url[:50]}...")
    
    try:
        # Connect to the database
        conn = await asyncpg.connect(database_url)
        print("✅ Connected to database successfully!")
        
        # Create the webhook_events table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS webhook_events (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            stripe_event_id VARCHAR NOT NULL UNIQUE,
            event_type VARCHAR NOT NULL,
            status VARCHAR NOT NULL DEFAULT 'processing',
            error_message TEXT,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            completed_at TIMESTAMP WITH TIME ZONE
        );
        """
        
        print("🔧 Creating webhook_events table...")
        await conn.execute(create_table_sql)
        print("✅ webhook_events table created successfully!")
        
        # Create indexes for performance
        indexes_sql = [
            "CREATE INDEX IF NOT EXISTS ix_webhook_events_stripe_event_id ON webhook_events (stripe_event_id);",
            "CREATE INDEX IF NOT EXISTS ix_webhook_events_status ON webhook_events (status);",
            "CREATE INDEX IF NOT EXISTS ix_webhook_events_created_at ON webhook_events (created_at);"
        ]
        
        print("🔧 Creating indexes...")
        for index_sql in indexes_sql:
            await conn.execute(index_sql)
        print("✅ Indexes created successfully!")
        
        # Verify the table was created
        print("🔍 Verifying table creation...")
        result = await conn.fetch("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'webhook_events' 
            ORDER BY ordinal_position;
        """)
        
        if result:
            print("✅ webhook_events table verified!")
            print("📋 Table structure:")
            for row in result:
                print(f"   - {row['column_name']}: {row['data_type']} ({'NULL' if row['is_nullable'] == 'YES' else 'NOT NULL'})")
        else:
            print("❌ ERROR: webhook_events table not found after creation!")
            return False
        
        # Close connection
        await conn.close()
        print("✅ Database connection closed.")
        
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return False


async def main():
    """Main function."""
    print("🎯 DIRECT WEBHOOK_EVENTS TABLE CREATION SCRIPT")
    print("=" * 50)
    
    success = await create_webhook_events_table()
    
    if success:
        print("\n🎉 WEBHOOK_EVENTS TABLE CREATION COMPLETED SUCCESSFULLY!")
        print("✅ Your Stripe webhooks should now work without 500 errors!")
        print("\n📋 NEXT STEPS:")
        print("1. Restart your application")
        print("2. Test a Stripe webhook to verify it works")
        print("3. Check your application logs for successful webhook processing")
        sys.exit(0)
    else:
        print("\n💥 WEBHOOK_EVENTS TABLE CREATION FAILED!")
        print("❌ Please check the errors above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
