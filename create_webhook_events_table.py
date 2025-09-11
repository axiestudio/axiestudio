#!/usr/bin/env python3
"""
🚀 AUTOMATIC WEBHOOK_EVENTS TABLE CREATION
Creates the missing webhook_events table using AxieStudio's automatic database system
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(src_path))

from loguru import logger
from axiestudio.services.database.auto_migration_manager import AutoMigrationManager
from axiestudio.services.deps import get_db_service


async def create_webhook_events_table():
    """Create the webhook_events table using the automatic migration system."""
    
    logger.info("🚀 STARTING AUTOMATIC WEBHOOK_EVENTS TABLE CREATION")
    
    # Set the database URL if provided
    database_url = os.getenv("AXIESTUDIO_DATABASE_URL")
    if database_url:
        logger.info(f"📊 Using database URL: {database_url[:50]}...")
        os.environ["DATABASE_URL"] = database_url
    
    try:
        # Initialize the auto migration manager
        migration_manager = AutoMigrationManager()
        
        logger.info("🔍 Checking current migration status...")
        status = await migration_manager.check_migration_status()
        logger.info(f"📊 Migration status: {status}")
        
        # Create missing tables (including webhook_events)
        logger.info("🔧 Creating missing tables...")
        result = await migration_manager.auto_create_missing_tables()
        
        if result["success"]:
            logger.info("✅ SUCCESS: Tables created successfully!")
            logger.info(f"📋 Created tables: {result['created_tables']}")
        else:
            logger.error("❌ FAILED: Table creation failed!")
            logger.error(f"🚨 Errors: {result['errors']}")
            return False
        
        # Run automatic migration to ensure everything is up to date
        logger.info("🔄 Running automatic migration...")
        migration_result = await migration_manager.run_auto_migration(force=True)
        
        if migration_result["success"]:
            logger.info("✅ SUCCESS: Migration completed successfully!")
        else:
            logger.error("❌ FAILED: Migration failed!")
            logger.error(f"🚨 Errors: {migration_result['errors']}")
            return False
        
        # Verify the webhook_events table was created
        logger.info("🔍 Verifying webhook_events table...")
        db_service = get_db_service()
        
        async with db_service.with_session() as session:
            from sqlalchemy import text, inspect
            
            inspector = inspect(session.bind)
            table_names = inspector.get_table_names()
            
            if "webhook_events" in table_names:
                logger.info("✅ SUCCESS: webhook_events table exists!")
                
                # Check table structure
                columns = inspector.get_columns("webhook_events")
                column_names = [col['name'] for col in columns]
                logger.info(f"📋 Table columns: {column_names}")
                
                expected_columns = [
                    'id', 'stripe_event_id', 'event_type', 'status', 
                    'error_message', 'created_at', 'completed_at'
                ]
                
                missing_columns = [col for col in expected_columns if col not in column_names]
                if missing_columns:
                    logger.warning(f"⚠️ Missing columns: {missing_columns}")
                else:
                    logger.info("✅ All required columns present!")
                
                return True
            else:
                logger.error("❌ FAILED: webhook_events table was not created!")
                logger.error(f"📋 Available tables: {table_names}")
                return False
                
    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR: {e}")
        import traceback
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return False


async def main():
    """Main function."""
    logger.info("🎯 WEBHOOK_EVENTS TABLE CREATION SCRIPT")
    logger.info("=" * 50)
    
    success = await create_webhook_events_table()
    
    if success:
        logger.info("🎉 WEBHOOK_EVENTS TABLE CREATION COMPLETED SUCCESSFULLY!")
        logger.info("✅ Your Stripe webhooks should now work without 500 errors!")
        sys.exit(0)
    else:
        logger.error("💥 WEBHOOK_EVENTS TABLE CREATION FAILED!")
        logger.error("❌ Please check the errors above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
