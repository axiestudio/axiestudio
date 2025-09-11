#!/usr/bin/env python3
"""
🚀 MASTER BRANCH: Create webhook_events table for Swedish version
This script creates the missing webhook_events table in the Neon database for the master branch.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(project_root))

async def create_webhook_events_table():
    """Create the webhook_events table for master branch."""
    
    print("🚀 MASTER BRANCH: Creating webhook_events table for Swedish version")
    print("=" * 70)
    
    try:
        import asyncpg
        
        # Get database URL from environment
        database_url = os.getenv('AXIESTUDIO_DATABASE_URL')
        if not database_url:
            print("❌ AXIESTUDIO_DATABASE_URL environment variable not set")
            return False
        
        print(f"🔗 Connecting to database...")
        
        # Connect to database
        conn = await asyncpg.connect(database_url)
        
        # Check if table already exists
        table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'webhook_events'
            );
        """)
        
        if table_exists:
            print("✅ webhook_events table already exists")
            await conn.close()
            return True
        
        print("📋 Creating webhook_events table...")
        
        # Create the webhook_events table
        await conn.execute("""
            CREATE TABLE webhook_events (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                stripe_event_id VARCHAR NOT NULL UNIQUE,
                event_type VARCHAR NOT NULL,
                status VARCHAR NOT NULL DEFAULT 'processing',
                error_message TEXT,
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                completed_at TIMESTAMP WITH TIME ZONE
            );
        """)
        
        print("📊 Creating performance indexes...")
        
        # Create indexes for performance
        await conn.execute("""
            CREATE INDEX ix_webhook_events_stripe_event_id ON webhook_events (stripe_event_id);
        """)
        
        await conn.execute("""
            CREATE INDEX ix_webhook_events_status ON webhook_events (status);
        """)
        
        await conn.execute("""
            CREATE INDEX ix_webhook_events_created_at ON webhook_events (created_at);
        """)
        
        print("✅ webhook_events table created successfully!")
        print("✅ Performance indexes created!")
        
        # Verify table structure
        columns = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'webhook_events'
            ORDER BY ordinal_position;
        """)
        
        print("\n📋 Table structure verification:")
        for col in columns:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
            print(f"  • {col['column_name']}: {col['data_type']} {nullable}{default}")
        
        # Test insert and select
        print("\n🧪 Testing table operations...")
        
        test_event_id = "evt_test_master_branch_123"
        await conn.execute("""
            INSERT INTO webhook_events (stripe_event_id, event_type, status)
            VALUES ($1, $2, $3)
        """, test_event_id, "test.event", "completed")
        
        result = await conn.fetchrow("""
            SELECT * FROM webhook_events WHERE stripe_event_id = $1
        """, test_event_id)
        
        if result:
            print("✅ Insert/Select test passed")
            
            # Clean up test data
            await conn.execute("""
                DELETE FROM webhook_events WHERE stripe_event_id = $1
            """, test_event_id)
            print("✅ Test data cleaned up")
        else:
            print("❌ Insert/Select test failed")
            return False
        
        await conn.close()
        
        print("\n🎉 SUCCESS: webhook_events table ready for master branch!")
        print("🇸🇪 Swedish webhook processing is now bulletproof!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating webhook_events table: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main function."""
    success = await create_webhook_events_table()
    
    if success:
        print("\n✅ MASTER BRANCH READY: Swedish webhook system is production-ready!")
        return 0
    else:
        print("\n❌ FAILED: Could not set up webhook system for master branch")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
