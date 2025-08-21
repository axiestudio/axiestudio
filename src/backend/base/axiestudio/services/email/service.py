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
    """Simple email service using SMTP."""
    
    def __init__(self):
        self.settings = EmailSettings()
    
    def generate_verification_token(self) -> str:
        """Generate a secure verification token."""
        return secrets.token_urlsafe(32)
    
    def get_verification_expiry(self) -> datetime:
        """Get verification token expiry time (24 hours from now)."""
        return datetime.now(timezone.utc) + timedelta(hours=24)
    
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
        """Send email using SMTP."""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.settings.FROM_NAME} <{self.settings.FROM_EMAIL}>"
            msg['To'] = to_email
            
            # Add text and HTML parts
            text_part = MIMEText(text_body, 'plain')
            html_part = MIMEText(html_body, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
                server.starttls()
                server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Verification email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False


# Global email service instance
email_service = EmailService()
