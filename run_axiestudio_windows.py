#!/usr/bin/env python3
"""
Windows-compatible runner for AxieStudio that fixes the ProactorEventLoop issue.

This script sets the correct event loop policy for Windows to work with psycopg.
"""

import asyncio
import selectors
import sys
import os
from pathlib import Path

def setup_windows_event_loop():
    """Set up SelectorEventLoop for Windows compatibility with psycopg."""
    if sys.platform == "win32":
        # Use SelectorEventLoop instead of ProactorEventLoop for psycopg compatibility
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        print("✅ Set Windows SelectorEventLoop policy for psycopg compatibility")

def main():
    """Main entry point."""
    # Set up the correct event loop for Windows
    setup_windows_event_loop()
    
    # Load environment variables from .env file
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print(f"📁 Loading environment from {env_file}")
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    # Import and run axiestudio after setting up the event loop
    try:
        import axiestudio.__main__ as axiestudio_main
        print("🚀 Starting AxieStudio with Windows-compatible event loop...")
        
        # Set default arguments if not provided
        if len(sys.argv) == 1:
            sys.argv.extend(["run", "--host", "0.0.0.0", "--port", "7860"])
        
        # Run the main application
        axiestudio_main.main()
        
    except ImportError as e:
        print(f"❌ Failed to import axiestudio: {e}")
        print("💡 Make sure axiestudio is installed: pip install -e .")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running AxieStudio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
