#!/usr/bin/env python3
"""Test Supabase connection and create tables if needed."""

import os
from sqlalchemy import create_engine, text

def test_supabase_connection():
    """Test connection to Supabase and create basic tables."""
    
    # Your Supabase connection string
    supabase_url = "postgresql+psycopg2://postgres.fupxtdocoygjixlafjgz:STEfanjohn!12@aws-1-eu-north-1.pooler.supabase.com:6543/postgres?sslmode=require"
    
    print("🔍 Testing Supabase connection...")
    print(f"Database: postgres.fupxtdocoygjixlafjgz (eu-north-1)")
    
    try:
        # Create engine
        engine = create_engine(supabase_url)
        
        # Test connection
        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                print("✅ Supabase connection successful!")
                
                # Check existing tables
                tables_result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """))
                
                existing_tables = [row[0] for row in tables_result.fetchall()]
                print(f"📋 Existing tables: {existing_tables}")
                
                # Create a simple test table
                print("🔧 Creating test table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS axiestudio_test (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Insert test data
                conn.execute(text("""
                    INSERT INTO axiestudio_test (name) 
                    VALUES ('Test from Python script')
                    ON CONFLICT DO NOTHING
                """))
                
                # Commit the transaction
                conn.commit()
                
                print("✅ Test table created successfully!")
                print("🎉 Your Supabase database is working!")
                
                return True
                
            else:
                print("❌ Connection test failed")
                return False
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_supabase_connection()
