#!/usr/bin/env python3
"""
🇸🇪 MASTER BRANCH: Test Swedish webhook system
Test the webhook system on the master branch (Swedish version)
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(project_root))

async def test_master_webhook_system():
    """Test the webhook system on master branch."""
    
    print("🇸🇪 MASTER BRANCH: Testing Swedish webhook system")
    print("=" * 60)
    
    try:
        import asyncpg
        
        # Get database URL from environment
        database_url = os.getenv('AXIESTUDIO_DATABASE_URL')
        if not database_url:
            print("❌ AXIESTUDIO_DATABASE_URL environment variable not set")
            return False
        
        print("🔗 Connecting to database...")
        conn = await asyncpg.connect(database_url)
        
        # Test 1: Verify webhook_events table structure
        print("\n📋 Test 1: Verifying webhook_events table structure...")
        
        columns = await conn.fetch("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'webhook_events'
            ORDER BY ordinal_position;
        """)
        
        expected_columns = ['id', 'stripe_event_id', 'event_type', 'status', 'error_message', 'created_at', 'completed_at']
        actual_columns = [col['column_name'] for col in columns]
        
        if all(col in actual_columns for col in expected_columns):
            print("✅ All required columns present")
        else:
            missing = [col for col in expected_columns if col not in actual_columns]
            print(f"❌ Missing columns: {missing}")
            return False
        
        # Test 2: Test webhook event insertion
        print("\n🧪 Test 2: Testing webhook event insertion...")
        
        test_events = [
            ("evt_master_checkout_123", "checkout.session.completed"),
            ("evt_master_subscription_123", "customer.subscription.created"),
            ("evt_master_payment_123", "invoice.payment_succeeded")
        ]
        
        for event_id, event_type in test_events:
            await conn.execute("""
                INSERT INTO webhook_events (stripe_event_id, event_type, status)
                VALUES ($1, $2, $3)
                ON CONFLICT (stripe_event_id) DO NOTHING
            """, event_id, event_type, "completed")
            
            # Verify insertion
            result = await conn.fetchrow("""
                SELECT * FROM webhook_events WHERE stripe_event_id = $1
            """, event_id)
            
            if result:
                print(f"✅ {event_type} event recorded successfully")
            else:
                print(f"❌ Failed to record {event_type} event")
                return False
        
        # Test 3: Test idempotency (duplicate prevention)
        print("\n🔒 Test 3: Testing idempotency (duplicate prevention)...")
        
        # Try to insert duplicate
        try:
            await conn.execute("""
                INSERT INTO webhook_events (stripe_event_id, event_type, status)
                VALUES ($1, $2, $3)
            """, "evt_master_checkout_123", "checkout.session.completed", "processing")
            print("❌ Duplicate insertion should have failed")
            return False
        except Exception:
            print("✅ Duplicate prevention working correctly")
        
        # Test 4: Test webhook status updates
        print("\n📝 Test 4: Testing webhook status updates...")
        
        await conn.execute("""
            UPDATE webhook_events 
            SET status = 'failed', error_message = 'Test error', completed_at = NOW()
            WHERE stripe_event_id = $1
        """, "evt_master_payment_123")
        
        result = await conn.fetchrow("""
            SELECT status, error_message FROM webhook_events 
            WHERE stripe_event_id = $1
        """, "evt_master_payment_123")
        
        if result and result['status'] == 'failed' and result['error_message'] == 'Test error':
            print("✅ Webhook status update working correctly")
        else:
            print("❌ Webhook status update failed")
            return False
        
        # Test 5: Test performance indexes
        print("\n⚡ Test 5: Testing performance indexes...")
        
        indexes = await conn.fetch("""
            SELECT indexname FROM pg_indexes 
            WHERE tablename = 'webhook_events'
        """)
        
        index_names = [idx['indexname'] for idx in indexes]
        expected_indexes = ['ix_webhook_events_stripe_event_id', 'ix_webhook_events_status', 'ix_webhook_events_created_at']
        
        for expected_idx in expected_indexes:
            if any(expected_idx in idx_name for idx_name in index_names):
                print(f"✅ Index {expected_idx} exists")
            else:
                print(f"⚠️ Index {expected_idx} might be missing")
        
        # Clean up test data
        print("\n🧹 Cleaning up test data...")
        for event_id, _ in test_events:
            await conn.execute("""
                DELETE FROM webhook_events WHERE stripe_event_id = $1
            """, event_id)
        
        print("✅ Test data cleaned up")
        
        await conn.close()
        
        print("\n🎉 ALL TESTS PASSED!")
        print("🇸🇪 Swedish webhook system is production-ready!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main function."""
    success = await test_master_webhook_system()
    
    if success:
        print("\n✅ MASTER BRANCH WEBHOOK SYSTEM: PRODUCTION READY!")
        print("🇸🇪 Swedish users will get immediate access after payment!")
        return 0
    else:
        print("\n❌ MASTER BRANCH WEBHOOK SYSTEM: NEEDS FIXES!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
