#!/usr/bin/env python3
"""
🗄️ AxieStudio Database Administration Tool

Enhanced CLI tool for managing AxieStudio database operations including
automatic table creation, migration management, and health monitoring.

Usage:
    python database_admin.py status          # Show database status
    python database_admin.py create-tables   # Create missing tables
    python database_admin.py migrate         # Run full migration
    python database_admin.py health          # Health check
    python database_admin.py list-tables     # List all tables
    python database_admin.py help            # Show this help
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.logging import RichHandler

# Add the backend to the path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

try:
    from axiestudio.services.database.service import DatabaseService
    from axiestudio.services.settings import settings
    from sqlalchemy import inspect, text
    from sqlmodel import SQLModel
except ImportError as e:
    print(f"❌ Error importing AxieStudio modules: {e}")
    print("🔧 Make sure you're running this from the AxieStudio root directory")
    sys.exit(1)

# Setup rich console and logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)
logger = logging.getLogger("database_admin")


class DatabaseAdmin:
    """Enhanced database administration tool"""
    
    def __init__(self):
        self.db_service = DatabaseService()
    
    async def show_status(self) -> None:
        """Show comprehensive database status"""
        console.print(Panel.fit("🗄️ AxieStudio Database Status", style="bold blue"))
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Connecting to database...", total=None)
                
                # Get database connection
                async with self.db_service.get_session() as session:
                    connection = session.connection()
                    inspector = inspect(connection)
                    
                    progress.update(task, description="Analyzing database structure...")
                    
                    # Get table information
                    table_names = inspector.get_table_names()
                    required_tables = ["flow", "user", "apikey", "folder", "message", "variable", "transaction", "vertex_build"]
                    
                    # Create status table
                    table = Table(title="📊 Database Tables Status")
                    table.add_column("Table Name", style="cyan")
                    table.add_column("Status", style="green")
                    table.add_column("Row Count", style="yellow")
                    
                    for table_name in required_tables:
                        if table_name in table_names:
                            try:
                                result = await session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                                count = result.scalar()
                                table.add_row(table_name, "✅ Exists", str(count))
                            except Exception:
                                table.add_row(table_name, "✅ Exists", "N/A")
                        else:
                            table.add_row(table_name, "❌ Missing", "0")
                    
                    console.print(table)
                    
                    # Summary
                    existing_count = len([t for t in required_tables if t in table_names])
                    console.print(f"\n📈 Summary: {existing_count}/{len(required_tables)} required tables exist")
                    console.print(f"🗂️ Total tables in database: {len(table_names)}")
                    
                    if existing_count == len(required_tables):
                        console.print("✅ Database is fully configured!", style="bold green")
                    else:
                        console.print("⚠️ Some tables are missing. Run 'create-tables' to fix.", style="bold yellow")
                        
        except Exception as e:
            console.print(f"❌ Error checking database status: {e}", style="bold red")
            logger.exception("Database status check failed")
    
    async def create_tables(self) -> None:
        """Create missing database tables"""
        console.print(Panel.fit("🔧 Creating Database Tables", style="bold green"))
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Initializing database...", total=None)
                
                await self.db_service.create_db_and_tables()
                
                progress.update(task, description="✅ Database tables created successfully!")
                
            console.print("🎉 Database table creation completed!", style="bold green")
            
        except Exception as e:
            console.print(f"❌ Error creating tables: {e}", style="bold red")
            logger.exception("Table creation failed")
    
    async def run_migration(self) -> None:
        """Run database migration"""
        console.print(Panel.fit("🔄 Running Database Migration", style="bold blue"))
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Running migration...", total=None)
                
                # Run the migration
                await self.db_service.run_migrations()
                
                progress.update(task, description="✅ Migration completed successfully!")
                
            console.print("🎉 Database migration completed!", style="bold green")
            
        except Exception as e:
            console.print(f"❌ Error running migration: {e}", style="bold red")
            logger.exception("Migration failed")
    
    async def health_check(self) -> None:
        """Perform comprehensive health check"""
        console.print(Panel.fit("🏥 Database Health Check", style="bold magenta"))
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Performing health check...", total=None)
                
                # Test database connection
                async with self.db_service.get_session() as session:
                    # Test basic query
                    result = await session.execute(text("SELECT 1"))
                    if result.scalar() == 1:
                        console.print("✅ Database connection: OK", style="green")
                    
                    # Check table integrity
                    connection = session.connection()
                    inspector = inspect(connection)
                    table_names = inspector.get_table_names()
                    
                    required_tables = ["flow", "user", "apikey", "folder", "message", "variable", "transaction", "vertex_build"]
                    missing_tables = [t for t in required_tables if t not in table_names]
                    
                    if not missing_tables:
                        console.print("✅ Table integrity: OK", style="green")
                    else:
                        console.print(f"⚠️ Missing tables: {', '.join(missing_tables)}", style="yellow")
                    
                    progress.update(task, description="✅ Health check completed!")
                
            console.print("🎉 Database health check completed!", style="bold green")
            
        except Exception as e:
            console.print(f"❌ Health check failed: {e}", style="bold red")
            logger.exception("Health check failed")
    
    async def list_tables(self) -> None:
        """List all database tables with details"""
        console.print(Panel.fit("📋 Database Tables", style="bold cyan"))
        
        try:
            async with self.db_service.get_session() as session:
                connection = session.connection()
                inspector = inspect(connection)
                table_names = sorted(inspector.get_table_names())
                
                if not table_names:
                    console.print("📭 No tables found in database", style="yellow")
                    return
                
                table = Table(title=f"📊 Database Tables ({len(table_names)} total)")
                table.add_column("Table Name", style="cyan")
                table.add_column("Columns", style="green")
                table.add_column("Primary Key", style="yellow")
                
                for table_name in table_names:
                    try:
                        columns = inspector.get_columns(table_name)
                        pk_columns = inspector.get_pk_constraint(table_name)
                        
                        column_count = len(columns)
                        pk_info = ", ".join(pk_columns.get('constrained_columns', [])) if pk_columns else "None"
                        
                        table.add_row(table_name, str(column_count), pk_info)
                    except Exception:
                        table.add_row(table_name, "Error", "Error")
                
                console.print(table)
                
        except Exception as e:
            console.print(f"❌ Error listing tables: {e}", style="bold red")
            logger.exception("Table listing failed")


def show_help():
    """Show help information"""
    help_text = """
🗄️ AxieStudio Database Administration Tool

Available Commands:
  status          Show database status and table information
  create-tables   Create missing database tables automatically
  migrate         Run database migration with Alembic
  health          Perform comprehensive database health check
  list-tables     List all tables with column information
  help            Show this help message

Examples:
  python database_admin.py status
  python database_admin.py create-tables
  python database_admin.py health

For more information, visit: https://github.com/axiestudio/axiestudio
"""
    console.print(Panel(help_text, title="Help", style="bold blue"))


async def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    admin = DatabaseAdmin()
    
    try:
        if command == "status":
            await admin.show_status()
        elif command == "create-tables":
            await admin.create_tables()
        elif command == "migrate":
            await admin.run_migration()
        elif command == "health":
            await admin.health_check()
        elif command == "list-tables":
            await admin.list_tables()
        elif command == "help":
            show_help()
        else:
            console.print(f"❌ Unknown command: {command}", style="bold red")
            console.print("💡 Use 'help' to see available commands")
    
    except KeyboardInterrupt:
        console.print("\n⏹️ Operation cancelled by user", style="yellow")
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}", style="bold red")
        logger.exception("Unexpected error occurred")


if __name__ == "__main__":
    asyncio.run(main())
