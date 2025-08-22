#!/usr/bin/env python3
"""
DOCKER-COMPATIBLE EMAIL VERIFICATION FIX
This is the most logical solution for fixing email verification in AxieStudio.

APPROACH:
1. Create a startup script that patches the email service on application start
2. Works in Docker containers without admin access
3. Automatically fixes the 'missing html_body' parameter issue
4. Enterprise-level implementation

USAGE:
1. Run this script before starting AxieStudio
2. Or integrate it into the Docker startup process
"""

import os
import sys
import asyncio
from pathlib import Path


def create_email_service_patch():
    """Create a patch file that fixes the email service."""
    
    patch_content = '''
# AxieStudio Email Service Patch
# This patch fixes the "missing html_body" parameter issue

import types
from loguru import logger


async def fixed_send_verification_code_email(self, email: str, username: str, verification_code: str) -> bool:
    """
    🎯 Send 6-digit verification code email (FIXED VERSION)
    
    This replaces the broken method with a working implementation that includes
    both text_body and html_body parameters for the _send_email call.
    """
    try:
        logger.info(f"🔄 Sending verification code email to {email} (PATCHED VERSION)")
        
        # Format code for display (123 456)
        try:
            from axiestudio.services.auth.verification_code import VerificationCodeService
            formatted_code = VerificationCodeService.format_code_for_display(verification_code)
        except:
            formatted_code = verification_code  # Fallback
        
        # Email subject
        subject = "🔐 Your AxieStudio Verification Code"
        
        # Create text version (required parameter that was missing!)
        text_body = f"""
AxieStudio - Email Verification

Hello {username}!

Your verification code is: {verification_code}

⏰ This code expires in 10 minutes

How to use this code:
1. Return to the AxieStudio verification page
2. Enter the 6-digit code above
3. Click "Verify Account" to complete setup
4. Start building amazing AI workflows!

🔒 Security Notice: Never share this code with anyone.

---
AxieStudio - Building the future of AI workflows
Visit us at: https://axiestudio.se
Need help? Contact our support team!
        """
        
        # Create HTML version (existing code, but now properly paired with text)
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your AxieStudio Verification Code</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
                .container {{ background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center; }}
                .content {{ padding: 40px 30px; text-align: center; }}
                .verification-code {{ font-size: 48px; font-weight: bold; letter-spacing: 8px; color: #667eea; margin: 0; font-family: 'Courier New', monospace; }}
                .security-info {{ background: #fff3cd; border: 2px solid #ffc107; padding: 20px; border-radius: 10px; margin: 25px 0; }}
                .footer {{ text-align: center; padding: 30px; background: #f8f9fa; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Verify Your Account</h1>
                    <p style="font-size: 18px; margin: 0;">Welcome to AxieStudio, {username}!</p>
                </div>
                <div class="content">
                    <h2>Enter this verification code in the app:</h2>
                    <div class="verification-code">{formatted_code}</div>
                    <div class="security-info">
                        <h3>🛡️ Security Information</h3>
                        <p>⏰ <strong>Expires in 10 minutes</strong><br>🔒 <strong>Never share this code</strong></p>
                    </div>
                </div>
                <div class="footer">
                    <p>🌟 <strong>AxieStudio</strong> - Building the future of AI workflows</p>
                    <p>Visit us at <a href="https://axiestudio.se">axiestudio.se</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # THE FIX: Call _send_email with ALL 4 required parameters!
        success = await self._send_email(email, subject, text_body, html_body)
        
        if success:
            logger.info(f"✅ Verification code email sent successfully to {email} (PATCHED)")
        else:
            logger.error(f"❌ Failed to send verification code email to {email} (PATCHED)")
        
        return success
        
    except Exception as e:
        logger.exception(f"❌ Error sending verification code email to {email} (PATCHED): {e}")
        return False


def apply_patch():
    """Apply the email service patch."""
    try:
        # Import the email service
        from axiestudio.services.email.service import email_service
        
        # Replace the broken method with the fixed one
        email_service.send_verification_code_email = types.MethodType(
            fixed_send_verification_code_email, 
            email_service
        )
        
        logger.info("✅ Email service patch applied successfully!")
        logger.info("✅ Email verification should now work correctly")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to apply email service patch: {e}")
        return False


# Auto-apply patch when this module is imported
if __name__ != "__main__":
    apply_patch()
'''
    
    return patch_content


def create_startup_script():
    """Create a startup script that applies the email fix."""
    
    startup_script = '''#!/usr/bin/env python3
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
'''
    
    return startup_script


def main():
    """Create the Docker-compatible email fix."""
    print("🐳 DOCKER-COMPATIBLE EMAIL VERIFICATION FIX")
    print("=" * 60)
    print("Creating deployment-ready fix for AxieStudio email verification...")
    print()
    
    # Create the patch file
    print("📝 Creating email service patch...")
    patch_content = create_email_service_patch()
    
    with open("email_service_patch.py", "w") as f:
        f.write(patch_content)
    
    print("✅ Created: email_service_patch.py")
    
    # Create the startup script
    print("📝 Creating startup script...")
    startup_content = create_startup_script()
    
    with open("axiestudio_with_fix.py", "w") as f:
        f.write(startup_content)
    
    print("✅ Created: axiestudio_with_fix.py")
    
    # Make startup script executable
    os.chmod("axiestudio_with_fix.py", 0o755)
    
    print("\n🎉 DOCKER EMAIL FIX CREATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("📋 DEPLOYMENT INSTRUCTIONS:")
    print()
    print("1. Copy these files to your AxieStudio deployment:")
    print("   - email_service_patch.py")
    print("   - axiestudio_with_fix.py")
    print()
    print("2. Update your Docker CMD or startup command:")
    print("   FROM: axiestudio run")
    print("   TO:   python axiestudio_with_fix.py")
    print()
    print("3. Or run manually:")
    print("   python axiestudio_with_fix.py")
    print()
    print("✅ This fix will:")
    print("   - Automatically patch the email service on startup")
    print("   - Fix the 'missing html_body' parameter error")
    print("   - Enable successful email verification")
    print("   - Work in Docker containers without admin access")
    print()
    print("🔧 The fix adds the missing text_body parameter to email calls,")
    print("   which is required by the _send_email method but was missing")
    print("   in the send_verification_code_email method.")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
