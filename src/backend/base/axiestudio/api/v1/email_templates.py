"""
Email Template Testing and Management API (Swedish App)
Allows testing and previewing all email templates
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from loguru import logger

from axiestudio.api.utils import DbSession
from axiestudio.services.auth.utils import get_current_active_user
from axiestudio.services.database.models.user.model import User
from axiestudio.services.email.service import EmailService
from axiestudio.services.security.login_detection import get_login_detection_service
from axiestudio.services.notifications.trial_notifications import get_trial_notification_service


router = APIRouter(prefix="/email-templates", tags=["Email Templates"])


class TestEmailRequest(BaseModel):
    email: EmailStr
    template_type: str
    test_data: Optional[dict] = None


class EmailTemplateResponse(BaseModel):
    success: bool
    message: str
    template_type: str
    recipient: str


@router.post("/test", response_model=EmailTemplateResponse)
async def test_email_template(
    request: TestEmailRequest,
    current_user: User = Depends(get_current_active_user),
    session: DbSession = None
):
    """
    Test any email template by sending it to a specified email address.
    
    Available template types:
    - verification_code: E-postverifiering med 6-siffrig kod
    - verification_link: E-postverifiering med länk
    - password_reset: E-post för lösenordsåterställning
    - temporary_password: Tillfälligt lösenord
    - login_credentials: Påminnelse om inloggningsuppgifter
    - new_login_detected: Säkerhetsnotifiering för ny inloggning
    - trial_ending: Notifiering om att provperioden slutar
    - subscription_welcome: Välkomstmail för ny prenumeration
    - subscription_cancelled: Bekräftelse på avbruten prenumeration
    """
    try:
        email_service = EmailService()
        template_type = request.template_type.lower()
        test_email = request.email
        test_data = request.test_data or {}
        
        # Use current user's data as defaults
        username = test_data.get("username", current_user.username)
        
        success = False
        
        if template_type == "verification_code":
            verification_code = test_data.get("verification_code", "123456")
            success = await email_service.send_verification_code_email(
                email=test_email,
                username=username,
                verification_code=verification_code
            )
            
        elif template_type == "verification_link":
            verification_link = test_data.get("verification_link", "https://flow.axiestudio.se/verify?token=test123")
            success = await email_service.send_verification_link_email(
                email=test_email,
                username=username,
                verification_link=verification_link
            )
            
        elif template_type == "password_reset":
            token = test_data.get("token", "test_reset_token_123")
            client_ip = test_data.get("client_ip", "192.168.1.100")
            success = await email_service.send_password_reset_email(
                email=test_email,
                username=username,
                token=token,
                client_ip=client_ip
            )
            
        elif template_type == "temporary_password":
            temp_password = test_data.get("temp_password", "TempPass123")
            client_ip = test_data.get("client_ip", "192.168.1.100")
            success = await email_service.send_temporary_password_email(
                email=test_email,
                username=username,
                temp_password=temp_password,
                client_ip=client_ip
            )
            
        elif template_type == "login_credentials":
            client_ip = test_data.get("client_ip", "192.168.1.100")
            success = await email_service.send_login_credentials_email(
                email=test_email,
                username=username,
                client_ip=client_ip
            )
            
        elif template_type == "new_login_detected":
            client_ip = test_data.get("client_ip", "192.168.1.100")
            location = test_data.get("location", "Stockholm, Sverige")
            device = test_data.get("device", "Chrome på Windows (Dator)")
            success = await email_service.send_new_login_detected_email(
                email=test_email,
                username=username,
                client_ip=client_ip,
                location=location,
                device=device
            )
            
        elif template_type == "trial_ending":
            days_left = test_data.get("days_left", 3)
            success = await email_service.send_trial_ending_email(
                email=test_email,
                username=username,
                days_left=days_left
            )
            
        elif template_type == "subscription_welcome":
            plan_name = test_data.get("plan_name", "Pro")
            success = await email_service.send_subscription_welcome_email(
                email=test_email,
                username=username,
                plan_name=plan_name
            )
            
        elif template_type == "subscription_cancelled":
            subscription_end_date = test_data.get("subscription_end_date", "15 december 2024")
            success = await email_service.send_subscription_cancelled_email(
                email=test_email,
                username=username,
                subscription_end_date=subscription_end_date
            )
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Okänd malltyp: {template_type}. Tillgängliga typer: verification_code, verification_link, password_reset, temporary_password, login_credentials, new_login_detected, trial_ending, subscription_welcome, subscription_cancelled"
            )
        
        if success:
            logger.info(f"✅ Test-e-post skickad: {template_type} till {test_email}")
            return EmailTemplateResponse(
                success=True,
                message=f"Test-e-post skickad framgångsrikt till {test_email}",
                template_type=template_type,
                recipient=test_email
            )
        else:
            logger.error(f"❌ Misslyckades att skicka test-e-post: {template_type} till {test_email}")
            raise HTTPException(
                status_code=500,
                detail="Misslyckades att skicka test-e-post. Kontrollera serverloggar för detaljer."
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fel vid testning av e-postmall: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internt serverfel: {str(e)}"
        )


@router.get("/available")
async def get_available_templates():
    """Get list of all available email templates."""
    return {
        "templates": [
            {
                "type": "verification_code",
                "name": "E-postverifiering (Kod)",
                "description": "6-siffrig verifieringskod för e-postverifiering",
                "test_data": {"verification_code": "123456"}
            },
            {
                "type": "verification_link", 
                "name": "E-postverifiering (Länk)",
                "description": "Verifieringslänk för e-postverifiering",
                "test_data": {"verification_link": "https://flow.axiestudio.se/verify?token=test123"}
            },
            {
                "type": "password_reset",
                "name": "Lösenordsåterställning",
                "description": "E-post för lösenordsåterställning med säker länk",
                "test_data": {"token": "test_reset_token", "client_ip": "192.168.1.100"}
            },
            {
                "type": "temporary_password",
                "name": "Tillfälligt lösenord",
                "description": "Tillfälligt lösenord för kontoåterställning",
                "test_data": {"temp_password": "TempPass123", "client_ip": "192.168.1.100"}
            },
            {
                "type": "login_credentials",
                "name": "Inloggningsuppgifter",
                "description": "Påminnelse om inloggningsuppgifter",
                "test_data": {"client_ip": "192.168.1.100"}
            },
            {
                "type": "new_login_detected",
                "name": "Ny inloggning upptäckt",
                "description": "Säkerhetsnotifiering för ny enhet/plats-inloggning",
                "test_data": {
                    "client_ip": "192.168.1.100",
                    "location": "Stockholm, Sverige", 
                    "device": "Chrome på Windows (Dator)"
                }
            },
            {
                "type": "trial_ending",
                "name": "Provperioden slutar",
                "description": "Notifiering när provperioden är på väg att löpa ut",
                "test_data": {"days_left": 3}
            },
            {
                "type": "subscription_welcome",
                "name": "Välkommen till prenumeration",
                "description": "Välkomstmail för nya prenumeranter",
                "test_data": {"plan_name": "Pro"}
            },
            {
                "type": "subscription_cancelled",
                "name": "Prenumeration avbruten",
                "description": "Bekräftelsemail för avbruten prenumeration",
                "test_data": {"subscription_end_date": "15 december 2024"}
            }
        ]
    }


@router.post("/test-login-detection")
async def test_login_detection(
    current_user: User = Depends(get_current_active_user),
    session: DbSession = None
):
    """Test the login detection system by simulating a new login."""
    try:
        login_detection = get_login_detection_service()
        
        # Simulate a login from a different IP/device
        test_ip = "203.0.113.1"  # Test IP address
        test_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        
        notification_sent = await login_detection.track_login(
            session=session,
            user=current_user,
            client_ip=test_ip,
            user_agent=test_user_agent
        )
        
        return {
            "success": True,
            "message": "Test av inloggningsdetektering slutförd",
            "notification_sent": notification_sent,
            "test_ip": test_ip,
            "user_agent": test_user_agent
        }
        
    except Exception as e:
        logger.error(f"Fel vid testning av inloggningsdetektering: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Test av inloggningsdetektering misslyckades: {str(e)}"
        )


@router.post("/test-trial-notifications")
async def test_trial_notifications(
    current_user: User = Depends(get_current_active_user),
    session: DbSession = None
):
    """Test the trial notification system."""
    try:
        trial_notification_service = get_trial_notification_service()
        
        # Send immediate trial notification for current user
        success = await trial_notification_service.send_immediate_trial_notification(
            session=session,
            user_id=current_user.id
        )
        
        return {
            "success": success,
            "message": "Test av provperiodsnotifieringar slutförd",
            "notification_sent": success,
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error(f"Fel vid testning av provperiodsnotifieringar: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Test av provperiodsnotifieringar misslyckades: {str(e)}"
        )


@router.get("/stats")
async def get_email_stats(
    current_user: User = Depends(get_current_active_user),
    session: DbSession = None
):
    """Get email and notification statistics."""
    try:
        trial_notification_service = get_trial_notification_service()
        
        # Get trial notification stats
        trial_stats = await trial_notification_service.get_notification_stats(session)
        
        return {
            "trial_notifications": trial_stats,
            "email_service": {
                "configured": True,  # Email service is always configured
                "methods": ["resend_sdk", "smtp"]
            }
        }
        
    except Exception as e:
        logger.error(f"Fel vid hämtning av e-poststatistik: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Misslyckades att hämta e-poststatistik: {str(e)}"
        )
