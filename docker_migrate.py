#!/usr/bin/env python3
"""
Docker-compatible migration script for subscription columns.
This can be run inside the Docker container.
"""

import asyncio
import os
import sys

# Set up environment for Docker
os.environ.setdefault("AXIESTUDIO_LOG_LEVEL", "INFO")

# Add the app path
sys.path.insert(0, "/app/src/backend/base")

from loguru import logger

async def run_migration():
    """Run the subscription migration inside Docker."""
    try:
        # Import the CLI migration function
        from axiestudio.cli.migrate_subscription import migrate_subscription_schema
        
        logger.info("🐳 Running subscription migration in Docker...")
        success = await migrate_subscription_schema()
        
        if success:
            logger.info("🎉 Docker migration completed successfully!")
            return True
        else:
            logger.error("❌ Docker migration failed!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Docker migration error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_migration())
    sys.exit(0 if success else 1)
