"""
Enterprise Email Service with Professional Templates
Clean, professional email templates without emojis
"""

import smtplib
import secrets
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any

from loguru import logger

from axiestudio.services.settings.email import EmailSettings
from axiestudio.services.deps import get_settings_service


class EmailService:
    """
    Enterprise-grade email service using SMTP.

    Features:
    - Professional email templates without emojis
    - Email verification codes
    - Password reset emails
    - Comprehensive error handling
    - Security best practices
    """

    def __init__(self):
        self.settings = EmailSettings()
        self._validate_configuration()

    def _validate_configuration(self) -> None:
        """Validate email configuration on startup."""
        if not self.settings.SMTP_HOST:
            logger.warning("SMTP_HOST not configured. Email functionality will be disabled.")
        
        if not self.settings.SMTP_USER or not self.settings.SMTP_PASSWORD:
            logger.warning("SMTP credentials not configured. Email functionality will be disabled.")
        
        if not self.settings.FROM_EMAIL:
            logger.warning("FROM_EMAIL not configured. Email functionality will be disabled.")

    async def health_check(self) -> Dict[str, Any]:
        """Check email service health."""
        try:
            health_status = {
                "service": "email",
                "status": "healthy",
                "smtp_host": self.settings.SMTP_HOST,
                "smtp_port": self.settings.SMTP_PORT,
                "from_email": self.settings.FROM_EMAIL,
                "issues": []
            }

            if not self.settings.SMTP_HOST:
                health_status["issues"].append("SMTP_HOST not configured")
                health_status["status"] = "degraded"

            if not self.settings.SMTP_USER or not self.settings.SMTP_PASSWORD:
                health_status["issues"].append("SMTP credentials not configured")
                health_status["status"] = "degraded"

            if not self.settings.FROM_EMAIL or "@" not in self.settings.FROM_EMAIL:
                health_status["issues"].append("Invalid FROM_EMAIL configuration")
                health_status["status"] = "degraded"

            return health_status

        except Exception as e:
            logger.error(f"Email service health check failed: {e}")
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
        """Send 6-digit verification code email with professional template."""
        try:
            subject = "Verify your AxieStudio account"
            
            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify your AxieStudio account</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background-color: #f7fafc;
        }}
        .email-container {{
            background: #ffffff;
            margin: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 40px 30px;
            text-align: center;
        }}

        .header h1 {{
            color: white;
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .header p {{
            color: rgba(255, 255, 255, 0.9);
            margin: 8px 0 0;
            font-size: 16px;
        }}
        .content {{
            padding: 40px;
        }}
        .verification-code {{
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            color: #2d3748;
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            padding: 24px;
            border-radius: 8px;
            letter-spacing: 6px;
            margin: 30px 0;
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
        }}
        .footer {{
            background-color: #f7fafc;
            padding: 30px 40px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
            color: #718096;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="logo">AX</div>
            <h1>Email Verification</h1>
            <p>Welcome to AxieStudio</p>
        </div>

        <div class="content">
            <p>Hello <strong>{username}</strong>,</p>
            <p>Thank you for signing up for AxieStudio. To complete your account setup, please use the verification code below:</p>

            <div class="verification-code">
                {verification_code}
            </div>

            <p style="text-align: center; color: #718096; font-size: 14px; margin: 16px 0;">
                This code expires in 10 minutes
            </p>

            <div style="background-color: #edf2f7; border-left: 4px solid #4299e1; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <h4 style="margin: 0 0 8px; color: #2b6cb0; font-size: 16px;">How to verify your account:</h4>
                <ol style="margin: 8px 0 0; padding-left: 20px; color: #4a5568;">
                    <li>Return to the AxieStudio verification page</li>
                    <li>Enter the 6-digit code above</li>
                    <li>Click "Verify Account" to complete setup</li>
                </ol>
            </div>

            <div style="background-color: #fef5e7; border-left: 4px solid #ed8936; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #744210; font-weight: 500;"><strong>Security Notice:</strong> Never share this code with anyone.</p>
            </div>

            <p style="color: #718096; font-size: 14px; margin-top: 30px;">
                Didn't request this verification? You can safely ignore this email.
            </p>
        </div>

        <div class="footer">
            <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
            <p>Visit us at <a href="https://axiestudio.se" style="color: #4299e1; text-decoration: none;">axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
AxieStudio - Email Verification

Hello {username},

Thank you for signing up for AxieStudio. To complete your account setup, please use the verification code below:

Verification Code: {verification_code}

This code expires in 10 minutes.

How to verify your account:
1. Return to the AxieStudio verification page
2. Enter the 6-digit code above
3. Click "Verify Account" to complete setup

Security Notice: Never share this code with anyone.

Didn't request this verification? You can safely ignore this email.

---
AxieStudio - Building the future of AI workflows
Visit us at: https://axiestudio.se
            """

            success = await self._send_email(email, subject, text_body, html_body)

            if success:
                logger.info(f"Verification code email sent successfully to {email}")
            else:
                logger.error(f"Failed to send verification code email to {email}")

            return success

        except Exception as e:
            logger.exception(f"Error sending verification code email to {email}: {e}")
            return False

    async def send_verification_email(self, email: str, username: str, token: str) -> bool:
        """Send email verification email (legacy token-based)."""
        try:
            # Get frontend URL from settings
            settings_service = get_settings_service()
            frontend_url = getattr(settings_service.settings, 'frontend_url', 'https://flow.axiestudio.se')
            
            # Create verification link
            verification_link = f"{frontend_url}/verify-email?token={token}"
            
            subject = "Verify your AxieStudio email address"
            
            # Use same professional template but with link instead of code
            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify your AxieStudio email</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background-color: #f7fafc;
        }}
        .email-container {{
            background: #ffffff;
            margin: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 40px 30px;
            text-align: center;
        }}

        .verify-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px 32px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 16px;
            margin: 24px 0;
        }}
        .footer {{
            background-color: #f7fafc;
            padding: 30px 40px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
            color: #718096;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <img src="https://flow.axiestudio.se/logo192.png" alt="AxieStudio Logo" style="width: 48px; height: 48px; margin: 0 auto 16px auto; display: block; border-radius: 8px;">
            <h1>Email Verification</h1>
            <p>Welcome to AxieStudio</p>
        </div>

        <div class="content" style="padding: 40px;">
            <p>Hello <strong>{username}</strong>,</p>
            <p>Thank you for signing up for AxieStudio. Please click the button below to verify your email address:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_link}" class="verify-button">
                    Verify Email Address
                </a>
            </div>

            <p style="color: #718096; font-size: 14px; margin-top: 30px;">
                Didn't request this verification? You can safely ignore this email.
            </p>
        </div>

        <div class="footer">
            <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
            <p>Visit us at <a href="https://axiestudio.se" style="color: #4299e1; text-decoration: none;">axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
AxieStudio - Email Verification

Hello {username},

Thank you for signing up for AxieStudio. Please click the link below to verify your email address:

{verification_link}

Didn't request this verification? You can safely ignore this email.

---
AxieStudio - Building the future of AI workflows
Visit us at: https://axiestudio.se
            """

            return await self._send_email(email, subject, text_body, html_body)

        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {e}")
            return False

    async def send_password_reset_email(self, email: str, username: str, token: str, client_ip: str = "unknown") -> bool:
        """Send password reset email with professional template."""
        try:
            # Get frontend URL from settings
            settings_service = get_settings_service()
            frontend_url = getattr(settings_service.settings, 'frontend_url', 'https://flow.axiestudio.se')

            # Create password reset link
            reset_link = f"{frontend_url}/reset-password?token={token}"

            subject = "Reset your AxieStudio password"

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset your AxieStudio password</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background-color: #f7fafc;
        }}
        .email-container {{
            background: #ffffff;
            margin: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        .header {{
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
            padding: 40px 40px 30px;
            text-align: center;
        }}

        .header h1 {{
            color: white;
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .header p {{
            color: rgba(255, 255, 255, 0.9);
            margin: 8px 0 0;
            font-size: 16px;
        }}
        .content {{
            padding: 40px;
        }}
        .reset-button {{
            display: inline-block;
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
            color: white;
            padding: 16px 32px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 16px;
            margin: 24px 0;
        }}
        .footer {{
            background-color: #f7fafc;
            padding: 30px 40px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
            color: #718096;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="logo">AX</div>
            <h1>Password Reset</h1>
            <p>Secure password reset for your account</p>
        </div>

        <div class="content">
            <p>Hello <strong>{username}</strong>,</p>
            <p>We received a request to reset your password for your AxieStudio account. Click the button below to reset your password:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" class="reset-button">
                    Reset Password
                </a>
            </div>

            <div style="background-color: #fef5e7; border-left: 4px solid #f59e0b; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #92400e; font-weight: 500;"><strong>Important:</strong> This password reset link will expire in 24 hours.</p>
            </div>

            <p><strong>What happens next:</strong></p>
            <ol style="color: #4a5568;">
                <li>Click the reset button above</li>
                <li>You'll be logged in automatically</li>
                <li>Go to Settings to change your password</li>
                <li>Your new password will be saved securely</li>
            </ol>

            <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #991b1b; font-weight: 500;"><strong>Security Notice:</strong> If you didn't request this password reset, please ignore this email.</p>
                <p style="margin: 8px 0 0 0; color: #991b1b; font-size: 12px;">Request originated from IP: {client_ip}</p>
            </div>
        </div>

        <div class="footer">
            <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
            <p>Visit us at <a href="https://axiestudio.se" style="color: #4299e1; text-decoration: none;">axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
AxieStudio - Password Reset

Hello {username},

We received a request to reset your password for your AxieStudio account.

To reset your password, visit this link:
{reset_link}

IMPORTANT: This password reset link will expire in 24 hours.

What happens next:
1. Click the reset link above
2. You'll be logged in automatically
3. Go to Settings to change your password
4. Your new password will be saved securely

Security Notice: If you didn't request this password reset, please ignore this email.
Request originated from IP: {client_ip}

---
AxieStudio - Building the future of AI workflows
Visit us at: https://axiestudio.se
            """

            return await self._send_email(email, subject, text_body, html_body)

        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {e}")
            return False

    async def send_temporary_password_email(self, email: str, username: str, temp_password: str, client_ip: str = "unknown") -> bool:
        """Send temporary password email with professional template."""
        try:
            subject = "Your AxieStudio Temporary Password"

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your AxieStudio Temporary Password</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background-color: #f7fafc;
        }}
        .email-container {{
            background-color: #ffffff;
            margin: 20px auto;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}

        .content {{
            padding: 40px;
        }}
        .password-box {{
            background-color: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 24px;
            margin: 24px 0;
            text-align: center;
        }}
        .temp-password {{
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 24px;
            font-weight: bold;
            color: #2d3748;
            background-color: #ffffff;
            padding: 16px;
            border-radius: 6px;
            border: 2px solid #4299e1;
            margin: 16px 0;
            letter-spacing: 2px;
        }}
        .login-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px 32px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin: 20px 0;
        }}
        .warning-box {{
            background-color: #fef5e7;
            border-left: 4px solid #f59e0b;
            padding: 16px;
            margin: 24px 0;
            border-radius: 4px;
        }}
        .footer {{
            background-color: #f7fafc;
            padding: 30px;
            text-align: center;
            color: #718096;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <img src="https://flow.axiestudio.se/logo192.png" alt="AxieStudio Logo" style="width: 48px; height: 48px; margin: 0 auto 16px auto; display: block; border-radius: 8px;">
            <h1>Password Reset</h1>
            <p>Your temporary password is ready</p>
        </div>

        <div class="content">
            <p>Hello <strong>{username}</strong>,</p>
            <p>We've generated a temporary password for your AxieStudio account. Use this to log in:</p>

            <div class="password-box">
                <p style="margin: 0 0 8px 0; font-weight: 600; color: #4a5568;">Temporary Password (Valid for 24 hours)</p>
                <div class="temp-password">{temp_password}</div>
                <p style="margin: 8px 0 0 0; font-size: 14px; color: #718096;">Copy this password exactly as shown</p>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://flow.axiestudio.se/login" class="login-button">
                    Login to AxieStudio
                </a>
            </div>

            <div class="warning-box">
                <p style="margin: 0; color: #92400e; font-weight: 500;"><strong>Important:</strong> This temporary password expires in 24 hours. You will be required to change it after logging in for security.</p>
            </div>

            <div style="background-color: #e6fffa; border-left: 4px solid #38b2ac; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #234e52; font-weight: 500;"><strong>Login Instructions:</strong></p>
                <ol style="margin: 8px 0 0 0; color: #234e52;">
                    <li>Go to the login page</li>
                    <li>Enter your username: <strong>{username}</strong></li>
                    <li>Enter the temporary password above</li>
                    <li>You'll be prompted to create a new password</li>
                </ol>
            </div>

            <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #991b1b; font-weight: 500;"><strong>Security Notice:</strong> If you didn't request this password reset, please contact support immediately.</p>
                <p style="margin: 8px 0 0 0; color: #991b1b; font-size: 12px;">Request originated from IP: {client_ip}</p>
            </div>
        </div>

        <div class="footer">
            <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
            <p>Visit us at <a href="https://axiestudio.se" style="color: #4299e1; text-decoration: none;">axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
AxieStudio - Password Reset

Hello {username},

We've generated a temporary password for your AxieStudio account.

Temporary Password (Valid for 24 hours): {temp_password}

Login Instructions:
1. Go to: https://flow.axiestudio.se/login
2. Username: {username}
3. Password: {temp_password}
4. You'll be prompted to create a new password

IMPORTANT: This temporary password expires in 24 hours. You will be required to change it after logging in for security.

Security Notice: If you didn't request this password reset, please contact support immediately.
Request originated from IP: {client_ip}

---
AxieStudio - Building the future of AI workflows
Visit us at: https://axiestudio.se
            """

            return await self._send_email(email, subject, text_body, html_body)

        except Exception as e:
            logger.error(f"Failed to send temporary password email to {email}: {e}")
            return False

    async def send_login_credentials_email(self, email: str, username: str, client_ip: str = "unknown") -> bool:
        """Send login credentials email with professional template."""
        try:
            subject = "Your AxieStudio Login Credentials"

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your AxieStudio Login Credentials</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background-color: #f7fafc;
        }}
        .email-container {{
            background-color: #ffffff;
            margin: 20px auto;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}

        .content {{
            padding: 40px;
        }}
        .credentials-box {{
            background-color: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 24px;
            margin: 24px 0;
            text-align: center;
        }}
        .credential-item {{
            margin: 16px 0;
            padding: 12px;
            background-color: #ffffff;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }}
        .credential-label {{
            font-weight: 600;
            color: #4a5568;
            font-size: 14px;
            margin-bottom: 4px;
        }}
        .credential-value {{
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 16px;
            color: #2d3748;
            font-weight: 600;
        }}
        .login-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px 32px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin: 20px 0;
        }}
        .footer {{
            background-color: #f7fafc;
            padding: 30px;
            text-align: center;
            color: #718096;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <img src="https://flow.axiestudio.se/logo192.png" alt="AxieStudio Logo" style="width: 48px; height: 48px; margin: 0 auto 16px auto; display: block; border-radius: 8px;">
            <h1>Your Login Credentials</h1>
            <p>Access your AxieStudio account</p>
        </div>

        <div class="content">
            <p>Hello <strong>{username}</strong>,</p>
            <p>As requested, here are your login credentials for AxieStudio:</p>

            <div class="credentials-box">
                <div class="credential-item">
                    <div class="credential-label">Username</div>
                    <div class="credential-value">{username}</div>
                </div>
                <div class="credential-item">
                    <div class="credential-label">Email</div>
                    <div class="credential-value">{email}</div>
                </div>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://flow.axiestudio.se/login" class="login-button">
                    Login to AxieStudio
                </a>
            </div>

            <div style="background-color: #e6fffa; border-left: 4px solid #38b2ac; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #234e52; font-weight: 500;"><strong>Security Note:</strong> Use your existing password to log in. If you've forgotten your password, you can change it in your account settings after logging in.</p>
            </div>

            <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #991b1b; font-weight: 500;"><strong>Security Notice:</strong> If you didn't request these credentials, please ignore this email.</p>
                <p style="margin: 8px 0 0 0; color: #991b1b; font-size: 12px;">Request originated from IP: {client_ip}</p>
            </div>
        </div>

        <div class="footer">
            <p><strong>AxieStudio</strong> - Building the future of AI workflows</p>
            <p>Visit us at <a href="https://axiestudio.se" style="color: #4299e1; text-decoration: none;">axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
AxieStudio - Your Login Credentials

Hello {username},

As requested, here are your login credentials for AxieStudio:

Username: {username}
Email: {email}

To log in, visit: https://flow.axiestudio.se/login

SECURITY NOTE: Use your existing password to log in. If you've forgotten your password, you can change it in your account settings after logging in.

Security Notice: If you didn't request these credentials, please ignore this email.
Request originated from IP: {client_ip}

---
AxieStudio - Building the future of AI workflows
Visit us at: https://axiestudio.se
            """

            return await self._send_email(email, subject, text_body, html_body)

        except Exception as e:
            logger.error(f"Failed to send login credentials email to {email}: {e}")
            return False

    async def _send_email(self, to_email: str, subject: str, text_body: str, html_body: str) -> bool:
        """Send email using SMTP with enterprise-level error handling and security."""
        try:
            # Debug logging for email configuration
            logger.info(f"EMAIL DEBUG - Attempting to send email to: {to_email}")
            logger.info(f"EMAIL DEBUG - SMTP Host: {self.settings.SMTP_HOST}")
            logger.info(f"EMAIL DEBUG - SMTP Port: {self.settings.SMTP_PORT}")
            logger.info(f"EMAIL DEBUG - SMTP User: {self.settings.SMTP_USER}")
            logger.info(f"EMAIL DEBUG - From Email: {self.settings.FROM_EMAIL}")
            logger.info(f"EMAIL DEBUG - Email Enabled: {getattr(self.settings, 'EMAIL_ENABLED', True)}")

            # Check if email is disabled
            if not getattr(self.settings, 'EMAIL_ENABLED', True):
                logger.warning("Email sending is disabled (EMAIL_ENABLED=False)")
                return False

            # Validate email settings
            if not self.settings.SMTP_USER or not self.settings.SMTP_PASSWORD:
                logger.error("SMTP credentials not configured. Please set AXIESTUDIO_EMAIL_SMTP_USER and AXIESTUDIO_EMAIL_SMTP_PASSWORD")
                return False

            if not self.settings.FROM_EMAIL or "@" not in self.settings.FROM_EMAIL:
                logger.error("Invalid FROM_EMAIL configuration")
                return False

            # Validate Resend configuration specifically
            if self.settings.SMTP_HOST == "smtp.resend.com":
                if self.settings.SMTP_USER != "resend":
                    logger.error(f"For Resend SMTP, SMTP_USER must be 'resend', got: {self.settings.SMTP_USER}")
                    return False
                if not self.settings.SMTP_PASSWORD.startswith("re_"):
                    logger.error("For Resend SMTP, SMTP_PASSWORD must be a Resend API key (starts with 're_')")
                    return False

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.settings.FROM_EMAIL
            msg['To'] = to_email

            # Create text and HTML parts
            text_part = MIMEText(text_body, 'plain', 'utf-8')
            html_part = MIMEText(html_body, 'html', 'utf-8')

            # Add parts to message
            msg.attach(text_part)
            msg.attach(html_part)

            # Send email with detailed debugging
            logger.info(f"SMTP CONFIG - Host: {self.settings.SMTP_HOST}:{self.settings.SMTP_PORT}")
            logger.info(f"SMTP CONFIG - User: {self.settings.SMTP_USER}")
            logger.info(f"SMTP CONFIG - From: {self.settings.FROM_EMAIL}")
            logger.info(f"SMTP CONFIG - To: {to_email}")
            logger.info(f"EMAIL DEBUG - Connecting to SMTP server...")
            with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
                logger.info(f"EMAIL DEBUG - Connection established successfully")
                logger.info(f"EMAIL DEBUG - Starting TLS...")
                server.starttls()
                logger.info(f"EMAIL DEBUG - TLS started successfully")
                logger.info(f"EMAIL DEBUG - Logging in with user: {self.settings.SMTP_USER}")
                server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
                logger.info(f"EMAIL DEBUG - Authentication successful")
                logger.info(f"EMAIL DEBUG - Sending message...")
                server.send_message(msg)
                logger.info(f"EMAIL DEBUG - Message sent to SMTP server successfully")

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            logger.error(f"SMTP AUTH DEBUG - Host: {self.settings.SMTP_HOST}, User: {self.settings.SMTP_USER}")
            logger.error(f"SMTP AUTH DEBUG - Password length: {len(self.settings.SMTP_PASSWORD) if self.settings.SMTP_PASSWORD else 0}")
            return False

        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"SMTP recipients refused: {e}")
            return False

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {e}")
            return False

        except ConnectionError as e:
            logger.error(f"Connection error to SMTP server: {e}")
            return False

        except TimeoutError as e:
            logger.error(f"Timeout connecting to SMTP server: {e}")
            return False

        except Exception as e:
            logger.exception(f"Unexpected error sending email to {to_email}: {e}")
            logger.error(f"ERROR DEBUG - SMTP Config: {self.settings.SMTP_HOST}:{self.settings.SMTP_PORT}")
            logger.error(f"ERROR DEBUG - From: {self.settings.FROM_EMAIL}, To: {to_email}")
            return False


# Global email service instance
email_service = EmailService()
