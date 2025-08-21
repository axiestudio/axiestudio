from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlmodel import select
from pydantic import BaseModel

from axiestudio.api.utils import DbSession
from axiestudio.services.database.models.user.model import User
from axiestudio.services.email.service import email_service

router = APIRouter(prefix="/email", tags=["Email Verification"])


class ResendEmailRequest(BaseModel):
    email: str


class ForgotPasswordRequest(BaseModel):
    email: str


@router.get("/verify")
async def verify_email(
    session: DbSession,
    token: str = Query(..., description="Email verification token"),
):
    """Verify email address using token."""
    if not token:
        raise HTTPException(status_code=400, detail="Verification token is required")
    
    # Find user by verification token
    stmt = select(User).where(User.email_verification_token == token)
    user = (await session.exec(stmt)).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired verification token. If you already verified your email, please try logging in directly."
        )
    
    # Check if token has expired
    if user.email_verification_expires and user.email_verification_expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Verification token has expired")
    
    # Verify the user
    user.email_verified = True
    user.is_active = True  # Activate the user
    user.email_verification_token = None  # Clear the token
    user.email_verification_expires = None  # Clear expiry
    user.updated_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(user)

    # Generate access token for automatic login
    from axiestudio.services.auth.utils import create_user_tokens
    tokens = await create_user_tokens(user.id, session, update_last_login=True)

    return {
        "message": "Email verified successfully! You are now logged in.",
        "verified": True,
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "user_id": str(user.id),
        "username": user.username,
        "auto_login": True
    }


@router.post("/resend-verification")
async def resend_verification_email(
    request: ResendEmailRequest,
    session: DbSession,
):
    """Resend verification email."""
    # Find user by email
    stmt = select(User).where(User.email == request.email)
    user = (await session.exec(stmt)).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email_verified:
        raise HTTPException(status_code=400, detail="Email is already verified")
    
    # Generate new verification token
    token = email_service.generate_verification_token()
    expiry = email_service.get_verification_expiry()
    
    # Update user with new token
    user.email_verification_token = token
    user.email_verification_expires = expiry
    user.updated_at = datetime.now(timezone.utc)
    
    await session.commit()
    
    # Send verification email
    email_sent = await email_service.send_verification_email(user.email, user.username, token)
    
    if not email_sent:
        raise HTTPException(status_code=500, detail="Failed to send verification email")
    
    return {
        "message": "Verification email sent successfully",
        "email": user.email
    }


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    session: DbSession,
    http_request: Request,
):
    """Send password reset email with enterprise security features."""
    from loguru import logger

    # Get client IP for security logging
    client_ip = http_request.client.host if http_request.client else "unknown"

    # Find user by email
    stmt = select(User).where(User.email == request.email)
    user = (await session.exec(stmt)).first()

    # Always return success to prevent email enumeration attacks
    success_response = {
        "message": "If an account with that email exists, a password reset link has been sent.",
        "email": request.email,
        "security_notice": "For security reasons, we don't confirm whether this email exists in our system."
    }

    if not user:
        # Log suspicious activity for security monitoring
        logger.warning(f"Password reset attempted for non-existent email: {request.email} from IP: {client_ip}")
        return success_response

    if not user.is_active:
        # Log inactive user reset attempts
        logger.info(f"Password reset attempted for inactive user: {user.username} from IP: {client_ip}")
        return success_response

    # Check for recent reset attempts (rate limiting)
    if user.email_verification_expires and user.email_verification_expires > datetime.now(timezone.utc):
        time_remaining = user.email_verification_expires - datetime.now(timezone.utc)
        if time_remaining.total_seconds() > 23 * 3600:  # If less than 1 hour since last request
            logger.warning(f"Rate limited password reset for user: {user.username} from IP: {client_ip}")
            return {
                "message": "A password reset link was recently sent. Please check your email or wait before requesting another.",
                "email": request.email,
                "rate_limited": True
            }

    # Generate password reset token with enhanced security
    reset_token = email_service.generate_verification_token()
    reset_expiry = email_service.get_verification_expiry()  # 24 hours

    # Store reset token and security metadata
    user.email_verification_token = reset_token
    user.email_verification_expires = reset_expiry
    user.updated_at = datetime.now(timezone.utc)

    # Log successful reset request for security audit
    logger.info(f"Password reset requested for user: {user.username} from IP: {client_ip}")

    await session.commit()

    # Send password reset email with enhanced template
    email_sent = await email_service.send_password_reset_email(
        user.email,
        user.username,
        reset_token,
        client_ip=client_ip  # Pass IP for security notice in email
    )

    if not email_sent:
        # Log error but still return success to prevent enumeration
        logger.error(f"Failed to send password reset email to {user.email} from IP: {client_ip}")

    return success_response


@router.get("/reset-password")
async def reset_password(
    session: DbSession,
    token: str = Query(..., description="Password reset token"),
):
    """Handle password reset token and log user in automatically."""
    if not token:
        raise HTTPException(status_code=400, detail="Reset token is required")

    # Find user by reset token (stored in email_verification_token field)
    stmt = select(User).where(User.email_verification_token == token)
    user = (await session.exec(stmt)).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    # Check if token has expired
    if user.email_verification_expires and user.email_verification_expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset token has expired")

    # Activate the user if they're not active (password reset also serves as email verification)
    if not user.is_active:
        user.is_active = True
        user.email_verified = True  # Mark email as verified since they accessed the reset link

    # Clear the reset token
    user.email_verification_token = None
    user.email_verification_expires = None
    user.updated_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(user)

    # Generate access token for automatic login
    from axiestudio.services.auth.utils import create_user_tokens
    tokens = await create_user_tokens(user.id, session, update_last_login=True)

    return {
        "message": "Password reset successful! You are now logged in. Please go to Settings to change your password.",
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "user_id": str(user.id),
        "username": user.username,
        "redirect_to_settings": True
    }
