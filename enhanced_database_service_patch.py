#!/usr/bin/env python3
"""
Enhanced Database Service Patch for AxieStudio
Adds automatic database table creation with proper conditional logic (if/else statements)
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


class EnhancedDatabaseService:
    """Enhanced database service with automatic table creation and conditional logic."""
    
    def __init__(self):
        self.db_service = get_db_service()
        
        # Define required tables and their creation order
        self.required_tables = {
            'user': self._create_user_table_sql,
            'flow': self._create_flow_table_sql,
            'apikey': self._create_apikey_table_sql,
            'folder': self._create_folder_table_sql,
            'message': self._create_message_table_sql,
            'variable': self._create_variable_table_sql,
            'transaction': self._create_transaction_table_sql,
            'vertex_build': self._create_vertex_build_table_sql,
        }
        
        # Email verification columns with proper types
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
    
    async def auto_create_database_tables(self) -> Dict[str, Any]:
        """Automatically create database tables with conditional logic."""
        logger.info("🔧 Starting automatic database table creation...")
        
        results = {
            "success": False,
            "created_tables": [],
            "existing_tables": [],
            "errors": [],
            "total_tables": 0
        }
        
        try:
            async with self.db_service.with_session() as session:
                # Step 1: Check which tables exist
                inspector = inspect(session.get_bind())
                existing_tables = inspector.get_table_names()
                results["existing_tables"] = existing_tables
                results["total_tables"] = len(existing_tables)
                
                logger.info(f"📊 Found {len(existing_tables)} existing tables")
                
                # Step 2: Create missing tables with conditional logic
                for table_name, create_function in self.required_tables.items():
                    try:
                        if table_name in existing_tables:
                            logger.info(f"✅ Table '{table_name}' already exists - skipping")
                            continue
                        else:
                            logger.info(f"🔧 Creating table '{table_name}'...")
                            await create_function(session)
                            results["created_tables"].append(table_name)
                            logger.info(f"✅ Successfully created table '{table_name}'")
                    
                    except Exception as e:
                        error_msg = f"Failed to create table '{table_name}': {e}"
                        results["errors"].append(error_msg)
                        logger.error(f"❌ {error_msg}")
                
                # Step 3: Ensure user table has all required columns
                if 'user' in existing_tables or 'user' in results["created_tables"]:
                    await self._ensure_user_table_columns(session)
                
                await session.commit()
                
                # Determine success
                results["success"] = len(results["errors"]) == 0
                
                if results["success"]:
                    logger.info(f"✅ Database table creation completed! Created {len(results['created_tables'])} new tables")
                else:
                    logger.warning(f"⚠️ Database table creation completed with {len(results['errors'])} errors")
                
                return results
                
        except Exception as e:
            logger.error(f"❌ Auto table creation failed: {e}")
            results["errors"].append(str(e))
            return results
    
    async def _ensure_user_table_columns(self, session):
        """Ensure user table has all required email verification columns."""
        logger.info("🔧 Ensuring user table has all required columns...")
        
        try:
            # Get current columns
            inspector = inspect(session.get_bind())
            current_columns = [col['name'] for col in inspector.get_columns('user')]
            
            # Add missing columns with conditional logic
            for column_name, column_definition in self.email_verification_columns.items():
                if column_name not in current_columns:
                    logger.info(f"🔧 Adding missing column: {column_name}")
                    
                    add_column_sql = f'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS {column_name} {column_definition};'
                    await session.exec(text(add_column_sql))
                    
                    logger.info(f"✅ Added column: {column_name}")
                else:
                    logger.debug(f"✅ Column '{column_name}' already exists")
            
            # Fix specific issues
            await self._fix_user_table_issues(session)
            
        except Exception as e:
            logger.error(f"❌ Failed to ensure user table columns: {e}")
            raise
    
    async def _fix_user_table_issues(self, session):
        """Fix specific user table issues."""
        logger.info("🔧 Fixing user table schema issues...")
        
        try:
            # Fix 1: Make verification_attempts NOT NULL
            await session.exec(text(
                "UPDATE \"user\" SET verification_attempts = 0 WHERE verification_attempts IS NULL"
            ))
            await session.exec(text(
                "ALTER TABLE \"user\" ALTER COLUMN verification_attempts SET NOT NULL"
            ))
            logger.info("✅ Fixed verification_attempts column")
            
            # Fix 2: Remove problematic indexes
            problematic_indexes = [
                "ix_user_email_verification_token",
                "ix_user_verification_code"
            ]
            
            for index_name in problematic_indexes:
                try:
                    await session.exec(text(f"DROP INDEX IF EXISTS {index_name}"))
                    logger.info(f"✅ Removed problematic index: {index_name}")
                except Exception as e:
                    logger.warning(f"⚠️ Could not remove index {index_name}: {e}")
            
        except Exception as e:
            logger.warning(f"⚠️ Some user table fixes failed: {e}")
    
    def _create_user_table_sql(self, session):
        """Create user table with all required columns."""
        return session.exec(text("""
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
        """))
    
    def _create_flow_table_sql(self, session):
        """Create flow table."""
        return session.exec(text("""
            CREATE TABLE IF NOT EXISTS "flow" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR NOT NULL,
                description TEXT,
                data JSONB,
                is_component BOOLEAN DEFAULT FALSE,
                user_id INTEGER REFERENCES "user"(id),
                folder_id UUID,
                endpoint_name VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
    
    def _create_apikey_table_sql(self, session):
        """Create apikey table."""
        return session.exec(text("""
            CREATE TABLE IF NOT EXISTS "apikey" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR NOT NULL,
                api_key VARCHAR NOT NULL UNIQUE,
                user_id INTEGER REFERENCES "user"(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used_at TIMESTAMP,
                total_uses INTEGER DEFAULT 0
            );
        """))
    
    def _create_folder_table_sql(self, session):
        """Create folder table."""
        return session.exec(text("""
            CREATE TABLE IF NOT EXISTS "folder" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR NOT NULL,
                description TEXT,
                user_id INTEGER REFERENCES "user"(id),
                parent_id UUID REFERENCES "folder"(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
    
    def _create_message_table_sql(self, session):
        """Create message table."""
        return session.exec(text("""
            CREATE TABLE IF NOT EXISTS "message" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                text TEXT,
                sender VARCHAR,
                sender_name VARCHAR,
                session_id VARCHAR,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                flow_id UUID REFERENCES "flow"(id),
                files JSONB
            );
        """))
    
    def _create_variable_table_sql(self, session):
        """Create variable table."""
        return session.exec(text("""
            CREATE TABLE IF NOT EXISTS "variable" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR NOT NULL,
                value TEXT,
                type VARCHAR,
                user_id INTEGER REFERENCES "user"(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
    
    def _create_transaction_table_sql(self, session):
        """Create transaction table."""
        return session.exec(text("""
            CREATE TABLE IF NOT EXISTS "transaction" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                vertex_id VARCHAR,
                target_id VARCHAR,
                inputs JSONB,
                outputs JSONB,
                status VARCHAR,
                error TEXT,
                flow_id UUID REFERENCES "flow"(id)
            );
        """))
    
    def _create_vertex_build_table_sql(self, session):
        """Create vertex_build table."""
        return session.exec(text("""
            CREATE TABLE IF NOT EXISTS "vertex_build" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                flow_id UUID REFERENCES "flow"(id),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version VARCHAR,
                data JSONB,
                artifacts JSONB,
                status VARCHAR DEFAULT 'pending'
            );
        """))
    
    async def run_comprehensive_setup(self) -> Dict[str, Any]:
        """Run comprehensive database setup with conditional logic."""
        logger.info("🚀 Running comprehensive database setup...")
        
        results = {
            "table_creation": None,
            "schema_validation": None,
            "overall_success": False
        }
        
        try:
            # Step 1: Auto-create tables
            logger.info("📊 Step 1: Auto-creating database tables...")
            results["table_creation"] = await self.auto_create_database_tables()
            
            # Step 2: Validate schema
            logger.info("🔍 Step 2: Validating database schema...")
            results["schema_validation"] = await self._validate_database_schema()
            
            # Determine overall success
            results["overall_success"] = (
                results["table_creation"]["success"] and
                results["schema_validation"]["success"]
            )
            
            if results["overall_success"]:
                logger.info("✅ Comprehensive database setup completed successfully!")
            else:
                logger.warning("⚠️ Database setup completed with some issues")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Comprehensive database setup failed: {e}")
            results["error"] = str(e)
            return results
    
    async def _validate_database_schema(self) -> Dict[str, Any]:
        """Validate the database schema."""
        try:
            async with self.db_service.with_session() as session:
                inspector = inspect(session.get_bind())
                
                # Check all required tables exist
                existing_tables = inspector.get_table_names()
                missing_tables = [table for table in self.required_tables.keys() if table not in existing_tables]
                
                # Check user table columns
                user_column_issues = []
                if 'user' in existing_tables:
                    user_columns = [col['name'] for col in inspector.get_columns('user')]
                    for col_name in self.email_verification_columns.keys():
                        if col_name not in user_columns:
                            user_column_issues.append(f"Missing column: {col_name}")
                
                success = len(missing_tables) == 0 and len(user_column_issues) == 0
                
                return {
                    "success": success,
                    "existing_tables": existing_tables,
                    "missing_tables": missing_tables,
                    "user_column_issues": user_column_issues,
                    "total_tables": len(existing_tables)
                }
                
        except Exception as e:
            logger.error(f"❌ Schema validation failed: {e}")
            return {"success": False, "error": str(e)}


# Global instance
enhanced_db_service = EnhancedDatabaseService()


async def main():
    """Main function to run the enhanced database setup."""
    print("🗄️ Enhanced Database Service for AxieStudio")
    print("=" * 60)
    print("Automatic table creation with conditional logic (if/else statements)")
    print()
    
    # Run comprehensive setup
    results = await enhanced_db_service.run_comprehensive_setup()
    
    # Print results
    if results["overall_success"]:
        print("\n✅ DATABASE SETUP SUCCESSFUL!")
        print("🎉 All tables created and schema validated!")
        print("🚀 AxieStudio is ready to start!")
    else:
        print("\n❌ DATABASE SETUP ISSUES DETECTED")
        print("Please review the results above and fix any remaining issues.")
    
    return 0 if results["overall_success"] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
