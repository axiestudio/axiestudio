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
            subject = "Verifiera ditt AxieStudio-konto"
            
            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifiera ditt AxieStudio-konto</title>
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
            <h1>E-postverifiering</h1>
            <p>Välkommen till AxieStudio</p>
        </div>

        <div class="content">
            <p>Hej <strong>{username}</strong>,</p>
            <p>Tack för att du registrerat dig för AxieStudio. För att slutföra din kontokonfiguration, vänligen använd verifieringskoden nedan:</p>

            <div class="verification-code">
                {verification_code}
            </div>

            <p style="text-align: center; color: #718096; font-size: 14px; margin: 16px 0;">
                Denna kod går ut om 10 minuter
            </p>

            <div style="background-color: #edf2f7; border-left: 4px solid #4299e1; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <h4 style="margin: 0 0 8px; color: #2b6cb0; font-size: 16px;">Så här verifierar du ditt konto:</h4>
                <ol style="margin: 8px 0 0; padding-left: 20px; color: #4a5568;">
                    <li>Återgå till AxieStudios verifieringssida</li>
                    <li>Ange den 6-siffriga koden ovan</li>
                    <li>Klicka på "Verifiera konto" för att slutföra konfigurationen</li>
                </ol>
            </div>

            <div style="background-color: #fef5e7; border-left: 4px solid #ed8936; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #744210; font-weight: 500;"><strong>Säkerhetsmeddelande:</strong> Dela aldrig denna kod med någon.</p>
            </div>

            <p style="color: #718096; font-size: 14px; margin-top: 30px;">
                Begärde du inte denna verifiering? Du kan säkert ignorera detta e-postmeddelande.
            </p>
        </div>

        <div class="footer">
            <p><strong>AxieStudio</strong> - Bygger framtiden för AI-arbetsflöden</p>
            <p>Besök oss på <a href="https://axiestudio.se" style="color: #4299e1; text-decoration: none;">axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
AxieStudio - E-postverifiering

Hej {username},

Tack för att du registrerat dig för AxieStudio. För att slutföra din kontokonfiguration, vänligen använd verifieringskoden nedan:

Verifieringskod: {verification_code}

Denna kod går ut om 10 minuter.

Så här verifierar du ditt konto:
1. Återgå till AxieStudios verifieringssida
2. Ange den 6-siffriga koden ovan
3. Klicka på "Verifiera konto" för att slutföra konfigurationen

Säkerhetsmeddelande: Dela aldrig denna kod med någon.

Begärde du inte denna verifiering? Du kan säkert ignorera detta e-postmeddelande.

---
AxieStudio - Bygger framtiden för AI-arbetsflöden
Besök oss på: https://axiestudio.se
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
            
            subject = "Verifiera din AxieStudio e-postadress"
            
            # Use same professional template but with link instead of code
            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifiera din AxieStudio e-postadress</title>
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
            <h1>E-postverifiering</h1>
            <p>Välkommen till AxieStudio</p>
        </div>

        <div class="content" style="padding: 40px;">
            <p>Hej <strong>{username}</strong>,</p>
            <p>Tack för att du registrerat dig för AxieStudio. Vänligen klicka på knappen nedan för att verifiera din e-postadress:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_link}" class="verify-button">
                    Verifiera e-postadress
                </a>
            </div>

            <p style="color: #718096; font-size: 14px; margin-top: 30px;">
                Begärde du inte denna verifiering? Du kan säkert ignorera detta e-postmeddelande.
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

            subject = "Återställ ditt AxieStudio-lösenord"

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Återställ ditt AxieStudio-lösenord</title>
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
            <h1>Lösenordsåterställning</h1>
            <p>Säker lösenordsåterställning för ditt konto</p>
        </div>

        <div class="content">
            <p>Hej <strong>{username}</strong>,</p>
            <p>Vi fick en begäran om att återställa ditt lösenord för ditt AxieStudio-konto. Klicka på knappen nedan för att återställa ditt lösenord:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" class="reset-button">
                    Återställ lösenord
                </a>
            </div>

            <div style="background-color: #fef5e7; border-left: 4px solid #f59e0b; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #92400e; font-weight: 500;"><strong>Viktigt:</strong> Denna lösenordsåterställningslänk går ut om 24 timmar.</p>
            </div>

            <p><strong>Vad händer härnäst:</strong></p>
            <ol style="color: #4a5568;">
                <li>Klicka på återställningsknappen ovan</li>
                <li>Du kommer att loggas in automatiskt</li>
                <li>Gå till Inställningar för att ändra ditt lösenord</li>
                <li>Ditt nya lösenord kommer att sparas säkert</li>
            </ol>

            <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #991b1b; font-weight: 500;"><strong>Säkerhetsmeddelande:</strong> Om du inte begärde denna lösenordsåterställning, vänligen ignorera detta e-postmeddelande.</p>
                <p style="margin: 8px 0 0 0; color: #991b1b; font-size: 12px;">Begäran kom från IP: {client_ip}</p>
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
AxieStudio - Lösenordsåterställning

