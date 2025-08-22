import smtplib
import secrets
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from loguru import logger
from pydantic_settings import BaseSettings

from axiestudio.services.deps import get_settings_service


class EmailSettings(BaseSettings):
    """Email configuration settings."""
    SMTP_HOST: str = "smtp-relay.brevo.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = "noreply@axiestudio.se"
    FROM_NAME: str = "Axie Studio"

    class Config:
        env_prefix = "AXIESTUDIO_EMAIL_"


class EmailService:
    """
    Enterprise-grade email service using SMTP.

    Features:
    - 6-digit verification codes (enterprise standard)
    - Email verification links (legacy support)
    - Password reset emails
    - Comprehensive error handling
    - Security best practices
    - Both text and HTML email formats
    """

    def __init__(self):
        self.settings = EmailSettings()
        self._validate_configuration()

    def _validate_configuration(self) -> None:
        """Validate email configuration on startup."""
        try:
            if not self.settings.SMTP_HOST:
                logger.warning("⚠️ SMTP_HOST not configured - email functionality will be limited")

            if not self.settings.SMTP_USER or not self.settings.SMTP_PASSWORD:
                logger.warning("⚠️ SMTP credentials not configured - emails will fail to send")
                logger.info("🔧 Set AXIESTUDIO_EMAIL_SMTP_USER and AXIESTUDIO_EMAIL_SMTP_PASSWORD environment variables")

            if not self.settings.FROM_EMAIL or "@" not in self.settings.FROM_EMAIL:
                logger.warning(f"⚠️ Invalid FROM_EMAIL configured: {self.settings.FROM_EMAIL}")

            logger.info(f"📧 Email service initialized - SMTP: {self.settings.SMTP_HOST}:{self.settings.SMTP_PORT}")
            logger.info(f"📧 From: {self.settings.FROM_NAME} <{self.settings.FROM_EMAIL}>")

        except Exception as e:
            logger.error(f"❌ Email service configuration validation failed: {e}")

    async def health_check(self) -> dict:
        """
        Perform email service health check.

        Returns:
            dict: Health status with configuration details
        """
        try:
            health_status = {
                "service": "email",
                "status": "healthy",
                "smtp_host": self.settings.SMTP_HOST,
                "smtp_port": self.settings.SMTP_PORT,
                "from_email": self.settings.FROM_EMAIL,
                "credentials_configured": bool(self.settings.SMTP_USER and self.settings.SMTP_PASSWORD),
                "issues": []
            }

            # Check configuration issues
            if not self.settings.SMTP_USER or not self.settings.SMTP_PASSWORD:
                health_status["issues"].append("SMTP credentials not configured")
                health_status["status"] = "degraded"

            if not self.settings.FROM_EMAIL or "@" not in self.settings.FROM_EMAIL:
                health_status["issues"].append("Invalid FROM_EMAIL configuration")
                health_status["status"] = "degraded"

            # Test SMTP connection (optional - can be enabled for deeper health checks)
            # This is commented out to avoid unnecessary connections during health checks
            # try:
            #     with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
            #         server.starttls()
            #         server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
            #     health_status["smtp_connection"] = "successful"
            # except Exception as e:
            #     health_status["issues"].append(f"SMTP connection failed: {e}")
            #     health_status["status"] = "unhealthy"

            return health_status

        except Exception as e:
            logger.error(f"❌ Email service health check failed: {e}")
            return {
                "service": "email",
                "status": "unhealthy",
                "error": str(e)
            }
    
    def generate_verification_token(self) -> str:
        """Generate a secure verification token."""
        return secrets.token_urlsafe(32)
    
    def get_verification_expiry(self) -> datetime:
        """Get verification token expiry time (24 hours from now)."""
        return datetime.now(timezone.utc) + timedelta(hours=24)
    
    async def send_verification_code_email(self, email: str, username: str, verification_code: str) -> bool:
        """
        🎯 Send 6-digit verification code email (Enterprise approach)

        This replaces the old token-based verification with a modern
        6-digit code system used by Google, Microsoft, AWS, etc.
        """
        try:
            # Format code for display (123 456)
            from axiestudio.services.auth.verification_code import VerificationCodeService
            formatted_code = VerificationCodeService.format_code_for_display(verification_code)

            # Create email content
            subject = "🔐 Your AxieStudio Verification Code"

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

            # Send email with BOTH text and HTML versions (Enterprise standard)
            success = await self._send_email(email, subject, text_body, html_body)

            if success:
                logger.info(f"✅ Verification code email sent successfully to {email}")
            else:
                logger.error(f"❌ Failed to send verification code email to {email}")

            return success

        except Exception as e:
            logger.exception(f"❌ Error sending verification code email to {email}: {e}")
            return False

    async def send_verification_email(self, email: str, username: str, token: str) -> bool:
        """Send email verification email."""
        try:
            # Get frontend URL from settings
            settings_service = get_settings_service()
            frontend_url = getattr(settings_service.settings, 'frontend_url', 'https://flow.axiestudio.se')
            
            # Create verification link
            verification_link = f"{frontend_url}/verify-email?token={token}"
            
            # Create email content
            subject = "Verify your Axie Studio account"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Verify your Axie Studio account</title>
                <style>
                    .logo {{
                        width: 80px;
                        height: 80px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 16px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto 20px;
                        overflow: hidden;
                        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                        border: 3px solid rgba(255, 255, 255, 0.2);
                    }}
                    .logo img {{
                        width: 100%;
                        height: 100%;
                        object-fit: cover;
                        border-radius: 13px;
                    }}
                    .verify-btn {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 12px 30px;
                        text-decoration: none;
                        border-radius: 8px;
                        display: inline-block;
                        font-weight: bold;
                        margin: 20px 0;
                    }}
                    .footer {{
                        border-top: 1px solid #eee;
                        margin-top: 30px;
                        padding-top: 20px;
                        text-align: center;
                    }}
                </style>
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f8fafc;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Logo -->
                    <div class="logo">
                        <img src="https://scontent-arn2-1.xx.fbcdn.net/v/t39.30808-6/499498872_122132145854766980_5268724011023190696_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=u5dFev5AG-kQ7kNvwFS6K3m&_nc_oc=AdltILxg_X65VXBn-MK3Z58PgtgR7ITbbYcGrvZSWDnQLiIitDDiDq9uw1DoamQT61U&_nc_zt=23&_nc_ht=scontent-arn2-1.xx&_nc_gid=mpLb2UFdGIvVDUjGf2bZuw&oh=00_AfXfUa1TAFSuNwQPVCsbeshZuHKq0TqnRwUgl4EdrFju9w&oe=68A94B99" alt="Axie Studio Logo" />
                    </div>

                    <h2 style="color: #2563eb; margin-bottom: 20px;">Welcome to Axie Studio!</h2>

                    <p>Hi <strong>{username}</strong>,</p>

                    <p>🎉 Thank you for joining <strong>Axie Studio</strong> - the ultimate platform for building AI-powered workflows! To complete your registration and start creating amazing flows, please verify your email address by clicking the button below:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_link}" class="verify-btn">
                            ✨ Verify Email Address
                        </a>
                    </div>

                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #666; background-color: #f8fafc; padding: 10px; border-radius: 6px; font-family: monospace;">{verification_link}</p>

                    <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px; margin: 20px 0; border-radius: 6px;">
                        <p style="margin: 0; color: #92400e;"><strong>⏰ Important:</strong> This verification link will expire in 24 hours.</p>
                    </div>

                    <p>Once verified, you'll be able to:</p>
                    <ul style="color: #4b5563;">
                        <li>🚀 Create powerful AI workflows</li>
                        <li>🔗 Connect multiple AI models</li>
                        <li>📊 Build custom dashboards</li>
                        <li>🤝 Collaborate with your team</li>
                    </ul>

                    <p>If you didn't create an account with Axie Studio, you can safely ignore this email.</p>

                    <div class="footer">
                        <div style="margin-bottom: 15px;">
                            <a href="https://axiestudio.se" style="color: #2563eb; text-decoration: none; font-weight: bold;">🌐 Visit axiestudio.se</a>
                        </div>
                        <p style="color: #666; font-size: 12px; margin: 0;">
                            This email was sent by <strong>Axie Studio</strong><br>
                            Building the future of AI workflows at <a href="https://flow.axiestudio.se" style="color: #2563eb;">axiestudio.se</a>
                        </p>
                        <p style="color: #999; font-size: 11px; margin-top: 10px;">
                            Need help? Contact our support team - we're here to help! 💬
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Welcome to Axie Studio!

            Hi {username},

            🎉 Thank you for joining Axie Studio - the ultimate platform for building AI-powered workflows!

            To complete your registration and start creating amazing flows, please verify your email address by visiting this link:

            {verification_link}

            ⏰ IMPORTANT: This verification link will expire in 24 hours.

            Once verified, you'll be able to:
            • 🚀 Create powerful AI workflows
            • 🔗 Connect multiple AI models
            • 📊 Build custom dashboards
            • 🤝 Collaborate with your team

            Visit us at: https://axiestudio.se

            If you didn't create an account with Axie Studio, you can safely ignore this email.

            ---
            Building the future of AI workflows at axiestudio.se
            Need help? Contact our support team - we're here to help!
            """
            
            return await self._send_email(email, subject, text_body, html_body)

        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {e}")
            return False

    async def send_password_reset_email(self, email: str, username: str, token: str, client_ip: str = "unknown") -> bool:
        """Send password reset email."""
        try:
            # Get frontend URL from settings
            settings_service = get_settings_service()
            frontend_url = getattr(settings_service.settings, 'frontend_url', 'https://flow.axiestudio.se')

            # Create password reset link (we'll create this page)
            reset_link = f"{frontend_url}/reset-password?token={token}"

            # Create email content
            subject = "Reset your Axie Studio password"

            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Reset your Axie Studio password</title>
                <style>
                    .logo {{
                        width: 80px;
                        height: 80px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 16px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto 20px;
                        overflow: hidden;
                        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                        border: 3px solid rgba(255, 255, 255, 0.2);
                    }}
                    .logo img {{
                        width: 100%;
                        height: 100%;
                        object-fit: cover;
                        border-radius: 13px;
                    }}
                    .reset-btn {{
                        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                        color: white;
                        padding: 12px 30px;
                        text-decoration: none;
                        border-radius: 8px;
                        display: inline-block;
                        font-weight: bold;
                        margin: 20px 0;
                    }}
                    .footer {{
                        border-top: 1px solid #eee;
                        margin-top: 30px;
                        padding-top: 20px;
                        text-align: center;
                    }}
                </style>
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f8fafc;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Logo -->
                    <div class="logo">
                        <img src="https://scontent-arn2-1.xx.fbcdn.net/v/t39.30808-6/499498872_122132145854766980_5268724011023190696_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=u5dFev5AG-kQ7kNvwFS6K3m&_nc_oc=AdltILxg_X65VXBn-MK3Z58PgtgR7ITbbYcGrvZSWDnQLiIitDDiDq9uw1DoamQT61U&_nc_zt=23&_nc_ht=scontent-arn2-1.xx&_nc_gid=mpLb2UFdGIvVDUjGf2bZuw&oh=00_AfXfUa1TAFSuNwQPVCsbeshZuHKq0TqnRwUgl4EdrFju9w&oe=68A94B99" alt="Axie Studio Logo" />
                    </div>

                    <h2 style="color: #dc2626; margin-bottom: 20px;">Reset Your Password</h2>

                    <p>Hi <strong>{username}</strong>,</p>

                    <p>🔐 We received a request to reset your password for your <strong>Axie Studio</strong> account. Click the button below to reset your password:</p>

                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" class="reset-btn">
                            🔑 Reset Password
                        </a>
                    </div>

                    <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px; margin: 20px 0; border-radius: 6px;">
                        <p style="margin: 0; color: #92400e;"><strong>⏰ Important:</strong> This password reset link will expire in 24 hours.</p>
                    </div>

                    <p><strong>What happens next?</strong></p>
                    <ol style="color: #4b5563;">
                        <li>🔗 Click the reset button above</li>
                        <li>🔐 You'll be logged in automatically</li>
                        <li>⚙️ Go to Settings to change your password</li>
                        <li>✅ Your new password will be saved securely</li>
                    </ol>

                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #666; background-color: #f8fafc; padding: 10px; border-radius: 6px; font-family: monospace;">{reset_link}</p>

                    <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 12px; margin: 20px 0; border-radius: 6px;">
                        <p style="margin: 0; color: #991b1b;"><strong>🚨 Security Notice:</strong> If you didn't request this password reset, please ignore this email. Your account is still secure.</p>
                        <p style="margin: 8px 0 0 0; color: #991b1b; font-size: 12px;">Request originated from IP: {client_ip}</p>
                    </div>

                    <div class="footer">
                        <div style="margin-bottom: 15px;">
                            <a href="https://axiestudio.se" style="color: #2563eb; text-decoration: none; font-weight: bold;">🌐 Visit axiestudio.se</a>
                        </div>
                        <p style="color: #666; font-size: 12px; margin: 0;">
                            This email was sent by <strong>Axie Studio</strong><br>
                            Building the future of AI workflows at <a href="https://flow.axiestudio.se" style="color: #2563eb;">axiestudio.se</a>
                        </p>
                        <p style="color: #999; font-size: 11px; margin-top: 10px;">
                            Need help? Contact our support team - we're here to help! 💬
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """

            text_body = f"""
            Reset Your Axie Studio Password

            Hi {username},

            🔐 We received a request to reset your password for your Axie Studio account.

            To reset your password, visit this link:
            {reset_link}

            ⏰ IMPORTANT: This password reset link will expire in 24 hours.

            What happens next:
            1. 🔗 Click the reset link above
            2. 🔐 You'll be logged in automatically
            3. ⚙️ Go to Settings to change your password
            4. ✅ Your new password will be saved securely

            🚨 Security Notice: If you didn't request this password reset, please ignore this email. Your account is still secure.

            Visit us at: https://axiestudio.se

            ---
            Building the future of AI workflows at axiestudio.se
            Need help? Contact our support team - we're here to help!
            """

            return await self._send_email(email, subject, text_body, html_body)

        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {e}")
            return False
    
    async def _send_email(self, to_email: str, subject: str, text_body: str, html_body: str) -> bool:
        """
        Send email using SMTP with enterprise-level error handling and security.

        This method provides:
        - Comprehensive error handling
        - Security best practices
        - Detailed logging for debugging
        - Support for both text and HTML email formats
        """
        try:
            # Validate email settings
            if not self.settings.SMTP_USER or not self.settings.SMTP_PASSWORD:
                logger.error("❌ SMTP credentials not configured. Please set AXIESTUDIO_EMAIL_SMTP_USER and AXIESTUDIO_EMAIL_SMTP_PASSWORD")
                return False

            if not to_email or "@" not in to_email:
                logger.error(f"❌ Invalid email address: {to_email}")
                return False

            logger.info(f"📧 Preparing to send email to {to_email}")

            # Create message with proper headers
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.settings.FROM_NAME} <{self.settings.FROM_EMAIL}>"
            msg['To'] = to_email
            msg['X-Mailer'] = "AxieStudio Email Service v1.0"
            msg['X-Priority'] = "3"  # Normal priority

            # Add text and HTML parts (enterprise standard)
            text_part = MIMEText(text_body, 'plain', 'utf-8')
            html_part = MIMEText(html_body, 'html', 'utf-8')

            msg.attach(text_part)
            msg.attach(html_part)

            logger.debug(f"📧 Connecting to SMTP server: {self.settings.SMTP_HOST}:{self.settings.SMTP_PORT}")

            # Send email with comprehensive error handling
            with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
                # Enable security
                server.starttls()
                logger.debug("🔒 TLS encryption enabled")

                # Authenticate
                server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
                logger.debug("✅ SMTP authentication successful")

                # Send message
                server.send_message(msg)
                logger.info(f"✅ Email sent successfully to {to_email}")

            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ SMTP Authentication failed: {e}")
            logger.error("🔧 Please check your SMTP credentials (AXIESTUDIO_EMAIL_SMTP_USER and AXIESTUDIO_EMAIL_SMTP_PASSWORD)")
            return False

        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"❌ Email address rejected by server: {to_email} - {e}")
            return False

        except smtplib.SMTPServerDisconnected as e:
            logger.error(f"❌ SMTP server disconnected: {e}")
            logger.error("🔧 Please check your SMTP server settings")
            return False

        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP error occurred: {e}")
            return False

        except Exception as e:
            logger.exception(f"❌ Unexpected error sending email to {to_email}: {e}")
            return False


# Global email service instance
email_service = EmailService()
