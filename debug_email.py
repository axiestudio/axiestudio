#!/usr/bin/env python3
"""
🔍 EMAIL DEBUG SCRIPT FOR AXIESTUDIO
This script helps diagnose email sending issues with Resend SMTP
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_env_file():
    """Load environment variables from .env file"""
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"📁 Loading environment from {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    else:
        print(f"⚠️  No .env file found at {env_file}")

def check_environment():
    """Check if all required environment variables are set"""
    print("\n🔍 CHECKING ENVIRONMENT VARIABLES:")
    print("=" * 50)
    
    required_vars = {
        "AXIESTUDIO_EMAIL_SMTP_HOST": os.getenv("AXIESTUDIO_EMAIL_SMTP_HOST"),
        "AXIESTUDIO_EMAIL_SMTP_PORT": os.getenv("AXIESTUDIO_EMAIL_SMTP_PORT"),
        "AXIESTUDIO_EMAIL_SMTP_USER": os.getenv("AXIESTUDIO_EMAIL_SMTP_USER"),
        "AXIESTUDIO_EMAIL_SMTP_PASSWORD": os.getenv("AXIESTUDIO_EMAIL_SMTP_PASSWORD"),
        "AXIESTUDIO_EMAIL_FROM_EMAIL": os.getenv("AXIESTUDIO_EMAIL_FROM_EMAIL"),
    }
    
    issues = []
    for var, value in required_vars.items():
        if value:
            if "PASSWORD" in var:
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
            issues.append(var)
    
    return len(issues) == 0, issues

def test_smtp_connection():
    """Test SMTP connection to Resend"""
    print("\n🔌 TESTING SMTP CONNECTION:")
    print("=" * 50)
    
    smtp_host = os.getenv("AXIESTUDIO_EMAIL_SMTP_HOST")
    smtp_port = int(os.getenv("AXIESTUDIO_EMAIL_SMTP_PORT", "587"))
    smtp_user = os.getenv("AXIESTUDIO_EMAIL_SMTP_USER")
    smtp_password = os.getenv("AXIESTUDIO_EMAIL_SMTP_PASSWORD")
    
    try:
        print(f"🔗 Connecting to {smtp_host}:{smtp_port}...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        
        print("🔐 Starting TLS...")
        server.starttls()
        
        print(f"🔑 Authenticating as {smtp_user}...")
        server.login(smtp_user, smtp_password)
        
        print("✅ SMTP connection successful!")
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication failed: {e}")
        print("💡 Check your SMTP username and password")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def send_test_email():
    """Send a test email"""
    print("\n📧 SENDING TEST EMAIL:")
    print("=" * 50)
    
    smtp_host = os.getenv("AXIESTUDIO_EMAIL_SMTP_HOST")
    smtp_port = int(os.getenv("AXIESTUDIO_EMAIL_SMTP_PORT", "587"))
    smtp_user = os.getenv("AXIESTUDIO_EMAIL_SMTP_USER")
    smtp_password = os.getenv("AXIESTUDIO_EMAIL_SMTP_PASSWORD")
    from_email = os.getenv("AXIESTUDIO_EMAIL_FROM_EMAIL")
    
    # Test email address
    to_email = "stefanjohnmiranda3@gmail.com"
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "AxieStudio Email Test"
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Create text and HTML parts
        text_body = """
AxieStudio Email Test

This is a test email to verify your email configuration is working.

If you received this email, your Resend SMTP setup is working correctly!

Test Details:
- SMTP Host: smtp.resend.com
- From: noreply@axiestudio.se
- Configuration: Working ✅
        """
        
        html_body = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AxieStudio Email Test</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <h2 style="color: #2563eb;">AxieStudio Email Test</h2>
    <p>This is a test email to verify your email configuration is working.</p>
    <div style="background-color: #dcfce7; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <p style="margin: 0; color: #166534;"><strong>✅ Success!</strong> If you received this email, your Resend SMTP setup is working correctly!</p>
    </div>
    <h3>Test Details:</h3>
    <ul>
        <li>SMTP Host: smtp.resend.com</li>
        <li>From: noreply@axiestudio.se</li>
        <li>Configuration: Working ✅</li>
    </ul>
</body>
</html>
        """
        
        text_part = MIMEText(text_body, 'plain', 'utf-8')
        html_part = MIMEText(html_body, 'html', 'utf-8')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send email
        print(f"📤 Sending test email to {to_email}...")
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        print("✅ Test email sent successfully!")
        print(f"📬 Check {to_email} for the test email")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🔍 AXIESTUDIO EMAIL DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Load environment
    load_env_file()
    
    # Check environment variables
    env_ok, missing_vars = check_environment()
    if not env_ok:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Please set these variables in your .env file or environment")
        return False
    
    # Test SMTP connection
    if not test_smtp_connection():
        print("\n❌ SMTP connection failed")
        print("💡 Please check your Resend credentials")
        return False
    
    # Send test email
    if not send_test_email():
        print("\n❌ Test email failed")
        return False
    
    print("\n🎉 ALL TESTS PASSED!")
    print("✅ Your email configuration is working correctly")
    print("✅ AxieStudio should be able to send emails now")
    
    return True

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 60)
    if success:
        print("🎉 EMAIL DIAGNOSTIC COMPLETED SUCCESSFULLY!")
    else:
        print("💥 EMAIL DIAGNOSTIC FOUND ISSUES!")
        print("🔧 Please fix the issues above and try again")
    print("=" * 60)
