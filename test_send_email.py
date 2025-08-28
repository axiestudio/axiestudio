#!/usr/bin/env python3
"""
📧 RESEND EMAIL SENDING TEST
Test script to send an actual email using Resend SMTP configuration
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime

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

def create_test_email(to_email: str):
    """Create a test email message"""

    # Get configuration
    from_email = os.getenv("AXIESTUDIO_EMAIL_FROM_EMAIL")
    from_name = os.getenv("AXIESTUDIO_EMAIL_FROM_NAME", "Axie Studio")

    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "🧪 Axie Studio Email Configuration Test"
    msg['From'] = f"{from_name} <{from_email}>"
    msg['To'] = to_email

    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Axie Studio Email Test</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2563eb;">🎉 Email Configuration Test Successful!</h1>
        </div>

        <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h2 style="color: #1e40af; margin-top: 0;">✅ Test Results</h2>
            <p><strong>✓ SMTP Configuration:</strong> Working correctly</p>
            <p><strong>✓ Resend Integration:</strong> Successfully connected</p>
            <p><strong>✓ Email Delivery:</strong> Message delivered</p>
            <p><strong>✓ From Address Fix:</strong> No more 'resend' fallback bug</p>
        </div>

        <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #059669; margin-top: 0;">📧 Configuration Details</h3>
            <p><strong>From:</strong> {from_email}</p>
            <p><strong>Display Name:</strong> {from_name}</p>
            <p><strong>SMTP Server:</strong> smtp.resend.com:587</p>
            <p><strong>Test Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div style="background-color: #fef3c7; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #d97706; margin-top: 0;">🔧 What Was Fixed</h3>
            <p><strong>Problem:</strong> FROM_EMAIL was falling back to 'resend' (invalid email)</p>
            <p><strong>Solution:</strong> Removed dangerous fallback, now uses proper email address</p>
            <p><strong>Result:</strong> Emails now send correctly from noreply@axiestudio.se</p>
        </div>

        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
            <p style="color: #6b7280; font-size: 14px;">
                This is an automated test email from Axie Studio<br>
                Sent via Resend SMTP • Configuration verified ✅
            </p>
        </div>
    </body>
    </html>
    """

    # Create plain text version
    text_content = f"""
🎉 AXIE STUDIO EMAIL CONFIGURATION TEST SUCCESSFUL!

✅ Test Results:
✓ SMTP Configuration: Working correctly
✓ Resend Integration: Successfully connected
✓ Email Delivery: Message delivered
✓ From Address Fix: No more 'resend' fallback bug

📧 Configuration Details:
From: {from_email}
Display Name: {from_name}
SMTP Server: smtp.resend.com:587
Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔧 What Was Fixed:
Problem: FROM_EMAIL was falling back to 'resend' (invalid email)
Solution: Removed dangerous fallback, now uses proper email address
Result: Emails now send correctly from noreply@axiestudio.se

This is an automated test email from Axie Studio
Sent via Resend SMTP • Configuration verified ✅
    """

    # Attach parts
    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    return msg

def send_test_email(to_email: str):
    """Send test email using Resend SMTP"""

    print(f"📧 SENDING TEST EMAIL TO: {to_email}")
    print("=" * 50)

    # Load environment variables
    load_env_file()

    # Get SMTP configuration
    smtp_host = os.getenv("AXIESTUDIO_EMAIL_SMTP_HOST")
    smtp_port = int(os.getenv("AXIESTUDIO_EMAIL_SMTP_PORT", "587"))
    smtp_user = os.getenv("AXIESTUDIO_EMAIL_SMTP_USER")
    smtp_password = os.getenv("AXIESTUDIO_EMAIL_SMTP_PASSWORD")
    from_email = os.getenv("AXIESTUDIO_EMAIL_FROM_EMAIL")

    print(f"🔧 SMTP Configuration:")
    print(f"  Host: {smtp_host}")
    print(f"  Port: {smtp_port}")
    print(f"  User: {smtp_user}")
    print(f"  From: {from_email}")
    print(f"  To: {to_email}")

    # Validate configuration
    if not all([smtp_host, smtp_port, smtp_user, smtp_password, from_email]):
        print("❌ ERROR: Missing SMTP configuration!")
        return False

    try:
        print("\n🚀 Creating email message...")
        msg = create_test_email(to_email)

        print("🔌 Connecting to SMTP server...")
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            print("🔐 Starting TLS encryption...")
            server.starttls()

            print("🔑 Authenticating with Resend...")
            server.login(smtp_user, smtp_password)

            print("📤 Sending email...")
            server.send_message(msg)

        print("\n🎉 SUCCESS! Email sent successfully!")
        print(f"✅ Test email delivered to {to_email}")
        print("✅ Resend SMTP configuration is working perfectly!")
        return True

    except Exception as e:
        print(f"\n❌ ERROR: Failed to send email!")
        print(f"Error details: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 AXIE STUDIO RESEND EMAIL SENDING TEST")
    print("=" * 60)

    # Test email address
    test_email = "stefanjohnmiranda3@gmail.com"

    # Send test email
    success = send_test_email(test_email)

    print("\n" + "=" * 60)
    if success:
        print("🎉 EMAIL TEST COMPLETED SUCCESSFULLY!")
        print("📧 Check your inbox for the test email.")
        print("✅ Your Resend configuration is working perfectly!")
    else:
        print("💥 EMAIL TEST FAILED!")
        print("🔧 Please check your configuration and try again.")
    print("=" * 60)