#!/usr/bin/env python3
"""
🧪 SIMPLE EMAIL TEST - Tests Resend SDK directly
"""

import os
import sys
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / ".env"
    
    if not env_path.exists():
        print('❌ .env file not found!')
        return False
    
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                value = value.strip('"\'')  # Remove quotes
                env_vars[key] = value
                os.environ[key] = value
    
    print('✅ Environment variables loaded from .env')
    return env_vars

def test_resend_sdk():
    """Test Resend SDK directly"""
    print("🚀 TESTING RESEND SDK DIRECTLY")
    print("=" * 50)
    
    # Load environment
    env_vars = load_env_file()
    if not env_vars:
        return False
    
    # Get configuration
    api_key = os.getenv('AXIESTUDIO_EMAIL_SMTP_PASSWORD')
    from_email = os.getenv('AXIESTUDIO_EMAIL_FROM_EMAIL')
    from_name = os.getenv('AXIESTUDIO_EMAIL_FROM_NAME', 'Axie Studio')
    
    print(f"📧 API Key: {api_key[:10]}..." if api_key else "❌ No API key")
    print(f"📧 From Email: {from_email}")
    print(f"📧 From Name: {from_name}")
    
    if not api_key or not from_email:
        print("❌ Missing required configuration")
        return False
    
    # Test Resend SDK
    try:
        print("\n🔧 Testing Resend SDK import...")
        import resend
        print("✅ Resend SDK imported successfully")
        
        # Configure API key
        resend.api_key = api_key
        print("✅ API key configured")
        
        # Prepare test email
        test_email = "stefanjohnmiranda5@gmail.com"
        params = {
            "from": f"{from_name} <{from_email}>",
            "to": [test_email],
            "subject": "🎉 AxieStudio Dual Email Test - Resend SDK",
            "html": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AxieStudio Email Test</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 8px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">🎉 Resend SDK Test Successful!</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0;">AxieStudio Dual Email System</p>
    </div>
    
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: #28a745; margin-top: 0;">✅ Test Results</h3>
        <ul style="color: #333;">
            <li>✅ Resend SDK: Working</li>
            <li>✅ API Key: Valid</li>
            <li>✅ Email Delivery: Successful</li>
            <li>✅ Dual System: Ready</li>
        </ul>
    </div>
    
    <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: #1976d2; margin-top: 0;">🚀 System Status</h3>
        <p><strong>Method:</strong> Resend Python SDK</p>
        <p><strong>From:</strong> """ + from_email + """</p>
        <p><strong>Test Time:</strong> """ + str(__import__('datetime').datetime.now()) + """</p>
    </div>
    
    <div style="text-align: center; color: #666; font-size: 14px;">
        <p>This email was sent using the Resend Python SDK to test AxieStudio's dual email system.</p>
        <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
    </div>
</body>
</html>
            """,
            "text": f"""
🎉 AXIESTUDIO DUAL EMAIL TEST - RESEND SDK

✅ Test Results:
- Resend SDK: Working
- API Key: Valid  
- Email Delivery: Successful
- Dual System: Ready

🚀 System Status:
Method: Resend Python SDK
From: {from_email}
Test Time: {__import__('datetime').datetime.now()}

This email was sent using the Resend Python SDK to test AxieStudio's dual email system.

AxieStudio - Building the future of AI workflows
            """
        }
        
        print(f"\n📤 Sending test email to {test_email}...")
        print(f"📧 From: {params['from']}")
        print(f"📧 Subject: {params['subject']}")
        
        # Send email
        response = resend.Emails.send(params)
        
        if response and hasattr(response, 'id'):
            print(f"✅ Email sent successfully!")
            print(f"📬 Message ID: {response.id}")
            print(f"📬 Check {test_email} for the test email")
            return True
        else:
            print(f"❌ Failed to send email - Invalid response: {response}")
            return False
            
    except ImportError:
        print("❌ Resend SDK not available - need to install: pip install resend")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 AXIESTUDIO RESEND SDK TEST")
    print("=" * 50)
    
    success = test_resend_sdk()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 RESEND SDK TEST PASSED!")
        print("✅ Your dual email system should work perfectly!")
    else:
        print("💥 RESEND SDK TEST FAILED!")
        print("🔧 Check the configuration and dependencies")
    print("=" * 50)

if __name__ == "__main__":
    main()
