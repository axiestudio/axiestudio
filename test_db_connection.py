#!/usr/bin/env python3
"""
Test script to verify database connection before starting Axie Studio
"""
import os
import sys
from sqlalchemy import create_engine, text

def test_database_connection():
    """Test the database connection using the environment variable"""
    
    # Get database URL from environment
    db_url = os.getenv('AXIESTUDIO_DATABASE_URL')
    
    if not db_url:
        print("❌ AXIESTUDIO_DATABASE_URL not found in environment")
        return False
    
    print(f"🔍 Testing connection to: {db_url.split('@')[1] if '@' in db_url else 'database'}")
    
    try:
        # Create engine
        engine = create_engine(db_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                print("✅ Database connection successful!")
                
                # Test if we can create tables (basic permission check)
                try:
                    conn.execute(text("CREATE TABLE IF NOT EXISTS test_table (id INTEGER)"))
                    conn.execute(text("DROP TABLE IF EXISTS test_table"))
                    print("✅ Database permissions OK (can create/drop tables)")
                    conn.commit()
                except Exception as e:
                    print(f"⚠️  Database permissions limited: {e}")
                
                return True
            else:
                print("❌ Database connection failed - unexpected result")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Common error suggestions
        if "could not connect to server" in str(e).lower():
            print("💡 Suggestion: Check if the database server is running and accessible")
        elif "authentication failed" in str(e).lower():
            print("💡 Suggestion: Check username/password in the connection string")
        elif "database" in str(e).lower() and "does not exist" in str(e).lower():
            print("💡 Suggestion: Check if the database name is correct")
        elif "ssl" in str(e).lower():
            print("💡 Suggestion: Check SSL configuration (sslmode parameter)")
            
        return False

if __name__ == "__main__":
    print("🚀 Testing Axie Studio Database Connection")
    print("=" * 50)
    
    success = test_database_connection()
    
    if success:
        print("\n✅ Database test passed! You can proceed with starting Axie Studio.")
        sys.exit(0)
    else:
        print("\n❌ Database test failed! Fix the connection before starting Axie Studio.")
        sys.exit(1)
