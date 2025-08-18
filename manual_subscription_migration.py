#!/usr/bin/env python3
"""
Manual database migration script for subscription columns.
Run this directly to add subscription columns to the user table.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

from loguru import logger
from sqlalchemy import text

async def manual_migration():
    """Manually add subscription columns to the user table."""
    try:
        # Import after path setup
        from axiestudio.services.deps import get_db_service
        
        logger.info("Starting manual subscription migration...")
        
        # Get database service
        db_service = get_db_service()
        logger.info(f"Database URL: {db_service.database_url}")
        
        # Check if we're using SQLite or PostgreSQL
        db_url = str(db_service.database_url).lower()
        is_sqlite = "sqlite" in db_url
        logger.info(f"Database type: {'SQLite' if is_sqlite else 'PostgreSQL'}")
        
        async with db_service.with_session() as session:
            # First, check existing columns
            logger.info("Checking existing columns...")
            
            if is_sqlite:
                result = await session.exec(text("PRAGMA table_info(user);"))
                rows = result.fetchall()
                existing_columns = {row[1] for row in rows}
            else:
                result = await session.exec(text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'user' AND table_schema = 'public';
                """))
                rows = result.fetchall()
                existing_columns = {row[0] for row in rows}
            
            logger.info(f"Existing columns: {sorted(existing_columns)}")
            
            # Define subscription columns to add
            subscription_columns = {
                'stripe_customer_id': 'VARCHAR(255)',
                'subscription_status': "VARCHAR(50) DEFAULT 'trial'",
                'subscription_id': 'VARCHAR(255)',
                'trial_start': 'TIMESTAMP',
                'trial_end': 'TIMESTAMP',
                'subscription_start': 'TIMESTAMP',
                'subscription_end': 'TIMESTAMP'
            }
            
            # Add missing columns
            added_columns = []
            for column_name, column_def in subscription_columns.items():
                if column_name not in existing_columns:
                    try:
                        if is_sqlite:
                            sql = f"ALTER TABLE user ADD COLUMN {column_name} {column_def};"
                        else:
                            sql = f'ALTER TABLE "user" ADD COLUMN {column_name} {column_def};'
                        
                        logger.info(f"Executing: {sql}")
                        await session.exec(text(sql))
                        added_columns.append(column_name)
                        logger.info(f"✅ Added column: {column_name}")
                        
                    except Exception as e:
                        logger.warning(f"❌ Failed to add column {column_name}: {e}")
                else:
                    logger.info(f"⏭️  Column {column_name} already exists")
            
            # Commit the changes
            if added_columns:
                await session.commit()
                logger.info(f"✅ Successfully added {len(added_columns)} columns: {added_columns}")
                
                # Update existing users with default trial values
                try:
                    logger.info("Setting default trial values for existing users...")
                    
                    if is_sqlite:
                        update_sql = """
                            UPDATE user 
                            SET 
                                trial_start = COALESCE(trial_start, create_at),
                                trial_end = COALESCE(trial_end, datetime(create_at, '+7 days')),
                                subscription_status = COALESCE(subscription_status, 'trial')
                            WHERE trial_start IS NULL OR subscription_status IS NULL;
                        """
                    else:
                        update_sql = """
                            UPDATE "user" 
                            SET 
                                trial_start = COALESCE(trial_start, create_at),
                                trial_end = COALESCE(trial_end, create_at + INTERVAL '7 days'),
                                subscription_status = COALESCE(subscription_status, 'trial')
                            WHERE trial_start IS NULL OR subscription_status IS NULL;
                        """
                    
                    result = await session.exec(text(update_sql))
                    await session.commit()
                    logger.info("✅ Updated existing users with trial defaults")
                    
                except Exception as e:
                    logger.warning(f"❌ Failed to update existing users: {e}")
                    
            else:
                logger.info("✅ All subscription columns already exist - no migration needed")
            
            # Verify final state
            logger.info("Verifying final column state...")
            if is_sqlite:
                result = await session.exec(text("PRAGMA table_info(user);"))
                rows = result.fetchall()
                final_columns = {row[1] for row in rows}
            else:
                result = await session.exec(text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'user' AND table_schema = 'public';
                """))
                rows = result.fetchall()
                final_columns = {row[0] for row in rows}
            
            subscription_present = [col for col in subscription_columns.keys() if col in final_columns]
            subscription_missing = [col for col in subscription_columns.keys() if col not in final_columns]
            
            logger.info(f"✅ Subscription columns present: {subscription_present}")
            if subscription_missing:
                logger.error(f"❌ Subscription columns still missing: {subscription_missing}")
                return False
            else:
                logger.info("🎉 All subscription columns are now present!")
                return True
                
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting manual subscription migration...")
    success = asyncio.run(manual_migration())
    if success:
        logger.info("🎉 Migration completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Migration failed!")
        sys.exit(1)
