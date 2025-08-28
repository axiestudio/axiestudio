#!/usr/bin/env python3
"""
🧪 SIMPLE EMAIL CONFIGURATION TEST
Test script to verify Resend email configuration without dependencies
"""

import os
from pathlib import Path

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

def test_email_configuration():
    """Test email configuration values"""
    print("🧪 RESEND EMAIL CONFIGURATION TEST")
    print("=" * 50)
    
    # Load environment variables
    load_env_file()
    
    # Get email configuration values
    smtp_host = os.getenv("AXIESTUDIO_EMAIL_SMTP_HOST")
    smtp_port = os.getenv("AXIESTUDIO_EMAIL_SMTP_PORT")
    smtp_user = os.getenv("AXIESTUDIO_EMAIL_SMTP_USER")
    smtp_password = os.getenv("AXIESTUDIO_EMAIL_SMTP_PASSWORD")
    from_email = os.getenv("AXIESTUDIO_EMAIL_FROM_EMAIL")
    from_name = os.getenv("AXIESTUDIO_EMAIL_FROM_NAME")
    
    print("📧 Configuration Values:")
    print(f"  SMTP Host: {smtp_host}")
    print(f"  SMTP Port: {smtp_port}")
    print(f"  SMTP User: {smtp_user}")
    print(f"  SMTP Password: {'*' * len(smtp_password) if smtp_password else 'NOT SET'}")
    print(f"  From Email: {from_email}")
    print(f"  From Name: {from_name}")
    
    # Validation checks
    print("\n🔍 Validation Checks:")
    issues = []
    
    # Check SMTP Host
    if smtp_host != "smtp.resend.com":
        issues.append(f"SMTP Host should be 'smtp.resend.com', got '{smtp_host}'")
    else:
        print("  ✅ SMTP Host is correct")
    
    # Check SMTP Port
    if smtp_port != "587":
        issues.append(f"SMTP Port should be '587', got '{smtp_port}'")
    else:
        print("  ✅ SMTP Port is correct")
    
    # Check SMTP User
    if smtp_user != "resend":
        issues.append(f"SMTP User should be 'resend', got '{smtp_user}'")
    else:
        print("  ✅ SMTP User is correct")
    
    # Check SMTP Password
    if not smtp_password or len(smtp_password) < 10:
        issues.append("SMTP Password appears to be missing or too short")
    else:
        print("  ✅ SMTP Password is set")
    
    # Check From Email
    if not from_email:
        issues.append("FROM_EMAIL is not set")
    elif "@" not in from_email:
        issues.append(f"FROM_EMAIL '{from_email}' is not a valid email address")
    elif from_email == "resend":
        issues.append("FROM_EMAIL is set to 'resend' which is invalid - this was the bug!")
    else:
        print(f"  ✅ From Email is valid: {from_email}")
    
    # Check From Name
    if not from_name:
        issues.append("FROM_NAME is not set")
    else:
        print(f"  ✅ From Name is set: {from_name}")
    
    # Summary
    print("\n" + "=" * 50)
    if issues:
        print("❌ CONFIGURATION ISSUES FOUND:")
        for issue in issues:
            print(f"  • {issue}")
        return False
    else:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Your Resend email configuration is correct!")
        print("\n📋 Summary:")
        print(f"  • Emails will be sent from: {from_email}")
        print(f"  • Display name: {from_name}")
        print(f"  • Using Resend SMTP: {smtp_host}:{smtp_port}")
        print("  • No more 'resend' fallback issues!")
        return True

def test_expert_fix():
    """Test that the expert's fix was applied correctly"""
    print("\n🔧 EXPERT FIX VERIFICATION:")
    print("=" * 50)
    
    from_email = os.getenv("AXIESTUDIO_EMAIL_FROM_EMAIL")
    smtp_user = os.getenv("AXIESTUDIO_EMAIL_SMTP_USER")
    
    print(f"FROM_EMAIL: {from_email}")
    print(f"SMTP_USER: {smtp_user}")
    
    if from_email == smtp_user:
        print("❌ PROBLEM: FROM_EMAIL equals SMTP_USER!")
        print("   This means the fallback is still being used.")
        return False
    elif from_email and "@" in from_email:
        print("✅ FIXED: FROM_EMAIL is a proper email address!")
        print("   The expert's fix has been applied correctly.")
        return True
    else:
        print("❌ PROBLEM: FROM_EMAIL is not set or invalid!")
        return False

if __name__ == "__main__":
    print("🚀 AXIE STUDIO RESEND EMAIL TEST")
    print("=" * 60)
    
    # Test configuration
    config_ok = test_email_configuration()
    
    # Test expert fix
    fix_ok = test_expert_fix()
    
    print("\n" + "=" * 60)
    if config_ok and fix_ok:
        print("🎉 SUCCESS! Your email configuration is ready for production!")
        print("📧 Resend emails should now work correctly.")
    else:
        print("💥 ISSUES FOUND! Please review the configuration.")
    print("=" * 60)
