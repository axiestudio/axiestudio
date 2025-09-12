#!/usr/bin/env python3
"""
Fix webhook_events table schema conflicts
This script drops the existing webhook_events table and lets the database service recreate it correctly.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the axiestudio package to the path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend" / "base"))

from sqlalchemy import text, create_engine
from loguru import logger

def fix_webhook_table():
    """Drop the existing webhook_events table to resolve schema conflicts."""
    
    # Get database URL from environment
    database_url = os.getenv('AXIESTUDIO_DATABASE_URL')
    if not database_url:
        logger.error("❌ AXIESTUDIO_DATABASE_URL not found in environment")
        return False
    
    logger.info("🔧 WEBHOOK TABLE FIX: Starting schema conflict resolution...")
    logger.info(f"📋 Database URL: {database_url[:50]}...")
    
    try:
        # Create sync engine
        sync_engine = create_engine(database_url)
        logger.info("✅ Database engine created successfully")
        
        with sync_engine.connect() as connection:
            logger.info("✅ Database connection established")
            
            # Start transaction
            trans = connection.begin()
            
            try:
                # Check if webhook_events table exists
                result = connection.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'webhook_events'
                    );
                """))
                table_exists = result.scalar()
                
                if table_exists:
                    logger.info("🔍 Found existing webhook_events table - dropping it...")
                    
                    # Drop all indexes first
                    drop_commands = [
                        "DROP INDEX IF EXISTS ix_webhook_events_created_at",
                        "DROP INDEX IF EXISTS ix_webhook_events_status", 
                        "DROP INDEX IF EXISTS ix_webhook_events_stripe_event_id",
                        "DROP INDEX IF EXISTS idx_webhook_events_stripe_event_id",
                        "DROP INDEX IF EXISTS idx_webhook_events_status",
                        "DROP INDEX IF EXISTS idx_webhook_events_event_type",
                        "DROP INDEX IF EXISTS idx_webhook_events_created_at",
                    ]
                    
                    for cmd in drop_commands:
                        try:
                            connection.execute(text(cmd))
                            logger.debug(f"✅ Executed: {cmd}")
                        except Exception as e:
                            logger.debug(f"⚠️ Could not execute {cmd}: {e}")
                    
                    # Drop the table
                    connection.execute(text("DROP TABLE webhook_events CASCADE"))
                    logger.info("✅ Dropped webhook_events table successfully")
                    
                    # Also drop alembic_version to force clean migration
                    connection.execute(text("DROP TABLE IF EXISTS alembic_version"))
                    logger.info("✅ Dropped alembic_version table to force clean migration")
                    
                else:
                    logger.info("✅ webhook_events table doesn't exist - no action needed")
                
                # Commit transaction
                trans.commit()
                logger.info("🎉 WEBHOOK TABLE FIX COMPLETED successfully!")
                logger.info("✅ The database service will recreate the table with correct schema")
                
                return True
                
            except Exception as e:
                trans.rollback()
                logger.error(f"❌ WEBHOOK TABLE FIX FAILED: {e}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False
    
    finally:
        try:
            sync_engine.dispose()
            logger.debug("✅ Database engine disposed")
        except Exception as e:
            logger.warning(f"⚠️ Could not dispose engine: {e}")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    logger.info("🚀 Starting webhook_events table fix...")
    success = fix_webhook_table()
    
    if success:
        logger.info("✅ Fix completed successfully! You can now start the application.")
        sys.exit(0)
    else:
        logger.error("❌ Fix failed! Check the logs above for details.")
        sys.exit(1)
