#!/usr/bin/env python3
"""
🚀 DUAL EMAIL SYSTEM TEST
Tests both Resend SDK and SMTP fallback
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend" / "base"))

from axiestudio.services.email.service import EmailService, RESEND_SDK_AVAILABLE
from dotenv import load_dotenv

async def test_dual_email_system():
    """Test the dual email system"""
    print("🚀 TESTING DUAL EMAIL SYSTEM")
    print("=" * 60)
    
    # Load environment variables
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment from {env_path}")
    else:
        print("❌ No .env file found")
        return False
    
    # Initialize email service
    print("\n🔧 Initializing Email Service...")
    email_service = EmailService()
    
    # Test configuration
    print("\n📋 Testing Email Methods...")
    method_results = await email_service.test_email_methods()
    
    print(f"📧 Resend SDK Available: {method_results['resend_sdk']['available']}")
    print(f"📧 Resend SDK Configured: {method_results['resend_sdk']['configured']}")
    print(f"📧 SMTP Available: {method_results['smtp']['available']}")
    print(f"📧 SMTP Configured: {method_results['smtp']['configured']}")
    print(f"🎯 Preferred Method: {email_service.preferred_method.value}")
    
    # Health check
    print("\n🏥 Health Check...")
    health = await email_service.health_check()
    print(f"Status: {health['status']}")
    if health['issues']:
        print(f"Issues: {health['issues']}")
    
    # Test email sending
    test_email = "stefanjohnmiranda5@gmail.com"
    print(f"\n📤 Testing email send to {test_email}...")
    
    try:
        success = await email_service.send_verification_code_email(
            email=test_email,
            username="Stefan",
            verification_code="123456"
        )
        
        if success:
            print("✅ Email sent successfully!")
            print(f"📬 Check {test_email} for the test email")
            return True
        else:
            print("❌ Email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 AXIESTUDIO DUAL EMAIL SYSTEM TEST")
    print("=" * 60)
    
    success = await test_dual_email_system()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 DUAL EMAIL SYSTEM TEST PASSED!")
        print("✅ Your email system is working perfectly!")
    else:
        print("💥 DUAL EMAIL SYSTEM TEST FAILED!")
        print("🔧 Check the configuration and try again")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
