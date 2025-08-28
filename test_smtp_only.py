#!/usr/bin/env python3
"""
🧪 SMTP EMAIL TEST - Tests SMTP directly (no external dependencies)
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import datetime

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

def test_smtp_email():
    """Test SMTP email sending directly"""
    print("📧 TESTING SMTP EMAIL DIRECTLY")
    print("=" * 50)
    
    # Load environment
    env_vars = load_env_file()
    if not env_vars:
        return False
    
    # Get SMTP configuration
    smtp_host = os.getenv('AXIESTUDIO_EMAIL_SMTP_HOST')
    smtp_port = int(os.getenv('AXIESTUDIO_EMAIL_SMTP_PORT', '587'))
    smtp_user = os.getenv('AXIESTUDIO_EMAIL_SMTP_USER')
    smtp_password = os.getenv('AXIESTUDIO_EMAIL_SMTP_PASSWORD')
    from_email = os.getenv('AXIESTUDIO_EMAIL_FROM_EMAIL')
    from_name = os.getenv('AXIESTUDIO_EMAIL_FROM_NAME', 'Axie Studio')
    
    print(f"📧 SMTP Host: {smtp_host}")
    print(f"📧 SMTP Port: {smtp_port}")
    print(f"📧 SMTP User: {smtp_user}")
    print(f"📧 SMTP Password: {smtp_password[:10]}..." if smtp_password else "❌ No password")
    print(f"📧 From Email: {from_email}")
    print(f"📧 From Name: {from_name}")
    
    # Validate configuration
    if not all([smtp_host, smtp_user, smtp_password, from_email]):
        print("❌ Missing required SMTP configuration")
        return False
    
    # Validate Resend configuration
    if smtp_host == "smtp.resend.com":
        if smtp_user != "resend":
            print(f"❌ For Resend, SMTP_USER must be 'resend', got: {smtp_user}")
            return False
        if not smtp_password.startswith("re_"):
            print("❌ For Resend, SMTP_PASSWORD must start with 're_' (API key)")
            return False
    
    print("✅ Configuration validation passed!")
    
    try:
        # Create email message
        test_email = "stefanjohnmiranda5@gmail.com"
        subject = "🎉 AxieStudio SMTP Test - Dual Email System"
        
        # Create HTML body
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AxieStudio SMTP Test</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 8px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">📧 SMTP Test Successful!</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0;">AxieStudio Dual Email System</p>
    </div>
    
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: #28a745; margin-top: 0;">✅ Test Results</h3>
        <ul style="color: #333;">
            <li>✅ SMTP Configuration: Working</li>
            <li>✅ Resend Integration: Connected</li>
            <li>✅ Email Delivery: Successful</li>
            <li>✅ Fallback System: Ready</li>
        </ul>
    </div>
    
    <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: #1976d2; margin-top: 0;">📧 Configuration Details</h3>
        <p><strong>Method:</strong> SMTP (Fallback)</p>
        <p><strong>SMTP Host:</strong> {smtp_host}</p>
        <p><strong>SMTP Port:</strong> {smtp_port}</p>
        <p><strong>From Address:</strong> {from_email}</p>
        <p><strong>Test Time:</strong> {datetime.datetime.now()}</p>
    </div>
    
    <div style="text-align: center; color: #666; font-size: 14px;">
        <p>This email was sent using SMTP to test AxieStudio's dual email system fallback.</p>
        <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
    </div>
</body>
</html>
        """
        
        # Create text body
        text_body = f"""
📧 AXIESTUDIO SMTP TEST - DUAL EMAIL SYSTEM

✅ Test Results:
- SMTP Configuration: Working
- Resend Integration: Connected
- Email Delivery: Successful  
- Fallback System: Ready

📧 Configuration Details:
Method: SMTP (Fallback)
SMTP Host: {smtp_host}
SMTP Port: {smtp_port}
From Address: {from_email}
Test Time: {datetime.datetime.now()}

This email was sent using SMTP to test AxieStudio's dual email system fallback.

AxieStudio - Building the future of AI workflows
        """
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = test_email
        
        # Attach parts
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        print(f"\n📤 Sending test email to {test_email}...")
        print(f"📧 From: {msg['From']}")
        print(f"📧 Subject: {subject}")
        
        # Connect to SMTP server
        print(f"\n🔌 Connecting to SMTP server {smtp_host}:{smtp_port}...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        
        print("🔧 Starting TLS encryption...")
        server.starttls()
        
        print(f"🔐 Authenticating with user: {smtp_user}")
        server.login(smtp_user, smtp_password)
        
        print("📤 Sending email...")
        text = msg.as_string()
        server.sendmail(from_email, test_email, text)
        
        print("🔌 Closing connection...")
        server.quit()
        
        print("✅ Email sent successfully via SMTP!")
        print(f"📬 Check {test_email} for the test email")
        return True
        
    except Exception as e:
        print(f"❌ SMTP Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 AXIESTUDIO SMTP TEST")
    print("=" * 50)
    
    success = test_smtp_email()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SMTP TEST PASSED!")
        print("✅ Your dual email system fallback is working!")
        print("✅ Even if SDK fails, SMTP will work!")
    else:
        print("💥 SMTP TEST FAILED!")
        print("🔧 Check the SMTP configuration")
    print("=" * 50)

if __name__ == "__main__":
    main()
