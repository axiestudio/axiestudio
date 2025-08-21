#!/usr/bin/env python3
"""
Enhanced Database Migration Script for AxieStudio
Automatically handles database schema updates and table creation
"""

import asyncio
import sys
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

from axiestudio.services.database.auto_migration_manager import auto_migration_manager
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


async def run_enhanced_migration():
    """Run enhanced database migration with rich output."""
    
    console.print(Panel.fit("🗄️ AxieStudio Enhanced Database Migration", style="bold blue"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Step 1: Check current status
        task1 = progress.add_task("Checking database status...", total=None)
        try:
            db_info = await auto_migration_manager.get_database_info()
            migration_status = await auto_migration_manager.check_migration_status()
            progress.update(task1, description="✅ Database status checked")
        except Exception as e:
            progress.update(task1, description=f"❌ Status check failed: {e}")
            return False
        
        # Step 2: Show current state
        progress.stop()
        console.print("\n📊 Current Database State:")
        
        status_table = Table(show_header=True, header_style="bold magenta")
        status_table.add_column("Property", style="cyan")
        status_table.add_column("Value", style="green")
        
        status_table.add_row("Database Type", db_info.get("dialect", "Unknown"))
        status_table.add_row("Total Tables", str(db_info.get("table_count", 0)))
        status_table.add_row("Alembic Version", db_info.get("alembic_version", "Not initialized"))
        status_table.add_row("Migration Status", migration_status.get("migration_status", "Unknown"))
        
        console.print(status_table)
        
        # Step 3: Show tables
        if db_info.get("tables"):
            console.print("\n📋 Current Tables:")
            tables_table = Table(show_header=True, header_style="bold yellow")
            tables_table.add_column("Table Name", style="cyan")
            tables_table.add_column("Columns", justify="right", style="magenta")
            tables_table.add_column("Indexes", justify="right", style="blue")
            
            for table_name in sorted(db_info["tables"]):
                details = db_info.get("table_details", {}).get(table_name, {})
                tables_table.add_row(
                    table_name,
                    str(len(details.get("columns", []))),
                    str(len(details.get("indexes", [])))
                )
            
            console.print(tables_table)
        
        # Step 4: Run migration
        console.print(Panel.fit("🔄 Running Enhanced Migration Process", style="bold green"))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Create missing tables
            task2 = progress.add_task("Creating missing tables...", total=None)
            try:
                table_results = await auto_migration_manager.auto_create_missing_tables()
                created_count = len(table_results.get("created_tables", []))
                error_count = len(table_results.get("errors", []))
                
                if created_count > 0:
                    progress.update(task2, description=f"✅ Created {created_count} tables")
                else:
                    progress.update(task2, description="✅ No missing tables found")
                
                if error_count > 0:
                    progress.update(task2, description=f"⚠️ {error_count} errors during table creation")
                
            except Exception as e:
                progress.update(task2, description=f"❌ Table creation failed: {e}")
                return False
            
            # Run full migration
            task3 = progress.add_task("Running full migration...", total=None)
            try:
                migration_results = await auto_migration_manager.run_auto_migration(force=False)
                
                if migration_results.get("success"):
                    progress.update(task3, description="✅ Migration completed successfully")
                else:
                    error_count = len(migration_results.get("errors", []))
                    progress.update(task3, description=f"⚠️ Migration completed with {error_count} errors")
                
            except Exception as e:
                progress.update(task3, description=f"❌ Migration failed: {e}")
                return False
            
            # Verify final state
            task4 = progress.add_task("Verifying final state...", total=None)
            try:
                final_info = await auto_migration_manager.get_database_info()
                final_table_count = final_info.get("table_count", 0)
                progress.update(task4, description=f"✅ Verification complete: {final_table_count} tables")
            except Exception as e:
                progress.update(task4, description=f"❌ Verification failed: {e}")
                return False
        
        # Step 5: Show results
        console.print(Panel.fit("📊 Migration Results", style="bold cyan"))
        
        if table_results.get("created_tables"):
            console.print("✅ Created Tables:")
            for table in table_results["created_tables"]:
                console.print(f"  • [green]{table}[/green]")
        
        if table_results.get("errors"):
            console.print("\n❌ Errors:")
            for error in table_results["errors"]:
                console.print(f"  • [red]{error}[/red]")
        
        if migration_results.get("errors"):
            console.print("\n⚠️ Migration Errors:")
            for error in migration_results["errors"]:
                console.print(f"  • [yellow]{error}[/yellow]")
        
        # Step 6: Final summary
        final_table_count = final_info.get("table_count", 0)
        initial_table_count = db_info.get("table_count", 0)
        tables_added = final_table_count - initial_table_count
        
        console.print(f"\n🎉 Migration Summary:")
        console.print(f"  • Initial tables: {initial_table_count}")
        console.print(f"  • Final tables: {final_table_count}")
        console.print(f"  • Tables added: {tables_added}")
        
        success = (
            migration_results.get("success", False) and 
            len(table_results.get("errors", [])) == 0
        )
        
        if success:
            console.print(Panel.fit("🎉 Migration Completed Successfully!", style="bold green"))
        else:
            console.print(Panel.fit("⚠️ Migration Completed with Issues", style="bold yellow"))
        
        return success


async def show_database_status():
    """Show detailed database status."""
    console.print(Panel.fit("🗄️ AxieStudio Database Status", style="bold blue"))
    
    try:
        db_info = await auto_migration_manager.get_database_info()
        migration_status = await auto_migration_manager.check_migration_status()
        
        # Database info
        info_table = Table(title="Database Information", show_header=True, header_style="bold magenta")
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="green")
        
        info_table.add_row("Database Type", db_info.get("dialect", "Unknown"))
        info_table.add_row("Total Tables", str(db_info.get("table_count", 0)))
        info_table.add_row("Alembic Version", db_info.get("alembic_version", "Not initialized"))
        info_table.add_row("Migration Status", migration_status.get("migration_status", "Unknown"))
        
        console.print(info_table)
        
        # Tables info
        if db_info.get("tables"):
            console.print("\n📋 Database Tables:")
            tables_table = Table(show_header=True, header_style="bold yellow")
            tables_table.add_column("Table Name", style="cyan")
            tables_table.add_column("Columns", justify="right", style="magenta")
            tables_table.add_column("Indexes", justify="right", style="blue")
            tables_table.add_column("Foreign Keys", justify="right", style="green")
            
            for table_name in sorted(db_info["tables"]):
                details = db_info.get("table_details", {}).get(table_name, {})
                tables_table.add_row(
                    table_name,
                    str(len(details.get("columns", []))),
                    str(len(details.get("indexes", []))),
                    str(len(details.get("foreign_keys", [])))
                )
            
            console.print(tables_table)
        
        return True
        
    except Exception as e:
        console.print(f"[red]Error getting database status: {e}[/red]")
        return False


async def main():
    """Main function with command line interface."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            success = await show_database_status()
        elif command == "migrate":
            success = await run_enhanced_migration()
        elif command == "help":
            console.print("""
🗄️ AxieStudio Database Migration Script

Commands:
  status   - Show current database status
  migrate  - Run enhanced migration process
  help     - Show this help message

Examples:
  python database_migration_script.py status
  python database_migration_script.py migrate
            """)
            return 0
        else:
            console.print(f"[red]Unknown command: {command}[/red]")
            console.print("Use 'help' to see available commands")
            return 1
    else:
        # Default: run migration
        success = await run_enhanced_migration()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
