#!/usr/bin/env python3
"""
Enhanced Auto Migration Manager for AxieStudio
Automatically creates database tables with proper conditional logic (if/else statements)
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

from axiestudio.services.deps import get_db_service
from sqlalchemy import text, inspect, MetaData
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger


class EnhancedAutoMigrationManager:
    """Enhanced automatic database migration manager with conditional logic."""
    
    def __init__(self):
        self.db_service = get_db_service()
        self.required_tables = [
            'user', 'flow', 'component', 'api_key', 'folder', 'message', 
            'transaction', 'vertex', 'edge', 'variable'
        ]
        
        # Email verification columns that should exist
        self.email_verification_columns = {
            'email_verified': 'BOOLEAN DEFAULT FALSE',
            'email_verification_token': 'VARCHAR',
            'email_verification_expires': 'TIMESTAMP',
            'verification_code': 'VARCHAR(6)',
            'verification_code_expires': 'TIMESTAMP',
            'verification_attempts': 'INTEGER DEFAULT 0 NOT NULL',
            'login_attempts': 'INTEGER DEFAULT 0',
            'locked_until': 'TIMESTAMP',
            'last_login_ip': 'VARCHAR',
            'password_changed_at': 'TIMESTAMP',
            'failed_login_attempts': 'INTEGER DEFAULT 0',
            'last_failed_login': 'TIMESTAMP'
        }
    
    async def check_database_status(self) -> Dict[str, Any]:
        """Check the current database status with conditional logic."""
        logger.info("🔍 Checking database status...")
        
        try:
            async with self.db_service.with_session() as session:
                # Check if database is accessible
                result = await session.exec(text("SELECT 1"))
                if not result.fetchone():
                    return {"status": "error", "message": "Database not accessible"}
                
                # Get table information
                inspector = inspect(session.get_bind())
                existing_tables = inspector.get_table_names()
                
                # Check missing tables
                missing_tables = []
                for table in self.required_tables:
                    if table not in existing_tables:
                        missing_tables.append(table)
                
                # Check user table columns if it exists
                user_column_status = {}
                if 'user' in existing_tables:
                    user_columns = inspector.get_columns('user')
                    existing_column_names = [col['name'] for col in user_columns]
                    
                    for col_name, col_def in self.email_verification_columns.items():
                        if col_name in existing_column_names:
                            user_column_status[col_name] = "exists"
                        else:
                            user_column_status[col_name] = "missing"
                
                return {
                    "status": "success",
                    "total_tables": len(existing_tables),
                    "existing_tables": existing_tables,
                    "missing_tables": missing_tables,
                    "user_column_status": user_column_status,
                    "database_accessible": True
                }
                
        except Exception as e:
            logger.error(f"❌ Database status check failed: {e}")
            return {"status": "error", "message": str(e)}
    
    async def auto_create_missing_tables(self) -> Dict[str, Any]:
        """Automatically create missing tables with conditional logic."""
        logger.info("🔧 Auto-creating missing tables...")
        
        status = await self.check_database_status()
        if status["status"] != "success":
            return {"success": False, "error": "Database status check failed"}
        
        missing_tables = status.get("missing_tables", [])
        created_tables = []
        errors = []
        
        if not missing_tables:
            logger.info("✅ No missing tables found")
            return {"success": True, "created_tables": [], "message": "No missing tables"}
        
        try:
            async with self.db_service.with_session() as session:
                # Use conditional logic to create tables
                for table_name in missing_tables:
                    try:
                        if table_name == "user":
                            # Create user table with all required columns
                            await self._create_user_table(session)
                        else:
                            # Create other tables using SQLModel metadata
                            await self._create_table_from_model(session, table_name)
                        
                        created_tables.append(table_name)
                        logger.info(f"✅ Created table: {table_name}")
                        
                    except Exception as e:
                        error_msg = f"Failed to create table {table_name}: {e}"
                        errors.append(error_msg)
                        logger.error(f"❌ {error_msg}")
                
                await session.commit()
                
        except Exception as e:
            logger.error(f"❌ Auto table creation failed: {e}")
            return {"success": False, "error": str(e)}
        
        return {
            "success": True,
            "created_tables": created_tables,
            "errors": errors,
            "message": f"Created {len(created_tables)} tables"
        }
    
    async def _create_user_table(self, session):
        """Create user table with all email verification columns."""
        logger.info("🔧 Creating user table with email verification columns...")
        
        # Check if table exists first
        table_exists_query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'user'
        );
        """
        
        result = await session.exec(text(table_exists_query))
        table_exists = result.fetchone()[0]
        
        if not table_exists:
            # Create the complete user table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                username VARCHAR NOT NULL UNIQUE,
                email VARCHAR,
                password VARCHAR NOT NULL,
                profile_image VARCHAR,
                is_active BOOLEAN DEFAULT TRUE,
                is_superuser BOOLEAN DEFAULT FALSE,
                create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login_at TIMESTAMP,
                signup_ip VARCHAR,
                device_fingerprint VARCHAR,
                email_verified BOOLEAN DEFAULT FALSE,
                email_verification_token VARCHAR,
                email_verification_expires TIMESTAMP,
                verification_code VARCHAR(6),
                verification_code_expires TIMESTAMP,
                verification_attempts INTEGER DEFAULT 0 NOT NULL,
                login_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP,
                last_login_ip VARCHAR,
                password_changed_at TIMESTAMP,
                failed_login_attempts INTEGER DEFAULT 0,
                last_failed_login TIMESTAMP,
                stripe_customer_id VARCHAR,
                subscription_status VARCHAR DEFAULT 'trial',
                subscription_id VARCHAR,
                trial_start TIMESTAMP,
                trial_end TIMESTAMP,
                subscription_start TIMESTAMP,
                subscription_end TIMESTAMP,
                store_api_key VARCHAR,
                optins JSONB
            );
            """
            
            await session.exec(text(create_table_sql))
            logger.info("✅ User table created successfully")
        else:
            logger.info("✅ User table already exists")
    
    async def _create_table_from_model(self, session, table_name: str):
        """Create table from SQLModel definition."""
        # This would use the actual SQLModel metadata to create tables
        # For now, we'll use the database service's built-in method
        await self.db_service.create_db_and_tables()
    
    async def fix_user_table_schema(self) -> Dict[str, Any]:
        """Fix user table schema issues with conditional logic."""
        logger.info("🔧 Fixing user table schema...")
        
        try:
            async with self.db_service.with_session() as session:
                fixes_applied = []
                
                # Check and fix verification_attempts column
                check_nullable_query = """
                SELECT is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'user' AND column_name = 'verification_attempts';
                """
                
                result = await session.exec(text(check_nullable_query))
                row = result.fetchone()
                
                if row and row[0] == 'YES':  # Column is nullable
                    # Fix NULL values first
                    await session.exec(text(
                        "UPDATE \"user\" SET verification_attempts = 0 WHERE verification_attempts IS NULL"
                    ))
                    
                    # Make column NOT NULL
                    await session.exec(text(
                        "ALTER TABLE \"user\" ALTER COLUMN verification_attempts SET NOT NULL"
                    ))
                    
                    fixes_applied.append("verification_attempts made NOT NULL")
                
                # Remove problematic indexes
                index_removal_queries = [
                    "DROP INDEX IF EXISTS ix_user_email_verification_token",
                    "DROP INDEX IF EXISTS ix_user_verification_code"
                ]
                
                for query in index_removal_queries:
                    try:
                        await session.exec(text(query))
                        fixes_applied.append(f"Removed index: {query.split()[-1]}")
                    except Exception as e:
                        logger.warning(f"Index removal warning: {e}")
                
                await session.commit()
                
                return {
                    "success": True,
                    "fixes_applied": fixes_applied,
                    "message": f"Applied {len(fixes_applied)} fixes"
                }
                
        except Exception as e:
            logger.error(f"❌ Schema fix failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def run_comprehensive_migration(self) -> Dict[str, Any]:
        """Run comprehensive migration with conditional logic."""
        logger.info("🚀 Running comprehensive database migration...")
        
        results = {
            "status_check": None,
            "table_creation": None,
            "schema_fixes": None,
            "overall_success": False
        }
        
        try:
            # Step 1: Check database status
            logger.info("📊 Step 1: Checking database status...")
            results["status_check"] = await self.check_database_status()
            
            if results["status_check"]["status"] != "success":
                return results
            
            # Step 2: Create missing tables
            logger.info("🔧 Step 2: Creating missing tables...")
            results["table_creation"] = await self.auto_create_missing_tables()
            
            # Step 3: Fix schema issues
            logger.info("🔧 Step 3: Fixing schema issues...")
            results["schema_fixes"] = await self.fix_user_table_schema()
            
            # Determine overall success
            results["overall_success"] = (
                results["status_check"]["status"] == "success" and
                results["table_creation"]["success"] and
                results["schema_fixes"]["success"]
            )
            
            if results["overall_success"]:
                logger.info("✅ Comprehensive migration completed successfully!")
            else:
                logger.warning("⚠️ Migration completed with some issues")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Comprehensive migration failed: {e}")
            results["error"] = str(e)
            return results


# Global instance
enhanced_auto_migration_manager = EnhancedAutoMigrationManager()


async def main():
    """Main function to run the enhanced migration."""
    print("🗄️ Enhanced Auto Migration Manager for AxieStudio")
    print("=" * 60)
    
    # Run comprehensive migration
    results = await enhanced_auto_migration_manager.run_comprehensive_migration()
    
    # Print results
    if results["overall_success"]:
        print("\n✅ MIGRATION SUCCESSFUL!")
        print("🎉 Database is ready for AxieStudio!")
    else:
        print("\n❌ MIGRATION ISSUES DETECTED")
        print("Please review the results above and fix any remaining issues.")
    
    return 0 if results["overall_success"] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
