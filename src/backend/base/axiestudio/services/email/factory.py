"""
Email Service Factory
Provides intelligent selection between SMTP and Resend SDK based on configuration
"""

from typing import Union
from loguru import logger

from axiestudio.services.settings.email import EmailSettings
from axiestudio.services.email.service import EmailService
from axiestudio.services.email.resend_service import ResendEmailService


class EmailServiceFactory:
    """
    Factory class for creating the appropriate email service instance.
    
    Automatically selects between SMTP and Resend SDK based on configuration:
    - If USE_RESEND_SDK=true and RESEND_API_KEY is set: Use ResendEmailService
    - Otherwise: Use traditional SMTP EmailService
    """
    
    @staticmethod
    def create_email_service() -> Union[EmailService, ResendEmailService]:
        """
        Create and return the appropriate email service instance.
        
        Returns:
            EmailService or ResendEmailService based on configuration
        """
        settings = EmailSettings()

        # Enhanced logging for production deployment visibility
        logger.info("=" * 80)
        logger.info("🚀 EMAIL SERVICE FACTORY - INITIALIZING EMAIL SERVICE")
        logger.info("=" * 80)

        logger.info(f"📋 Email Service Configuration Analysis:")
        logger.info(f"   USE_RESEND_SDK: {settings.USE_RESEND_SDK}")
        logger.info(f"   RESEND_API_KEY configured: {bool(settings.RESEND_API_KEY)}")
        logger.info(f"   FROM_EMAIL: {settings.FROM_EMAIL}")
        logger.info(f"   FROM_NAME: {settings.FROM_NAME}")

        # Check if Resend SDK should be used
        if settings.USE_RESEND_SDK and settings.RESEND_API_KEY:
            logger.info("🎯 DECISION: Using Resend SDK as PRIMARY email service")
            logger.info("✅ RESEND SDK IS THE PRIMARY EMAIL METHOD")
            logger.info("❌ SMTP is NOT being used (Resend SDK replaced SMTP)")
            logger.info("🔧 Initializing ResendEmailService...")

            try:
                service = ResendEmailService()
                logger.info("✅ ResendEmailService initialized successfully")
                logger.info("🚀 PRODUCTION STATUS: Resend SDK is ACTIVE and READY")
                logger.info("=" * 80)
                return service
            except Exception as e:
                logger.error(f"❌ Failed to initialize ResendEmailService: {e}")
                logger.error("🔄 Falling back to SMTP EmailService")
                logger.info("=" * 80)
                return EmailService()
        else:
            logger.warning("⚠️ DECISION: Using SMTP for email service")
            logger.warning("❌ RESEND SDK IS NOT PRIMARY - Check configuration!")

            if not settings.USE_RESEND_SDK:
                logger.warning("   Reason: USE_RESEND_SDK is not set to 'true'")
            if not settings.RESEND_API_KEY:
                logger.warning("   Reason: RESEND_API_KEY is not configured")

            logger.info("🔧 Initializing SMTP EmailService...")
            logger.info("=" * 80)
            return EmailService()
    
    @staticmethod
    def get_service_info() -> dict:
        """
        Get information about which email service would be created.
        
        Returns:
            Dictionary with service information
        """
        settings = EmailSettings()
        
        if settings.USE_RESEND_SDK and settings.RESEND_API_KEY:
            return {
                "service_type": "resend_sdk",
                "class_name": "ResendEmailService",
                "api_key_configured": bool(settings.RESEND_API_KEY),
                "from_email": settings.FROM_EMAIL,
                "use_resend_sdk": settings.USE_RESEND_SDK
            }
        else:
            return {
                "service_type": "smtp",
                "class_name": "EmailService",
                "smtp_host": settings.SMTP_HOST,
                "smtp_port": settings.SMTP_PORT,
                "smtp_user": settings.SMTP_USER,
                "from_email": settings.FROM_EMAIL,
                "use_resend_sdk": settings.USE_RESEND_SDK,
                "fallback_reason": "RESEND_API_KEY not configured" if settings.USE_RESEND_SDK else "USE_RESEND_SDK=false"
            }


# Global email service instance (singleton pattern)
_email_service_instance = None


def get_email_service() -> Union[EmailService, ResendEmailService]:
    """
    Get the global email service instance (singleton).
    
    Returns:
        The configured email service instance
    """
    global _email_service_instance
    
    if _email_service_instance is None:
        _email_service_instance = EmailServiceFactory.create_email_service()
        logger.info(f"EMAIL FACTORY - Initialized global email service: {type(_email_service_instance).__name__}")
    
    return _email_service_instance


def reset_email_service():
    """
    Reset the global email service instance.
    Useful for testing or when configuration changes.
    """
    global _email_service_instance
    _email_service_instance = None
    logger.info("EMAIL FACTORY - Reset global email service instance")


def health_check_all_services() -> dict:
    """
    Perform health check on all available email services.
    
    Returns:
        Dictionary with health status of all services
    """
    results = {
        "factory_info": EmailServiceFactory.get_service_info(),
        "services": {}
    }
    
    # Check SMTP service
    try:
        smtp_service = EmailService()
        results["services"]["smtp"] = smtp_service.health_check()
    except Exception as e:
        results["services"]["smtp"] = {
            "service": "smtp",
            "status": "error",
            "error": str(e)
        }
    
    # Check Resend service if configured
    settings = EmailSettings()
    if settings.RESEND_API_KEY:
        try:
            resend_service = ResendEmailService()
            results["services"]["resend"] = resend_service.health_check()
        except Exception as e:
            results["services"]["resend"] = {
                "service": "resend",
                "status": "error",
                "error": str(e)
            }
    else:
        results["services"]["resend"] = {
            "service": "resend",
            "status": "not_configured",
            "message": "RESEND_API_KEY not configured"
        }
    
    return results
