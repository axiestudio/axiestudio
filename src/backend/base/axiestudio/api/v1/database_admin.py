"""
🗄️ Database Administration API Endpoints

Provides REST API endpoints for database management operations including
table creation, migration status, and health monitoring.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import inspect, text
from sqlmodel import SQLModel
import logging

from axiestudio.api.deps import get_current_active_superuser
from axiestudio.services.database.service import DatabaseService
from axiestudio.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()


class DatabaseStatus:
    """Database status information"""
    
    def __init__(self, 
                 connected: bool = False,
                 total_tables: int = 0,
                 required_tables_exist: int = 0,
                 required_tables_total: int = 0,
                 missing_tables: List[str] = None,
                 table_details: List[Dict[str, Any]] = None):
        self.connected = connected
        self.total_tables = total_tables
        self.required_tables_exist = required_tables_exist
        self.required_tables_total = required_tables_total
        self.missing_tables = missing_tables or []
        self.table_details = table_details or []


@router.get("/status")
async def get_database_status(
    current_user: User = Depends(get_current_active_superuser)
) -> Dict[str, Any]:
    """
    Get comprehensive database status information.
    
    Returns:
        - Connection status
        - Table counts and details
        - Missing tables
        - Health indicators
    """
    try:
        db_service = DatabaseService()
        
        async with db_service.get_session() as session:
            connection = session.connection()
            inspector = inspect(connection)
            
            # Test connection
            await session.execute(text("SELECT 1"))
            
            # Get table information
            table_names = inspector.get_table_names()
            required_tables = ["flow", "user", "apikey", "folder", "message", "variable", "transaction", "vertex_build"]
            
            existing_required = [t for t in required_tables if t in table_names]
            missing_tables = [t for t in required_tables if t not in table_names]
            
            # Get table details
            table_details = []
            for table_name in table_names:
                try:
                    columns = inspector.get_columns(table_name)
                    pk_constraint = inspector.get_pk_constraint(table_name)
                    
                    # Get row count
                    try:
                        result = await session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                        row_count = result.scalar()
                    except Exception:
                        row_count = None
                    
                    table_details.append({
                        "name": table_name,
                        "column_count": len(columns),
                        "primary_key": pk_constraint.get('constrained_columns', []),
                        "row_count": row_count,
                        "is_required": table_name in required_tables
                    })
                except Exception as e:
                    logger.warning(f"Error getting details for table {table_name}: {e}")
                    table_details.append({
                        "name": table_name,
                        "error": str(e),
                        "is_required": table_name in required_tables
                    })
            
            return {
                "status": "success",
                "connected": True,
                "database_healthy": len(missing_tables) == 0,
                "total_tables": len(table_names),
                "required_tables": {
                    "total": len(required_tables),
                    "existing": len(existing_required),
                    "missing": missing_tables
                },
                "tables": table_details,
                "timestamp": "now"
            }
            
    except Exception as e:
        logger.exception("Database status check failed")
        return {
            "status": "error",
            "connected": False,
            "error": str(e),
            "timestamp": "now"
        }


@router.get("/tables")
async def list_tables(
    current_user: User = Depends(get_current_active_superuser)
) -> Dict[str, Any]:
    """
    List all database tables with detailed information.
    """
    try:
        db_service = DatabaseService()
        
        async with db_service.get_session() as session:
            connection = session.connection()
            inspector = inspect(connection)
            
            table_names = inspector.get_table_names()
            tables_info = []
            
            for table_name in sorted(table_names):
                try:
                    columns = inspector.get_columns(table_name)
                    pk_constraint = inspector.get_pk_constraint(table_name)
                    foreign_keys = inspector.get_foreign_keys(table_name)
                    indexes = inspector.get_indexes(table_name)
                    
                    # Get row count
                    try:
                        result = await session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                        row_count = result.scalar()
                    except Exception:
                        row_count = None
                    
                    tables_info.append({
                        "name": table_name,
                        "columns": [{"name": col["name"], "type": str(col["type"])} for col in columns],
                        "column_count": len(columns),
                        "primary_key": pk_constraint.get('constrained_columns', []),
                        "foreign_keys": len(foreign_keys),
                        "indexes": len(indexes),
                        "row_count": row_count
                    })
                    
                except Exception as e:
                    logger.warning(f"Error getting info for table {table_name}: {e}")
                    tables_info.append({
                        "name": table_name,
                        "error": str(e)
                    })
            
            return {
                "status": "success",
                "total_tables": len(table_names),
                "tables": tables_info
            }
            
    except Exception as e:
        logger.exception("Failed to list tables")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list tables: {str(e)}"
        )


@router.post("/create-tables")
async def create_missing_tables(
    current_user: User = Depends(get_current_active_superuser)
) -> Dict[str, Any]:
    """
    Create missing database tables automatically.
    """
    try:
        db_service = DatabaseService()
        
        # Get current state
        async with db_service.get_session() as session:
            connection = session.connection()
            inspector = inspect(connection)
            tables_before = set(inspector.get_table_names())
        
        # Create tables
        await db_service.create_db_and_tables()
        
        # Get new state
        async with db_service.get_session() as session:
            connection = session.connection()
            inspector = inspect(connection)
            tables_after = set(inspector.get_table_names())
        
        created_tables = list(tables_after - tables_before)
        
        return {
            "status": "success",
            "message": "Table creation completed",
            "tables_before": len(tables_before),
            "tables_after": len(tables_after),
            "created_tables": created_tables,
            "created_count": len(created_tables)
        }
        
    except Exception as e:
        logger.exception("Table creation failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create tables: {str(e)}"
        )


@router.post("/migrate")
async def run_migration(
    current_user: User = Depends(get_current_active_superuser)
) -> Dict[str, Any]:
    """
    Run database migration using Alembic.
    """
    try:
        db_service = DatabaseService()
        
        # Run migration
        await db_service.run_migrations()
        
        return {
            "status": "success",
            "message": "Database migration completed successfully"
        }
        
    except Exception as e:
        logger.exception("Migration failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Migration failed: {str(e)}"
        )


@router.get("/health")
async def database_health_check(
    current_user: User = Depends(get_current_active_superuser)
) -> Dict[str, Any]:
    """
    Perform comprehensive database health check.
    """
    try:
        db_service = DatabaseService()
        health_status = {
            "status": "healthy",
            "checks": {},
            "timestamp": "now"
        }
        
        # Test connection
        try:
            async with db_service.get_session() as session:
                await session.execute(text("SELECT 1"))
                health_status["checks"]["connection"] = {"status": "ok", "message": "Database connection successful"}
        except Exception as e:
            health_status["checks"]["connection"] = {"status": "error", "message": str(e)}
            health_status["status"] = "unhealthy"
        
        # Check required tables
        try:
            async with db_service.get_session() as session:
                connection = session.connection()
                inspector = inspect(connection)
                table_names = inspector.get_table_names()
                required_tables = ["flow", "user", "apikey", "folder", "message", "variable", "transaction", "vertex_build"]
                missing_tables = [t for t in required_tables if t not in table_names]
                
                if not missing_tables:
                    health_status["checks"]["tables"] = {"status": "ok", "message": "All required tables exist"}
                else:
                    health_status["checks"]["tables"] = {
                        "status": "warning", 
                        "message": f"Missing tables: {', '.join(missing_tables)}"
                    }
                    if health_status["status"] == "healthy":
                        health_status["status"] = "degraded"
        except Exception as e:
            health_status["checks"]["tables"] = {"status": "error", "message": str(e)}
            health_status["status"] = "unhealthy"
        
        # Test basic operations
        try:
            async with db_service.get_session() as session:
                # Try to query user table
                result = await session.execute(text("SELECT COUNT(*) FROM user"))
                user_count = result.scalar()
                health_status["checks"]["operations"] = {
                    "status": "ok", 
                    "message": f"Basic operations working, {user_count} users"
                }
        except Exception as e:
            health_status["checks"]["operations"] = {"status": "error", "message": str(e)}
            health_status["status"] = "unhealthy"
        
        return health_status
        
    except Exception as e:
        logger.exception("Health check failed")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "now"
        }


@router.get("/migration-status")
async def get_migration_status(
    current_user: User = Depends(get_current_active_superuser)
) -> Dict[str, Any]:
    """
    Get current migration status and version information.
    """
    try:
        db_service = DatabaseService()
        
        async with db_service.get_session() as session:
            # Check if alembic_version table exists
            connection = session.connection()
            inspector = inspect(connection)
            table_names = inspector.get_table_names()
            
            if "alembic_version" not in table_names:
                return {
                    "status": "no_migration_table",
                    "message": "Alembic version table not found",
                    "current_version": None
                }
            
            # Get current version
            try:
                result = await session.execute(text("SELECT version_num FROM alembic_version"))
                current_version = result.scalar()
                
                return {
                    "status": "success",
                    "current_version": current_version,
                    "migration_table_exists": True
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to read migration version: {str(e)}",
                    "migration_table_exists": True
                }
        
    except Exception as e:
        logger.exception("Failed to get migration status")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get migration status: {str(e)}"
        )
