"""Database health check and monitoring service for Axie Studio."""

import asyncio
import time
from typing import Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger


class DatabaseHealthChecker:
    """Monitor database health and provide fallback strategies."""
    
    def __init__(self):
        self.last_check_time: Optional[float] = None
        self.last_check_result: bool = False
        self.consecutive_failures: int = 0
        self.max_failures_before_alert: int = 3
        
    async def check_database_health(self, session: AsyncSession) -> Dict[str, Any]:
        """
        Comprehensive database health check.
        
        Returns:
            Dict with health status, metrics, and recommendations
        """
        start_time = time.time()
        health_status = {
            "healthy": False,
            "response_time_ms": 0,
            "connection_pool_status": "unknown",
            "table_count": 0,
            "last_error": None,
            "recommendations": []
        }
        
        try:
            # Test basic connectivity
            result = await session.execute(text("SELECT 1"))
            result.fetchone()
            
            # Check response time
            response_time = (time.time() - start_time) * 1000
            health_status["response_time_ms"] = round(response_time, 2)
            
            # Count tables (indicates successful migrations)
            table_result = await session.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = table_result.scalar()
            health_status["table_count"] = table_count
            
            # Check connection pool if available
            if hasattr(session.bind, 'pool'):
                pool = session.bind.pool
                health_status["connection_pool_status"] = {
                    "size": pool.size(),
                    "checked_in": pool.checkedin(),
                    "checked_out": pool.checkedout(),
                    "overflow": pool.overflow(),
                }
            
            # Determine overall health
            health_status["healthy"] = True
            self.consecutive_failures = 0
            
            # Add performance recommendations
            if response_time > 1000:  # > 1 second
                health_status["recommendations"].append(
                    "Database response time is slow. Consider optimizing queries or upgrading database."
                )
            
            if table_count < 5:  # Expected minimum tables
                health_status["recommendations"].append(
                    "Low table count detected. Database migrations may not have completed."
                )
                
            logger.info(f"Database health check passed: {response_time:.2f}ms, {table_count} tables")
            
        except Exception as e:
            self.consecutive_failures += 1
            health_status["last_error"] = str(e)
            health_status["recommendations"].append(
                "Database connection failed. Check connection string and network connectivity."
            )
            
            if self.consecutive_failures >= self.max_failures_before_alert:
                health_status["recommendations"].append(
                    f"Database has failed {self.consecutive_failures} consecutive health checks. "
                    "Consider switching to backup database or maintenance mode."
                )
            
            logger.error(f"Database health check failed: {e}")
        
        self.last_check_time = time.time()
        self.last_check_result = health_status["healthy"]
        
        return health_status
    
    async def test_database_connection(self, database_url: str) -> bool:
        """
        Test if a database URL is accessible.
        
        Args:
            database_url: Database connection string to test
            
        Returns:
            True if connection successful, False otherwise
        """
        try:
            from sqlalchemy.ext.asyncio import create_async_engine
            
            # Create temporary engine for testing
            engine = create_async_engine(database_url, echo=False)
            
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            
            await engine.dispose()
            logger.info(f"Database connection test successful: {database_url[:30]}...")
            return True
            
        except Exception as e:
            logger.warning(f"Database connection test failed: {e}")
            return False
    
    def get_fallback_recommendations(self) -> list[str]:
        """Get recommendations for database fallback strategies."""
        recommendations = []
        
        if self.consecutive_failures > 0:
            recommendations.extend([
                "Consider implementing read-only mode during database issues",
                "Cache frequently accessed data in Redis or memory",
                "Set up database connection retry logic with exponential backoff",
                "Monitor Supabase status page for service issues",
                "Consider setting up a backup database instance"
            ])
        
        return recommendations


# Global health checker instance
db_health_checker = DatabaseHealthChecker()
