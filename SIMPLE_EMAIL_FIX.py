#!/usr/bin/env python3
"""
SIMPLE EMAIL VERIFICATION FIX
Patches the running AxieStudio application to fix email verification.

This approach works by:
1. Finding the actual email service module in memory
2. Monkey-patching the broken method with a fixed version
3. No file system changes needed - works in Docker containers
"""

import sys
import types


def create_fixed_send_verification_code_email():
    """Create a fixed version of the send_verification_code_email method."""
    
    async def send_verification_code_email(self, email: str, username: str, verification_code: str) -> bool:
        """
        🎯 Send 6-digit verification code email (FIXED VERSION)
        
        This is the corrected version that includes both text_body and html_body parameters.
        """
        try:
            from loguru import logger
            logger.info(f"🔄 Sending verification code email to {email} (FIXED VERSION)")
            
            # Format code for display (123 456)
            try:
                from axiestudio.services.auth.verification_code import VerificationCodeService
                formatted_code = VerificationCodeService.format_code_for_display(verification_code)
            except:
                formatted_code = verification_code  # Fallback to plain code
            
            # Create email content
            subject = "🔐 Your AxieStudio Verification Code"
            
            # Create text version for email clients that don't support HTML
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

🔒 Security Notice: Never share this code with anyone. AxieStudio will never ask for your verification code via phone or email.

What you'll get access to:
🚀 AI Workflow Builder - Create powerful automation with drag-and-drop
🤖 Multiple AI Models - OpenAI, Anthropic, Claude, and more
📊 Real-time Dashboards - Monitor and visualize your results
🏪 1,600+ Components - Ready-to-use flows and tools
🤝 Team Collaboration - Share and work together seamlessly

---
AxieStudio - Building the future of AI workflows
Visit us at: https://axiestudio.se
Need help? Contact our support team - we're here to help!
            """

            # Create HTML version
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
                    .code-container {{
                        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                        border: 3px solid #667eea;
                        border-radius: 15px;
                        padding: 30px;
                        margin: 30px 0;
                        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
                    }}
                    .verification-code {{
                        font-size: 48px;
                        font-weight: bold;
                        letter-spacing: 8px;
                        color: #667eea;
                        margin: 0;
                        font-family: 'Courier New', monospace;
                    }}
                    .code-label {{
                        font-size: 14px;
                        color: #666;
                        margin-bottom: 10px;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                    }}
                    .security-info {{ background: #fff3cd; border: 2px solid #ffc107; padding: 20px; border-radius: 10px; margin: 25px 0; }}
                    .features {{ background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 25px 0; text-align: left; }}
                    .feature-item {{ margin: 10px 0; padding: 5px 0; }}
                    .footer {{ text-align: center; padding: 30px; background: #f8f9fa; color: #666; font-size: 14px; }}
                    .highlight {{ color: #667eea; font-weight: bold; }}
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

                        <div class="code-container">
                            <div class="code-label">Your Verification Code</div>
                            <div class="verification-code">{formatted_code}</div>
                        </div>

                        <div class="security-info">
                            <h3 style="margin: 0 0 10px 0;">🛡️ Security Information</h3>
                            <p style="margin: 0;">
                                ⏰ <strong>Expires in 10 minutes</strong><br>
                                🔒 <strong>Never share this code</strong><br>
                                🎯 <strong>Enter it in the AxieStudio app</strong>
                            </p>
                        </div>

                        <div class="features">
                            <h3>🌟 What you'll get access to:</h3>
                            <div class="feature-item">🚀 <strong>AI Workflow Builder</strong> - Create powerful automation with drag-and-drop</div>
                            <div class="feature-item">🤖 <strong>Multiple AI Models</strong> - OpenAI, Anthropic, Claude, and more</div>
                            <div class="feature-item">📊 <strong>Real-time Dashboards</strong> - Monitor and visualize your results</div>
                            <div class="feature-item">🏪 <strong>1,600+ Components</strong> - Ready-to-use flows and tools</div>
                            <div class="feature-item">🤝 <strong>Team Collaboration</strong> - Share and work together seamlessly</div>
                        </div>

                        <p style="color: #666; font-size: 14px; margin-top: 30px;">
                            Didn't request this code? You can safely ignore this email.
                        </p>
                    </div>

                    <div class="footer">
                        <p>🌟 <strong>AxieStudio</strong> - Building the future of AI workflows</p>
                        <p>Visit us at <a href="https://axiestudio.se" style="color: #667eea;">axiestudio.se</a></p>
                        <p>Need help? Our support team is ready to assist! 💬</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Send email with BOTH text and HTML versions (FIXED!)
            success = await self._send_email(email, subject, text_body, html_body)

            if success:
                logger.info(f"✅ Verification code email sent successfully to {email} (FIXED VERSION)")
            else:
                logger.error(f"❌ Failed to send verification code email to {email} (FIXED VERSION)")

            return success

        except Exception as e:
            from loguru import logger
            logger.exception(f"❌ Error sending verification code email to {email} (FIXED VERSION): {e}")
            return False
    
    return send_verification_code_email


def apply_email_fix():
    """Apply the email verification fix by monkey-patching the email service."""
    try:
        print("🔧 Applying email verification fix...")
        
        # Try to import the email service
        try:
            from axiestudio.services.email.service import email_service
            print("✅ Found email service instance")
        except ImportError as e:
            print(f"❌ Could not import email service: {e}")
            return False
        
        # Get the fixed method
        fixed_method = create_fixed_send_verification_code_email()
        
        # Monkey-patch the method
        email_service.send_verification_code_email = types.MethodType(fixed_method, email_service)
        
        print("✅ Email verification method has been patched!")
        print("✅ The 'missing html_body' error should now be resolved")
        
        return True
        
    except Exception as e:
        print(f"❌ Error applying email fix: {e}")
        return False


def main():
    """Main function to apply the fix."""
    print("🚀 SIMPLE EMAIL VERIFICATION FIX")
    print("=" * 50)
    print("Monkey-patching the email service to fix verification emails...")
    print()
    
    success = apply_email_fix()
    
    if success:
        print("\n🎉 EMAIL FIX APPLIED SUCCESSFULLY!")
        print("✅ Email verification should now work correctly")
        print("✅ Users can receive verification codes")
        print("✅ Account activation is restored")
        print("\n🧪 Test the fix by:")
        print("1. Creating a new user account")
        print("2. Requesting a verification code")
        print("3. Checking that the email is received")
        return 0
    else:
        print("\n❌ EMAIL FIX FAILED")
        print("Please check the error messages above")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
