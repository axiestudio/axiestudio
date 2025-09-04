#!/usr/bin/env python3
"""
Start Axie Studio with environment variables loaded from .env file
"""
import os
import sys
import asyncio
import platform
from dotenv import load_dotenv

# Fix Windows async event loop issue for PostgreSQL
if platform.system() == "Windows":
    print("🔧 Setting Windows-compatible event loop policy...")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables from .env file
print("🔧 Loading environment variables from .env file...")
load_dotenv(override=True)

# Print loaded environment variables for debugging
db_url = os.getenv('AXIESTUDIO_DATABASE_URL')
superuser = os.getenv('AXIESTUDIO_SUPERUSER')
smtp_host = os.getenv('AXIESTUDIO_EMAIL_SMTP_HOST')

print(f"AXIESTUDIO_DATABASE_URL: {'✅ SET' if db_url else '❌ NOT SET'}")
if db_url:
    print(f"  Database: {db_url[:50]}...")
print(f"AXIESTUDIO_SUPERUSER: {superuser if superuser else '❌ NOT SET'}")
print(f"AXIESTUDIO_EMAIL_SMTP_HOST: {'✅ SET' if smtp_host else '❌ NOT SET'}")

# Import and run axiestudio
if __name__ == "__main__":
    # Add the run command to sys.argv
    sys.argv = ["axiestudio", "run"]

    # Import and run axiestudio
    from axiestudio.__main__ import main
    main()
