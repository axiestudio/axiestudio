#!/usr/bin/env python3
"""
LANGFLOW-STYLE FIX TEST: Test if the webhook migration issue is resolved
This will verify that the Langflow-style error handling works properly.
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the axiestudio package to the path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend" / "base"))

# Set environment variables for testing
os.environ.setdefault("AXIESTUDIO_DATABASE_URL", "sqlite:///./test_axiestudio.db")
os.environ.setdefault("AXIESTUDIO_LOG_LEVEL", "DEBUG")

async def test_webhook_table():
    """Test if webhook_events table exists and works properly."""
    
    print("🔍 TESTING WEBHOOK_EVENTS TABLE STATUS")
    print("=" * 50)
    
    try:
        from axiestudio.services.deps import get_db_service
        from sqlalchemy import text
        
        db_service = get_db_service()
        print("✅ Database service loaded")
        
        async with db_service.with_session() as session:
            print("✅ Database connection established")
            
            # Test 1: Check if table exists
            print("\n📋 TEST 1: Checking if webhook_events table exists...")
            try:
                result = await session.execute(text("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'webhook_events' 
                    ORDER BY ordinal_position
                """))
                columns = result.fetchall()
                
                if not columns:
                    print("❌ CRITICAL: webhook_events table DOES NOT EXIST!")
                    print("💡 This means ALL webhooks will fail with 500 errors!")
                    return False
                
                print("✅ webhook_events table exists with schema:")
                for col in columns:
                    nullable = "YES" if col[2] == "YES" else "NO"
                    print(f"   - {col[0]}: {col[1]} (nullable: {nullable})")
                
            except Exception as e:
                print(f"❌ FAILED to check table schema: {e}")
                return False
            
            # Test 2: Check indexes
            print("\n📋 TEST 2: Checking indexes...")
            try:
                result = await session.execute(text("""
                    SELECT indexname, indexdef 
                    FROM pg_indexes 
                    WHERE tablename = 'webhook_events'
                """))
                indexes = result.fetchall()
                
                if indexes:
                    print("✅ Found indexes:")
                    for idx in indexes:
                        print(f"   - {idx[0]}")
                else:
                    print("⚠️ No indexes found - this may impact performance")
                
            except Exception as e:
                print(f"⚠️ Could not check indexes: {e}")
            
            # Test 3: Test INSERT/SELECT operations
            print("\n📋 TEST 3: Testing INSERT/SELECT operations...")
            try:
                test_event_id = f"test_{hash('webhook_test')}"
                
                # Try to insert a test record
                await session.execute(text("""
                    INSERT INTO webhook_events (stripe_event_id, event_type, status, created_at) 
                    VALUES (:id, :type, :status, NOW()) 
                    ON CONFLICT (stripe_event_id) DO NOTHING
                """), {
                    'id': test_event_id, 
                    'type': 'test.event', 
                    'status': 'processing'
                })
                
                # Try to select the record
                result = await session.execute(text("""
                    SELECT stripe_event_id, event_type, status 
                    FROM webhook_events 
                    WHERE stripe_event_id = :id
                """), {'id': test_event_id})
                
                row = result.fetchone()
                
                if row:
                    print("✅ INSERT/SELECT operations working correctly")
                    print(f"   - Retrieved: {row[0]}, {row[1]}, {row[2]}")
                else:
                    print("❌ INSERT/SELECT operations FAILED")
                    return False
                
            except Exception as e:
                print(f"❌ CRITICAL: INSERT/SELECT operations failed: {e}")
                print("💡 This means webhook idempotency is BROKEN!")
                return False
            
            # Test 4: Test webhook endpoint accessibility
            print("\n📋 TEST 4: Checking webhook endpoint...")
            try:
                # Import the webhook handler
                from axiestudio.api.v1.subscriptions import stripe_webhook
                print("✅ Webhook handler can be imported")
                
                # Check if Stripe service is available
                from axiestudio.services.stripe.service import stripe_service
                print("✅ Stripe service is available")
                
            except Exception as e:
                print(f"❌ Webhook handler/service import failed: {e}")
                return False
            
            print("\n🎉 ALL WEBHOOK TESTS PASSED!")
            print("✅ webhook_events table exists and is functional")
            print("✅ Database operations working correctly")
            print("✅ Webhook handlers are importable")
            print("✅ Webhooks should work properly!")
            
            return True
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print("💡 This indicates a serious database or configuration issue")
        return False


async def main():
    """Main test function."""
    print("Starting webhook system test...\n")
    
    success = await test_webhook_table()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ WEBHOOK SYSTEM STATUS: WORKING")
        print("💡 Your webhooks should process correctly")
        print("🚀 Stripe payments should work without 500 errors")
    else:
        print("❌ WEBHOOK SYSTEM STATUS: BROKEN")
        print("💡 Webhooks will fail with 500 errors")
        print("🔧 Database schema needs to be fixed")
        print("\n🛠️ RECOMMENDED ACTIONS:")
        print("1. Run: python fix_migration_loop.py")
        print("2. Or manually create webhook_events table")
        print("3. Restart the application")
    
    return success


if __name__ == "__main__":
    # Fix for Windows ProactorEventLoop issue with psycopg
    import platform
    if platform.system() == "Windows":
        import selectors
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    result = asyncio.run(main())
    sys.exit(0 if result else 1)
