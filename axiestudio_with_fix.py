#!/usr/bin/env python3
"""
AxieStudio Startup Script with Email Fix
This script starts AxieStudio with the email verification fix applied.
"""

import sys
import os
from pathlib import Path

# Apply the email fix before starting AxieStudio
def apply_email_fix():
    """Apply the email verification fix."""
    try:
        print("🔧 Applying email verification fix...")
        
        # Import and apply the patch
        import email_service_patch
        
        print("✅ Email verification fix applied successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to apply email fix: {e}")
        return False

def main():
    """Main startup function."""
    print("🚀 Starting AxieStudio with Email Fix")
    print("=" * 50)
    
    # Apply the email fix first
    if not apply_email_fix():
        print("⚠️ Email fix failed, but continuing with startup...")
    
    # Start AxieStudio normally
    print("🚀 Starting AxieStudio...")
    
    try:
        # Import and run AxieStudio
        from axiestudio.__main__ import main as axiestudio_main
        axiestudio_main()
        
    except Exception as e:
        print(f"❌ Failed to start AxieStudio: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