Hej {username},

Vi fick en begäran om att återställa ditt lösenord för ditt AxieStudio-konto.

För att återställa ditt lösenord, besök denna länk:
{reset_link}

VIKTIGT: Denna lösenordsåterställningslänk går ut om 24 timmar.

Vad händer härnäst:
1. Klicka på återställningslänken ovan
2. Du kommer att loggas in automatiskt
3. Gå till Inställningar för att ändra ditt lösenord
4. Ditt nya lösenord kommer att sparas säkert

Säkerhetsmeddelande: Om du inte begärde denna lösenordsåterställning, vänligen ignorera detta e-postmeddelande.
Begäran kom från IP: {client_ip}

---
AxieStudio - Bygger framtiden för AI-arbetsflöden
Besök oss på: https://axiestudio.se
            """

            return await self._send_email(email, subject, text_body, html_body)

        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {e}")
            return False

    async def send_temporary_password_email(self, email: str, username: str, temp_password: str, client_ip: str = "unknown") -> bool:
        """Send temporary password email with professional template."""
        try:
            subject = "Ditt tillfälliga AxieStudio-lösenord"

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ditt tillfälliga AxieStudio-lösenord</title>
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
            <h1>Lösenordsåterställning</h1>
            <p>Ditt tillfälliga lösenord är klart</p>
        </div>

        <div class="content">
            <p>Hej <strong>{username}</strong>,</p>
            <p>Vi har genererat ett tillfälligt lösenord för ditt AxieStudio-konto. Använd detta för att logga in:</p>

            <div class="password-box">
                <p style="margin: 0 0 8px 0; font-weight: 600; color: #4a5568;">Tillfälligt lösenord (Giltigt i 24 timmar)</p>
                <div class="temp-password">{temp_password}</div>
                <p style="margin: 8px 0 0 0; font-size: 14px; color: #718096;">Kopiera detta lösenord exakt som det visas</p>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://flow.axiestudio.se/login" class="login-button">
                    Logga in på AxieStudio
                </a>
            </div>

            <div class="warning-box">
                <p style="margin: 0; color: #92400e; font-weight: 500;"><strong>Viktigt:</strong> Detta tillfälliga lösenord går ut om 24 timmar. Du kommer att behöva ändra det efter inloggning av säkerhetsskäl.</p>
            </div>

            <div style="background-color: #e6fffa; border-left: 4px solid #38b2ac; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #234e52; font-weight: 500;"><strong>Inloggningsinstruktioner:</strong></p>
                <ol style="margin: 8px 0 0 0; color: #234e52;">
                    <li>Gå till inloggningssidan</li>
                    <li>Ange ditt användarnamn: <strong>{username}</strong></li>
                    <li>Ange det tillfälliga lösenordet ovan</li>
                    <li>Du kommer att uppmanas att skapa ett nytt lösenord</li>
                </ol>
            </div>

            <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #991b1b; font-weight: 500;"><strong>Säkerhetsmeddelande:</strong> Om du inte begärde denna lösenordsåterställning, vänligen kontakta support omedelbart.</p>
                <p style="margin: 8px 0 0 0; color: #991b1b; font-size: 12px;">Begäran kom från IP: {client_ip}</p>
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
AxieStudio - Lösenordsåterställning

Hej {username},

Vi har genererat ett tillfälligt lösenord för ditt AxieStudio-konto.

Tillfälligt lösenord (Giltigt i 24 timmar): {temp_password}

Inloggningsinstruktioner:
1. Gå till: https://flow.axiestudio.se/login
2. Användarnamn: {username}
3. Lösenord: {temp_password}
4. Du kommer att uppmanas att skapa ett nytt lösenord

VIKTIGT: Detta tillfälliga lösenord går ut om 24 timmar. Du kommer att behöva ändra det efter inloggning av säkerhetsskäl.

Säkerhetsmeddelande: Om du inte begärde denna lösenordsåterställning, vänligen kontakta support omedelbart.
Begäran kom från IP: {client_ip}

---
AxieStudio - Bygger framtiden för AI-arbetsflöden
Besök oss på: https://axiestudio.se
            """

            return await self._send_email(email, subject, text_body, html_body)

        except Exception as e:
            logger.error(f"Failed to send temporary password email to {email}: {e}")
            return False

    async def send_login_credentials_email(self, email: str, username: str, client_ip: str = "unknown") -> bool:
        """Send login credentials email with professional template."""
        try:
            subject = "Dina AxieStudio inloggningsuppgifter"

            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dina AxieStudio inloggningsuppgifter</title>
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
            <h1>Dina inloggningsuppgifter</h1>
            <p>Få tillgång till ditt AxieStudio-konto</p>
        </div>

        <div class="content">
            <p>Hej <strong>{username}</strong>,</p>
            <p>Som begärt, här är dina inloggningsuppgifter för AxieStudio:</p>

            <div class="credentials-box">
                <div class="credential-item">
                    <div class="credential-label">Användarnamn</div>
                    <div class="credential-value">{username}</div>
                </div>
                <div class="credential-item">
                    <div class="credential-label">E-post</div>
                    <div class="credential-value">{email}</div>
                </div>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://flow.axiestudio.se/login" class="login-button">
                    Logga in på AxieStudio
                </a>
            </div>

            <div style="background-color: #e6fffa; border-left: 4px solid #38b2ac; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #234e52; font-weight: 500;"><strong>Säkerhetsnotering:</strong> Använd ditt befintliga lösenord för att logga in. Om du har glömt ditt lösenord kan du ändra det i dina kontoinställningar efter inloggning.</p>
            </div>

            <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 16px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; color: #991b1b; font-weight: 500;"><strong>Säkerhetsmeddelande:</strong> Om du inte begärde dessa inloggningsuppgifter, vänligen ignorera detta e-postmeddelande.</p>
                <p style="margin: 8px 0 0 0; color: #991b1b; font-size: 12px;">Begäran kom från IP: {client_ip}</p>
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
AxieStudio - Dina inloggningsuppgifter

