#!/usr/bin/env python3
"""
Test .env file loading
"""
import os
from dotenv import load_dotenv

print("🔧 Current working directory:", os.getcwd())
print("🔧 .env file exists:", os.path.exists('.env'))

if os.path.exists('.env'):
    with open('.env', 'r') as f:
        content = f.read()
        print("🔧 .env file content (first 200 chars):")
        print(content[:200])

print("\n🔧 Loading .env file...")
result = load_dotenv(override=True)
print("🔧 load_dotenv result:", result)

print("\n🔧 Environment variables after loading:")
for key in ['AXIESTUDIO_DATABASE_URL', 'AXIESTUDIO_SUPERUSER', 'AXIESTUDIO_EMAIL_SMTP_HOST']:
    value = os.getenv(key)
    if value:
        print(f"  {key}: {value[:50]}...")
    else:
        print(f"  {key}: NOT SET")
