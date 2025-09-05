"""
Enterprise Email Service using Resend SDK
High-performance email service with comprehensive logging and error handling
"""

import secrets
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

import resend
from loguru import logger

from axiestudio.services.settings.email import EmailSettings
from axiestudio.services.deps import get_settings_service


class ResendEmailService:
    """
    Enterprise-grade email service using Resend SDK.

    Features:
    - Native Resend SDK integration
    - Professional email templates without emojis
    - Email verification codes
    - Password reset emails
    - Comprehensive error handling and logging
    - Security best practices
    - API response tracking
    """

    def __init__(self):
        self.settings = EmailSettings()
        self._validate_configuration()
        self._initialize_resend()

    def _validate_configuration(self) -> None:
        """Validate Resend configuration on startup."""
        if not self.settings.RESEND_API_KEY:
            logger.warning("RESEND_API_KEY not configured. Email functionality will be disabled.")
        
        if not self.settings.FROM_EMAIL:
            logger.warning("FROM_EMAIL not configured. Email functionality will be disabled.")
        
        if self.settings.FROM_EMAIL and "@" not in self.settings.FROM_EMAIL:
            logger.warning("Invalid FROM_EMAIL format. Email functionality may be impaired.")

    def _initialize_resend(self) -> None:
        """Initialize Resend SDK with API key."""
        if self.settings.RESEND_API_KEY:
            resend.api_key = self.settings.RESEND_API_KEY
            logger.info("RESEND SDK - Initialized with API key")
        else:
            logger.error("RESEND SDK - Cannot initialize without API key")

    async def health_check(self) -> Dict[str, Any]:
        """Check email service health."""
        try:
            health_status = {
                "service": "resend_email",
                "status": "healthy",
                "api_key_configured": bool(self.settings.RESEND_API_KEY),
                "from_email": self.settings.FROM_EMAIL,
                "sdk_version": resend.__version__ if hasattr(resend, '__version__') else "unknown",
                "issues": []
            }

            if not self.settings.RESEND_API_KEY:
                health_status["issues"].append("RESEND_API_KEY not configured")
                health_status["status"] = "degraded"

            if not self.settings.FROM_EMAIL or "@" not in self.settings.FROM_EMAIL:
                health_status["issues"].append("Invalid FROM_EMAIL configuration")
                health_status["status"] = "degraded"

            return health_status

        except Exception as e:
            logger.error(f"Resend email service health check failed: {e}")
            return {
                "service": "resend_email",
                "status": "unhealthy",
                "error": str(e)
            }
    
    def generate_verification_token(self) -> str:
        """Generate a secure verification token."""
        return secrets.token_urlsafe(32)
    
    def get_verification_expiry(self) -> datetime:
        """Get verification token expiry time (24 hours from now)."""
        return datetime.now(timezone.utc) + timedelta(hours=24)

    async def _send_email_with_resend(self, to_email: str, subject: str, text_body: str, html_body: str, 
                                     reply_to: Optional[str] = None) -> bool:
        """Send email using Resend SDK with comprehensive logging and error handling."""
        try:
            # Validate configuration
            if not self.settings.RESEND_API_KEY:
                logger.error("RESEND SDK - API key not configured")
                return False

            if not self.settings.FROM_EMAIL:
                logger.error("RESEND SDK - FROM_EMAIL not configured")
                return False

            # Prepare email parameters
            from_address = f"{self.settings.FROM_NAME} <{self.settings.FROM_EMAIL}>"
            
            params: resend.Emails.SendParams = {
                "from": from_address,
                "to": [to_email],
                "subject": subject,
                "html": html_body,
                "text": text_body,
            }
            
            if reply_to:
                params["reply_to"] = [reply_to]

            # Log email attempt
            logger.info(f"RESEND SDK - Attempting to send email to: {to_email}")
            logger.info(f"RESEND SDK - From: {from_address}")
            logger.info(f"RESEND SDK - Subject: {subject}")
            logger.info(f"RESEND SDK - Reply-to: {reply_to if reply_to else 'None'}")

            # Send email using Resend SDK
            email_response = resend.Emails.send(params)

            # Log successful response - handle both dict and object formats
            if email_response:
                # Handle dict response format
                if isinstance(email_response, dict) and 'id' in email_response:
                    email_id = email_response['id']
                    logger.info(f"RESEND SDK - Email sent successfully. ID: {email_id}")
                    logger.info(f"RESEND SDK - Response: {email_response}")
                    return True
                # Handle object response format
                elif hasattr(email_response, 'id'):
                    logger.info(f"RESEND SDK - Email sent successfully. ID: {email_response.id}")
                    logger.info(f"RESEND SDK - Response: {email_response}")
                    return True
                else:
                    logger.warning(f"RESEND SDK - Unexpected response format: {email_response}")
                    return False
            else:
                logger.error("RESEND SDK - No response received from API")
                return False

        except Exception as e:
            logger.error(f"RESEND SDK - Failed to send email to {to_email}: {e}")
            logger.exception("RESEND SDK - Full exception details:")
            return False

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
            color: #ffffff;
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .content {{
            padding: 40px;
        }}
        .verification-code {{
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            margin: 30px 0;
        }}
        .code {{
            font-size: 32px;
            font-weight: bold;
            color: #495057;
            letter-spacing: 8px;
            font-family: 'Courier New', monospace;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Kontoverifiering</h1>
        </div>
        <div class="content">
            <p>Hej {username},</p>
            <p>Tack för att du registrerat dig hos AxieStudio! För att slutföra din kontoregistrering, vänligen använd verifieringskoden nedan:</p>
            
            <div class="verification-code">
                <div class="code">{verification_code}</div>
                <p style="margin: 10px 0 0 0; color: #6c757d; font-size: 14px;">Denna kod är giltig i {self.settings.VERIFICATION_CODE_EXPIRY_MINUTES} minuter</p>
            </div>
            
            <p>Om du inte begärde denna verifiering, vänligen ignorera detta e-postmeddelande.</p>
            
            <p>Välkommen till AxieStudio!</p>
        </div>
        <div class="footer">
            <p>Detta e-postmeddelande skickades automatiskt. Vänligen svara inte på detta meddelande.</p>
            <p>AxieStudio - Bygger framtiden för AI-arbetsflöden</p>
            <p>Besök oss på: <a href="https://axiestudio.se">https://axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
Hej {username},

Tack för att du registrerat dig hos AxieStudio! För att slutföra din kontoregistrering, vänligen använd verifieringskoden nedan:

VERIFIERINGSKOD: {verification_code}

Denna kod är giltig i {self.settings.VERIFICATION_CODE_EXPIRY_MINUTES} minuter.

Om du inte begärde denna verifiering, vänligen ignorera detta e-postmeddelande.

Välkommen till AxieStudio!

---
AxieStudio - Bygger framtiden för AI-arbetsflöden
Besök oss på: https://axiestudio.se
            """

            return await self._send_email_with_resend(email, subject, text_body, html_body)

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
        .header h1 {{
            color: #ffffff;
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .content {{
            padding: 40px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            margin: 20px 0;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>E-postverifiering</h1>
        </div>
        <div class="content">
            <p>Hej {username},</p>
            <p>Tack för att du registrerat dig hos AxieStudio! För att slutföra din kontoregistrering, vänligen klicka på knappen nedan för att verifiera din e-postadress:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_link}" class="button">Verifiera e-postadress</a>
            </div>

            <p>Om knappen inte fungerar, kopiera och klistra in följande länk i din webbläsare:</p>
            <p style="word-break: break-all; color: #667eea;">{verification_link}</p>

            <p>Denna länk är giltig i 24 timmar.</p>

            <p>Om du inte begärde denna verifiering, vänligen ignorera detta e-postmeddelande.</p>

            <p>Välkommen till AxieStudio!</p>
        </div>
        <div class="footer">
            <p>Detta e-postmeddelande skickades automatiskt. Vänligen svara inte på detta meddelande.</p>
            <p>AxieStudio - Bygger framtiden för AI-arbetsflöden</p>
            <p>Besök oss på: <a href="https://axiestudio.se">https://axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
Hej {username},

Tack för att du registrerat dig hos AxieStudio! För att slutföra din kontoregistrering, vänligen besök följande länk för att verifiera din e-postadress:

{verification_link}

Denna länk är giltig i 24 timmar.

Om du inte begärde denna verifiering, vänligen ignorera detta e-postmeddelande.

Välkommen till AxieStudio!

---
AxieStudio - Bygger framtiden för AI-arbetsflöden
Besök oss på: https://axiestudio.se
            """

            return await self._send_email_with_resend(email, subject, text_body, html_body)

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
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            padding: 40px 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            color: #ffffff;
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .content {{
            padding: 40px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            margin: 20px 0;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
        }}
        .security-notice {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Lösenordsåterställning</h1>
        </div>
        <div class="content">
            <p>Hej {username},</p>
            <p>Vi har mottagit en begäran om att återställa lösenordet för ditt AxieStudio-konto. Om du begärde detta, klicka på knappen nedan för att skapa ett nytt lösenord:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" class="button">Återställ lösenord</a>
            </div>

            <p>Om knappen inte fungerar, kopiera och klistra in följande länk i din webbläsare:</p>
            <p style="word-break: break-all; color: #dc3545;">{reset_link}</p>

            <div class="security-notice">
                <strong>Säkerhetsmeddelande:</strong>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>Denna länk är giltig i {self.settings.PASSWORD_RESET_EXPIRY_HOURS} timme(r)</li>
                    <li>Länken kan endast användas en gång</li>
                    <li>Begäran kom från IP-adress: {client_ip}</li>
                </ul>
            </div>

            <p>Om du inte begärde en lösenordsåterställning, vänligen ignorera detta e-postmeddelande. Ditt lösenord förblir oförändrat.</p>

            <p>Om du har frågor eller behöver hjälp, kontakta oss på {self.settings.SUPPORT_EMAIL}</p>
        </div>
        <div class="footer">
            <p>Detta e-postmeddelande skickades automatiskt. Vänligen svara inte på detta meddelande.</p>
            <p>AxieStudio - Bygger framtiden för AI-arbetsflöden</p>
            <p>Besök oss på: <a href="https://axiestudio.se">https://axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
Hej {username},

Vi har mottagit en begäran om att återställa lösenordet för ditt AxieStudio-konto. Om du begärde detta, besök följande länk för att skapa ett nytt lösenord:

{reset_link}

SÄKERHETSMEDDELANDE:
- Denna länk är giltig i {self.settings.PASSWORD_RESET_EXPIRY_HOURS} timme(r)
- Länken kan endast användas en gång
- Begäran kom från IP-adress: {client_ip}

Om du inte begärde en lösenordsåterställning, vänligen ignorera detta e-postmeddelande. Ditt lösenord förblir oförändrat.

Om du har frågor eller behöver hjälp, kontakta oss på {self.settings.SUPPORT_EMAIL}

---
AxieStudio - Bygger framtiden för AI-arbetsflöden
Besök oss på: https://axiestudio.se
            """

            return await self._send_email_with_resend(email, subject, text_body, html_body)

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
            background: #ffffff;
            margin: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        .header {{
            background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
            padding: 40px 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            color: #1a202c;
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .content {{
            padding: 40px;
        }}
        .password-box {{
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            margin: 30px 0;
        }}
        .password {{
            font-size: 24px;
            font-weight: bold;
            color: #495057;
            font-family: 'Courier New', monospace;
            word-break: break-all;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
        }}
        .security-notice {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Tillfälligt lösenord</h1>
        </div>
        <div class="content">
            <p>Hej {username},</p>
            <p>Som begärt har vi genererat ett tillfälligt lösenord för ditt AxieStudio-konto:</p>

            <div class="password-box">
                <div class="password">{temp_password}</div>
                <p style="margin: 10px 0 0 0; color: #6c757d; font-size: 14px;">Kopiera detta lösenord exakt som det visas</p>
            </div>

            <div class="security-notice">
                <strong>Viktiga säkerhetsanvisningar:</strong>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>Ändra detta lösenord omedelbart efter inloggning</li>
                    <li>Använd ett starkt, unikt lösenord</li>
                    <li>Dela aldrig ditt lösenord med andra</li>
                    <li>Begäran kom från IP-adress: {client_ip}</li>
                </ul>
            </div>

            <p>För att logga in, besök: <a href="https://flow.axiestudio.se/login">https://flow.axiestudio.se/login</a></p>

            <p>Om du inte begärde detta tillfälliga lösenord, kontakta oss omedelbart på {self.settings.SUPPORT_EMAIL}</p>
        </div>
        <div class="footer">
            <p>Detta e-postmeddelande skickades automatiskt. Vänligen svara inte på detta meddelande.</p>
            <p>AxieStudio - Bygger framtiden för AI-arbetsflöden</p>
            <p>Besök oss på: <a href="https://axiestudio.se">https://axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
Hej {username},

Som begärt har vi genererat ett tillfälligt lösenord för ditt AxieStudio-konto:

TILLFÄLLIGT LÖSENORD: {temp_password}

VIKTIGA SÄKERHETSANVISNINGAR:
- Ändra detta lösenord omedelbart efter inloggning
- Använd ett starkt, unikt lösenord
- Dela aldrig ditt lösenord med andra
- Begäran kom från IP-adress: {client_ip}

För att logga in, besök: https://flow.axiestudio.se/login

Om du inte begärde detta tillfälliga lösenord, kontakta oss omedelbart på {self.settings.SUPPORT_EMAIL}

---
AxieStudio - Bygger framtiden för AI-arbetsflöden
Besök oss på: https://axiestudio.se
            """

            return await self._send_email_with_resend(email, subject, text_body, html_body)

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
            background: #ffffff;
            margin: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        .header {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            padding: 40px 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            color: #ffffff;
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .content {{
            padding: 40px;
        }}
        .credentials-box {{
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin: 30px 0;
        }}
        .credential-item {{
            margin: 15px 0;
            padding: 10px;
            background: #ffffff;
            border-radius: 4px;
            border-left: 4px solid #28a745;
        }}
        .credential-label {{
            font-weight: bold;
            color: #495057;
            font-size: 14px;
        }}
        .credential-value {{
            font-family: 'Courier New', monospace;
            font-size: 16px;
            color: #212529;
            word-break: break-all;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            margin: 20px 0;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
        }}
        .security-notice {{
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
            color: #0c5460;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Inloggningsuppgifter</h1>
        </div>
        <div class="content">
            <p>Hej {username},</p>
            <p>Som begärt, här är dina inloggningsuppgifter för AxieStudio:</p>

            <div class="credentials-box">
                <div class="credential-item">
                    <div class="credential-label">Användarnamn:</div>
                    <div class="credential-value">{username}</div>
                </div>
                <div class="credential-item">
                    <div class="credential-label">E-post:</div>
                    <div class="credential-value">{email}</div>
                </div>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://flow.axiestudio.se/login" class="button">Logga in på AxieStudio</a>
            </div>

            <div class="security-notice">
                <strong>Säkerhetsnotering:</strong> Använd ditt befintliga lösenord för att logga in. Om du har glömt ditt lösenord kan du ändra det i dina kontoinställningar efter inloggning.
            </div>

            <p>Säkerhetsmeddelande: Om du inte begärde dessa inloggningsuppgifter, vänligen ignorera detta e-postmeddelande.</p>
            <p style="color: #6c757d; font-size: 14px;">Begäran kom från IP: {client_ip}</p>
        </div>
        <div class="footer">
            <p>Detta e-postmeddelande skickades automatiskt. Vänligen svara inte på detta meddelande.</p>
            <p>AxieStudio - Bygger framtiden för AI-arbetsflöden</p>
            <p>Besök oss på: <a href="https://axiestudio.se">https://axiestudio.se</a></p>
        </div>
    </div>
</body>
</html>
            """

            text_body = f"""
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

            return await self._send_email_with_resend(email, subject, text_body, html_body)

        except Exception as e:
            logger.error(f"Failed to send login credentials email to {email}: {e}")
            return False
