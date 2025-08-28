#!/usr/bin/env python3
"""
🧪 EMAIL CONFIGURATION TEST
Test script to verify Resend email configuration is working correctly
"""

import os
import sys
from pathlib import Path

# Add the backend to Python path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

# Load environment variables from .env file manually
def load_env_file():
    """Load .env file manually"""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env_file()

def test_email_settings():
    """Test email settings configuration"""
    print("🧪 TESTING EMAIL CONFIGURATION")
    print("=" * 50)
    
    try:
        from axiestudio.services.settings.email import EmailSettings
        
        # Initialize email settings
        email_settings = EmailSettings()
        
        print("📧 Email Configuration:")
        print(f"  SMTP Host: {email_settings.SMTP_HOST}")
        print(f"  SMTP Port: {email_settings.SMTP_PORT}")
        print(f"  SMTP User: {email_settings.SMTP_USER}")
        print(f"  SMTP Password: {'*' * len(email_settings.SMTP_PASSWORD) if email_settings.SMTP_PASSWORD else 'NOT SET'}")
        print(f"  From Email: {email_settings.FROM_EMAIL}")
        print(f"  From Name: {email_settings.FROM_NAME}")
        print(f"  Email Enabled: {email_settings.EMAIL_ENABLED}")
        print(f"  Debug Mode: {email_settings.DEBUG_EMAIL}")
        
        print("\n🔍 Configuration Validation:")
        is_configured = email_settings.is_configured()
        print(f"  Is Configured: {is_configured}")
        
        if is_configured:
            print("✅ EMAIL CONFIGURATION IS VALID!")
            
            # Test SMTP configuration
            smtp_config = email_settings.get_smtp_config()
            print(f"\n📤 SMTP Config: {smtp_config}")
            
            # Test email configuration
            email_config = email_settings.get_email_config()
            print(f"📧 Email Config: {email_config}")
            
        else:
            print("❌ EMAIL CONFIGURATION IS INVALID!")
            
            # Check what's missing
            issues = []
            if not email_settings.SMTP_HOST:
                issues.append("SMTP_HOST not set")
            if not email_settings.SMTP_USER:
                issues.append("SMTP_USER not set")
            if not email_settings.SMTP_PASSWORD:
                issues.append("SMTP_PASSWORD not set")
            if not email_settings.FROM_EMAIL:
                issues.append("FROM_EMAIL not set")
            elif "@" not in email_settings.FROM_EMAIL:
                issues.append("FROM_EMAIL is not a valid email address")
                
            print(f"  Issues: {', '.join(issues)}")
        
        return is_configured
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_variables():
    """Test environment variables are loaded correctly"""
    print("\n🌍 ENVIRONMENT VARIABLES:")
    print("=" * 50)
    
    env_vars = [
        "AXIESTUDIO_EMAIL_FROM_EMAIL",
        "AXIESTUDIO_EMAIL_FROM_NAME", 
        "AXIESTUDIO_EMAIL_SMTP_HOST",
        "AXIESTUDIO_EMAIL_SMTP_PORT",
        "AXIESTUDIO_EMAIL_SMTP_USER",
        "AXIESTUDIO_EMAIL_SMTP_PASSWORD"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if var == "AXIESTUDIO_EMAIL_SMTP_PASSWORD":
            display_value = "*" * len(value) if value else "NOT SET"
        else:
            display_value = value or "NOT SET"
        print(f"  {var}: {display_value}")

if __name__ == "__main__":
    print("🚀 AXIE STUDIO EMAIL CONFIGURATION TEST")
    print("=" * 60)
    
    # Test environment variables
    test_environment_variables()
    
    # Test email settings
    success = test_email_settings()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! Email configuration is ready for Resend.")
    else:
        print("💥 TESTS FAILED! Please check your configuration.")
    print("=" * 60)
