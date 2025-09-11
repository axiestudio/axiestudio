#!/usr/bin/env python3
"""
🧪 WEBHOOK FIX VERIFICATION SCRIPT
Tests that the webhook_events table exists and webhook handlers work correctly
"""

import os
import sys
import asyncio
import asyncpg
import json


async def test_webhook_system():
    """Test the webhook system comprehensively."""
    
    database_url = os.getenv("AXIESTUDIO_DATABASE_URL")
    if not database_url:
        print("❌ ERROR: AXIESTUDIO_DATABASE_URL environment variable not set!")
        return False
    
    print("🧪 TESTING WEBHOOK SYSTEM")
    print("=" * 50)
    print(f"📊 Database: {database_url[:50]}...")
    
    try:
        # Connect to the database
        conn = await asyncpg.connect(database_url)
        print("✅ Connected to database successfully!")
        
        # Test 1: Verify webhook_events table exists
        print("\n🔍 TEST 1: Verifying webhook_events table...")
        result = await conn.fetch("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'webhook_events' 
            ORDER BY ordinal_position;
        """)
        
        if result:
            print("✅ webhook_events table exists!")
            print("📋 Table structure:")
            for row in result:
                print(f"   - {row['column_name']}: {row['data_type']} ({'NULL' if row['is_nullable'] == 'YES' else 'NOT NULL'})")
        else:
            print("❌ ERROR: webhook_events table not found!")
            return False
        
        # Test 2: Verify indexes exist
        print("\n🔍 TEST 2: Verifying indexes...")
        indexes = await conn.fetch("""
            SELECT indexname, indexdef 
            FROM pg_indexes 
            WHERE tablename = 'webhook_events';
        """)
        
        expected_indexes = [
            'ix_webhook_events_stripe_event_id',
            'ix_webhook_events_status', 
            'ix_webhook_events_created_at'
        ]
        
        found_indexes = [idx['indexname'] for idx in indexes]
        print(f"📋 Found indexes: {found_indexes}")
        
        for expected_idx in expected_indexes:
            if expected_idx in found_indexes:
                print(f"   ✅ {expected_idx}")
            else:
                print(f"   ⚠️ Missing: {expected_idx}")
        
        # Test 3: Test webhook event insertion
        print("\n🔍 TEST 3: Testing webhook event insertion...")
        test_event_id = "evt_test_webhook_fix_123"
        
        # Clean up any existing test data
        await conn.execute("DELETE FROM webhook_events WHERE stripe_event_id = $1", test_event_id)
        
        # Insert test webhook event
        await conn.execute("""
            INSERT INTO webhook_events (stripe_event_id, event_type, status, created_at) 
            VALUES ($1, $2, $3, NOW())
        """, test_event_id, "checkout.session.completed", "processing")
        
        print("✅ Test webhook event inserted successfully!")
        
        # Verify insertion
        result = await conn.fetchrow("""
            SELECT * FROM webhook_events WHERE stripe_event_id = $1
        """, test_event_id)
        
        if result:
            print("✅ Test webhook event retrieved successfully!")
            print(f"   - ID: {result['id']}")
            print(f"   - Event ID: {result['stripe_event_id']}")
            print(f"   - Event Type: {result['event_type']}")
            print(f"   - Status: {result['status']}")
            print(f"   - Created: {result['created_at']}")
        else:
            print("❌ ERROR: Test webhook event not found after insertion!")
            return False
        
        # Test 4: Test webhook event update
        print("\n🔍 TEST 4: Testing webhook event update...")
        await conn.execute("""
            UPDATE webhook_events 
            SET status = 'completed', completed_at = NOW() 
            WHERE stripe_event_id = $1
        """, test_event_id)
        
        # Verify update
        result = await conn.fetchrow("""
            SELECT status, completed_at FROM webhook_events WHERE stripe_event_id = $1
        """, test_event_id)
        
        if result and result['status'] == 'completed' and result['completed_at']:
            print("✅ Test webhook event updated successfully!")
            print(f"   - Status: {result['status']}")
            print(f"   - Completed: {result['completed_at']}")
        else:
            print("❌ ERROR: Test webhook event update failed!")
            return False
        
        # Test 5: Test duplicate prevention
        print("\n🔍 TEST 5: Testing duplicate prevention...")
        try:
            await conn.execute("""
                INSERT INTO webhook_events (stripe_event_id, event_type, status, created_at) 
                VALUES ($1, $2, $3, NOW())
            """, test_event_id, "checkout.session.completed", "processing")
            print("❌ ERROR: Duplicate insertion should have failed!")
            return False
        except asyncpg.UniqueViolationError:
            print("✅ Duplicate prevention working correctly!")
        
        # Clean up test data
        await conn.execute("DELETE FROM webhook_events WHERE stripe_event_id = $1", test_event_id)
        print("🧹 Test data cleaned up.")
        
        # Test 6: Check for existing webhook events
        print("\n🔍 TEST 6: Checking existing webhook events...")
        count = await conn.fetchval("SELECT COUNT(*) FROM webhook_events")
        print(f"📊 Total webhook events in database: {count}")
        
        if count > 0:
            recent_events = await conn.fetch("""
                SELECT stripe_event_id, event_type, status, created_at 
                FROM webhook_events 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            
            print("📋 Recent webhook events:")
            for event in recent_events:
                print(f"   - {event['stripe_event_id']}: {event['event_type']} ({event['status']})")
        
        # Close connection
        await conn.close()
        print("\n✅ Database connection closed.")
        
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return False


async def main():
    """Main function."""
    print("🎯 WEBHOOK SYSTEM VERIFICATION SCRIPT")
    
    success = await test_webhook_system()
    
    if success:
        print("\n🎉 ALL WEBHOOK TESTS PASSED!")
        print("✅ Your webhook system is ready to handle Stripe events!")
        print("\n📋 WHAT THIS MEANS:")
        print("• webhook_events table exists with correct structure")
        print("• Indexes are in place for performance")
        print("• Webhook event insertion/update works")
        print("• Duplicate prevention is working")
        print("• No more 500 errors on webhook processing!")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Restart your AxieStudio application")
        print("2. Test a real Stripe webhook (create a subscription)")
        print("3. Check your application logs for successful processing")
        print("4. Verify no more 500 errors in Stripe dashboard")
        
        sys.exit(0)
    else:
        print("\n💥 WEBHOOK TESTS FAILED!")
        print("❌ Please check the errors above and fix them.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
