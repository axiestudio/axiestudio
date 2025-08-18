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
        # Get database service with error handling
        try:
            db_service = get_db_service()
            if not db_service:
                logger.warning("Database service not initialized - skipping subscription schema setup")
                return False
        except Exception as e:
            logger.warning(f"Failed to get database service: {e} - skipping subscription schema setup")
            return False
        
        # Check if we're using SQLite or PostgreSQL for appropriate syntax
        db_url = str(db_service.database_url).lower()
        is_sqlite = "sqlite" in db_url

        # SQL commands to add subscription fields if they don't exist
        if is_sqlite:
            # SQLite syntax (newer versions support IF NOT EXISTS)
            migration_commands = [
                "ALTER TABLE user ADD COLUMN stripe_customer_id VARCHAR(255) NULL;",
                "ALTER TABLE user ADD COLUMN subscription_status VARCHAR(50) DEFAULT 'trial';",
                "ALTER TABLE user ADD COLUMN subscription_id VARCHAR(255) NULL;",
                "ALTER TABLE user ADD COLUMN trial_start TIMESTAMP NULL;",
                "ALTER TABLE user ADD COLUMN trial_end TIMESTAMP NULL;",
                "ALTER TABLE user ADD COLUMN subscription_start TIMESTAMP NULL;",
                "ALTER TABLE user ADD COLUMN subscription_end TIMESTAMP NULL;"
            ]
        else:
            # PostgreSQL syntax
            migration_commands = [
                "ALTER TABLE user ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(255) NULL;",
                "ALTER TABLE user ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(50) DEFAULT 'trial';",
                "ALTER TABLE user ADD COLUMN IF NOT EXISTS subscription_id VARCHAR(255) NULL;",
                "ALTER TABLE user ADD COLUMN IF NOT EXISTS trial_start TIMESTAMP NULL;",
                "ALTER TABLE user ADD COLUMN IF NOT EXISTS trial_end TIMESTAMP NULL;",
                "ALTER TABLE user ADD COLUMN IF NOT EXISTS subscription_start TIMESTAMP NULL;",
                "ALTER TABLE user ADD COLUMN IF NOT EXISTS subscription_end TIMESTAMP NULL;"
            ]
        
        try:
            async with db_service.with_session() as session:
                logger.info("Setting up subscription database schema...")

                # First, try to add columns (these might fail if columns already exist)
                for i, command in enumerate(migration_commands, 1):
                    try:
                        await session.exec(text(command))
                        logger.debug(f"Executed subscription schema command {i}/{len(migration_commands)}")
                    except Exception as e:
                        # Column might already exist, which is fine
                        logger.debug(f"Schema command {i} result: {e}")

                # Commit the schema changes first
                try:
                    await session.commit()
                    logger.debug("Schema changes committed successfully")
                except Exception as e:
                    logger.warning(f"Failed to commit schema changes: {e}")
                    await session.rollback()
                    return False

                # Update existing users to have trial information if they don't have it
                try:
                    if is_sqlite:
                        # SQLite syntax
                        update_existing_users_query = text("""
                            UPDATE user
                            SET
                                trial_start = COALESCE(trial_start, create_at),
                                trial_end = COALESCE(trial_end, datetime(create_at, '+7 days')),
                                subscription_status = COALESCE(subscription_status, 'trial')
                            WHERE trial_start IS NULL OR subscription_status IS NULL;
                        """)
                    else:
                        # PostgreSQL syntax
                        update_existing_users_query = text("""
                            UPDATE "user"
                            SET
                                trial_start = COALESCE(trial_start, create_at),
                                trial_end = COALESCE(trial_end, create_at + INTERVAL '7 days'),
                                subscription_status = COALESCE(subscription_status, 'trial')
                            WHERE trial_start IS NULL OR subscription_status IS NULL;
                        """)

                    result = await session.exec(update_existing_users_query)
                    await session.commit()
                    logger.info("Successfully set up subscription database schema and updated existing users")

                except Exception as e:
                    logger.warning(f"User update query failed: {e} - schema setup completed but user updates skipped")
                    await session.rollback()
                    # Don't return False here - schema setup was successful

        except Exception as e:
            logger.error(f"Database session error during subscription setup: {e}")
            return False
                
        return True
        
    except Exception as e:
        logger.error(f"Failed to set up subscription schema: {e}")
        return False


def run_subscription_setup():
    """Synchronous wrapper for subscription setup."""
    try:
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(setup_subscription_schema())
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error running subscription setup: {e}")


# Don't auto-run on import - this will be called explicitly during app startup
# This prevents threading issues and startup hangs
logger.debug("Subscription setup module loaded - will run during app startup")
