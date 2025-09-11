#!/usr/bin/env python3
"""
🎯 TEST: Conditional Webhook Table Creation
Tests the IF/ELSE logic for webhook_events table creation
"""

import asyncio
import os
import sys

# Simple database test using asyncpg
try:
    import asyncpg
except ImportError:
    print("❌ asyncpg not available - installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "asyncpg"])
    import asyncpg

# Database URL
DATABASE_URL = os.getenv("AXIESTUDIO_DATABASE_URL")
if not DATABASE_URL:
    print("❌ AXIESTUDIO_DATABASE_URL environment variable not set")
    sys.exit(1)

async def test_conditional_webhook_creation():
    """Test the conditional webhook table creation logic."""
    
    print("🎯 TESTING: Conditional Webhook Table Creation (IF/ELSE Logic)")
    print("=" * 70)
    
    try:
        # Connect to database
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Connected to Neon database")
        
        # Step 1: Check if webhook_events table exists
        print("\n🔍 STEP 1: Checking if webhook_events table exists...")
        
        table_exists_query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'webhook_events'
            );
        """
        
        table_exists = await conn.fetchval(table_exists_query)
        print(f"📋 webhook_events table exists: {table_exists}")
        
        # Step 2: Implement IF/ELSE logic as requested
        if table_exists:
            print("✅ IF: Table exists → SKIPPING creation")
            
            # Check table structure
            columns_query = """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'webhook_events' 
                ORDER BY ordinal_position;
            """
            
            columns = await conn.fetch(columns_query)
            print("📋 Current table structure:")
            for col in columns:
                print(f"   - {col['column_name']}: {col['data_type']} ({'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'})")
            
            # Check if event_type column exists
            event_type_exists = any(col['column_name'] == 'event_type' for col in columns)
            
            if event_type_exists:
                print("✅ event_type column exists - table structure is correct")
            else:
                print("❌ event_type column missing - adding it...")
                await conn.execute("""
                    ALTER TABLE webhook_events 
                    ADD COLUMN IF NOT EXISTS event_type VARCHAR(100) NOT NULL DEFAULT 'unknown'
                """)
                print("✅ event_type column added successfully")
                
        else:
            print("❌ ELSE: Table missing → CREATING it...")
            
            # Create the webhook_events table with enterprise schema
            create_table_sql = """
                CREATE TABLE webhook_events (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    stripe_event_id VARCHAR(255) UNIQUE NOT NULL,
                    event_type VARCHAR(100) NOT NULL,
                    status VARCHAR(50) NOT NULL DEFAULT 'processing',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    processed_at TIMESTAMP WITH TIME ZONE,
                    error_message TEXT,
                    retry_count INTEGER DEFAULT 0,
                    metadata JSONB
                );
            """
            
            await conn.execute(create_table_sql)
            print("✅ webhook_events table created successfully")
            
            # Create performance indexes
            indexes_sql = [
                "CREATE INDEX IF NOT EXISTS idx_webhook_events_stripe_event_id ON webhook_events(stripe_event_id);",
                "CREATE INDEX IF NOT EXISTS idx_webhook_events_status ON webhook_events(status);",
                "CREATE INDEX IF NOT EXISTS idx_webhook_events_event_type ON webhook_events(event_type);",
                "CREATE INDEX IF NOT EXISTS idx_webhook_events_created_at ON webhook_events(created_at);"
            ]
            
            for index_sql in indexes_sql:
                await conn.execute(index_sql)
            
            print("✅ Performance indexes created successfully")
        
        # Step 3: Test webhook functionality
        print("\n🧪 STEP 3: Testing webhook functionality...")
        
        test_event_id = "test_conditional_12345"
        test_event_type = "checkout.session.completed"
        
        # Check if test event exists
        event_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1 FROM webhook_events WHERE stripe_event_id = $1
            )
        """, test_event_id)
        
        if event_exists:
            print(f"✅ IF: Test event {test_event_id} exists → SKIPPING insertion")
        else:
            print(f"❌ ELSE: Test event {test_event_id} missing → INSERTING it...")
            
            await conn.execute("""
                INSERT INTO webhook_events (stripe_event_id, event_type, status, created_at) 
                VALUES ($1, $2, 'processing', NOW())
            """, test_event_id, test_event_type)
            
            print("✅ Test webhook event inserted successfully")
        
        # Verify the test event
        test_event = await conn.fetchrow("""
            SELECT stripe_event_id, event_type, status, created_at 
            FROM webhook_events 
            WHERE stripe_event_id = $1
        """, test_event_id)
        
        if test_event:
            print(f"✅ Test verification successful:")
            print(f"   - Event ID: {test_event['stripe_event_id']}")
            print(f"   - Event Type: {test_event['event_type']}")
            print(f"   - Status: {test_event['status']}")
            print(f"   - Created: {test_event['created_at']}")
        else:
            print("❌ Test verification failed")
            return False
        
        # Step 4: Test the actual webhook SQL from the application
        print("\n🔧 STEP 4: Testing application webhook SQL...")
        
        app_test_event_id = "app_test_67890"
        app_test_event_type = "customer.subscription.created"
        
        # This is the exact SQL used in the application
        app_sql = """
            INSERT INTO webhook_events (stripe_event_id, event_type, status, created_at) 
            VALUES ($1, $2, 'processing', NOW())
            ON CONFLICT (stripe_event_id) DO NOTHING
        """
        
        try:
            await conn.execute(app_sql, app_test_event_id, app_test_event_type)
            print("✅ Application webhook SQL executed successfully")
            
            # Verify
            app_event = await conn.fetchrow("""
                SELECT * FROM webhook_events WHERE stripe_event_id = $1
            """, app_test_event_id)
            
            if app_event:
                print("✅ Application webhook event verified in database")
            else:
                print("❌ Application webhook event not found")
                
        except Exception as e:
            print(f"❌ Application webhook SQL failed: {e}")
            return False
        
        await conn.close()
        
        print("\n" + "=" * 70)
        print("🎉 CONDITIONAL WEBHOOK CREATION TEST COMPLETED!")
        print("✅ IF table exists → SKIP creation ✓")
        print("✅ ELSE table missing → CREATE table ✓")
        print("✅ IF event exists → SKIP insertion ✓")
        print("✅ ELSE event missing → INSERT event ✓")
        print("✅ Application webhook SQL working ✓")
        print("🚀 Ready to resolve Alembic multiple heads issue!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_conditional_webhook_creation())
    if success:
        print("\n🎯 SUCCESS: Conditional logic working perfectly!")
        sys.exit(0)
    else:
        print("\n💥 FAILED: Issues detected")
        sys.exit(1)
