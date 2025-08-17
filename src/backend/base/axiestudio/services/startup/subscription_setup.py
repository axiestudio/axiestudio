"""Startup service to initialize subscription-related database schema."""

import asyncio
from loguru import logger

try:
    from axiestudio.services.deps import get_db_service
    from sqlalchemy import text
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    logger.warning("Database services not available - skipping subscription setup")


async def setup_subscription_schema():
    """Set up subscription-related database schema on startup."""
    if not DB_AVAILABLE:
        logger.warning("Database not available - skipping subscription schema setup")
        return False
    
    try:
        db_service = get_db_service()
        
        # SQL commands to add subscription fields if they don't exist
        migration_commands = [
            """
            ALTER TABLE user 
            ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(255) NULL;
            """,
            """
            ALTER TABLE user 
            ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(50) DEFAULT 'trial';
            """,
            """
            ALTER TABLE user 
            ADD COLUMN IF NOT EXISTS subscription_id VARCHAR(255) NULL;
            """,
            """
            ALTER TABLE user 
            ADD COLUMN IF NOT EXISTS trial_start TIMESTAMP NULL;
            """,
            """
            ALTER TABLE user 
            ADD COLUMN IF NOT EXISTS trial_end TIMESTAMP NULL;
            """,
            """
            ALTER TABLE user 
            ADD COLUMN IF NOT EXISTS subscription_start TIMESTAMP NULL;
            """,
            """
            ALTER TABLE user 
            ADD COLUMN IF NOT EXISTS subscription_end TIMESTAMP NULL;
            """
        ]
        
        async with db_service.with_session() as session:
            logger.info("Setting up subscription database schema...")
            
            for i, command in enumerate(migration_commands, 1):
                try:
                    await session.exec(text(command))
                    logger.debug(f"Executed subscription schema command {i}/{len(migration_commands)}")
                except Exception as e:
                    # Column might already exist, which is fine
                    logger.debug(f"Schema command {i} result: {e}")
            
            # Update existing users to have trial information if they don't have it
            try:
                update_existing_users_query = text("""
                    UPDATE user 
                    SET 
                        trial_start = COALESCE(trial_start, create_at),
                        trial_end = COALESCE(trial_end, datetime(create_at, '+7 days')),
                        subscription_status = COALESCE(subscription_status, 'trial')
                    WHERE trial_start IS NULL OR subscription_status IS NULL;
                """)
                
                result = await session.exec(update_existing_users_query)
                await session.commit()
                logger.info("Successfully set up subscription database schema")
                
            except Exception as e:
                logger.debug(f"User update query result: {e}")
                await session.commit()
                
        return True
        
    except Exception as e:
        logger.error(f"Failed to set up subscription schema: {e}")
        return False


def run_subscription_setup():
    """Synchronous wrapper for subscription setup."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create a task
            asyncio.create_task(setup_subscription_schema())
        else:
            # If not in async context, run directly
            asyncio.run(setup_subscription_schema())
    except Exception as e:
        logger.error(f"Error running subscription setup: {e}")


# Auto-run setup when module is imported (for Docker startup)
if DB_AVAILABLE:
    try:
        # Try to run setup, but don't fail if it doesn't work
        import threading
        setup_thread = threading.Thread(target=run_subscription_setup, daemon=True)
        setup_thread.start()
        logger.info("Subscription setup initiated in background")
    except Exception as e:
        logger.debug(f"Background subscription setup failed: {e}")