Hej {username},

Som begärt, här är dina inloggningsuppgifter för AxieStudio:

Användarnamn: {username}
E-post: {email}

För att logga in, besök: https://flow.axiestudio.se/login

SÄKERHETSNOTERING: Använd ditt befintliga lösenord för att logga in. Om du har glömt ditt lösenord kan du ändra det i dina kontoinställningar efter inloggning.

Säkerhetsmeddelande: Om du inte begärde dessa inloggningsuppgifter, vänligen ignorera detta e-postmeddelande.
Begäran kom från IP: {client_ip}

---
AxieStudio - Bygger framtiden för AI-arbetsflöden
Besök oss på: https://axiestudio.se
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

            # Validate email settings
            if not self.settings.SMTP_USER or not self.settings.SMTP_PASSWORD:
                logger.error("SMTP credentials not configured. Please set AXIESTUDIO_EMAIL_SMTP_USER and AXIESTUDIO_EMAIL_SMTP_PASSWORD")
                return False

            if not self.settings.FROM_EMAIL or "@" not in self.settings.FROM_EMAIL:
                logger.error("Invalid FROM_EMAIL configuration")
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
                logger.info(f"EMAIL DEBUG - Starting TLS...")
                server.starttls()
                logger.info(f"EMAIL DEBUG - Logging in with user: {self.settings.SMTP_USER}")
                server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
                logger.info(f"EMAIL DEBUG - Sending message...")
                server.send_message(msg)
                logger.info(f"EMAIL DEBUG - Message sent to SMTP server successfully")

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            return False

        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"SMTP recipients refused: {e}")
            return False

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {e}")
            return False

        except Exception as e:
            logger.exception(f"Unexpected error sending email to {to_email}: {e}")
            return False


# Global email service instance - now uses factory pattern with enhanced logging
from axiestudio.services.email.factory import get_email_service
from loguru import logger

logger.info("🚀" + "=" * 80)
logger.info("🚀 AXIESTUDIO EMAIL SYSTEM - INITIALIZING GLOBAL EMAIL SERVICE")
logger.info("🚀" + "=" * 80)

email_service = get_email_service()

# Log the final service type for production visibility
service_type = type(email_service).__name__
if "Resend" in service_type:
    logger.info("✅ GLOBAL EMAIL SERVICE: ResendEmailService (Resend SDK PRIMARY)")
    logger.info("🎯 EMAIL DELIVERY METHOD: Resend SDK API")
    logger.info("❌ SMTP STATUS: Not used (Resend SDK replaced SMTP)")
else:
    logger.info("⚠️ GLOBAL EMAIL SERVICE: EmailService (SMTP)")
    logger.info("🔧 EMAIL DELIVERY METHOD: SMTP Protocol")
    logger.info("❌ RESEND SDK STATUS: Not primary (check configuration)")

logger.info("🚀" + "=" * 80)
