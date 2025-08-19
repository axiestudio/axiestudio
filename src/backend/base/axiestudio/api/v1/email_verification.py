from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query, Depends
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
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
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
    
    return {
        "message": "Email verified successfully! You can now log in to your account.",
        "verified": True
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
):
    """Send password reset email."""
    # Find user by email
    stmt = select(User).where(User.email == request.email)
    user = (await session.exec(stmt)).first()

    # Always return success to prevent email enumeration attacks
    success_response = {
        "message": "If an account with that email exists, a password reset link has been sent.",
        "email": request.email
    }

    if not user:
        # Don't reveal that the user doesn't exist
        return success_response

    if not user.is_active:
        # Don't send reset emails to inactive users
        return success_response

    # Generate password reset token (reuse verification token logic)
    reset_token = email_service.generate_verification_token()
    reset_expiry = email_service.get_verification_expiry()  # 24 hours

    # Store reset token in email_verification_token field (we'll reuse this field)
    user.email_verification_token = reset_token
    user.email_verification_expires = reset_expiry
    user.updated_at = datetime.now(timezone.utc)

    await session.commit()

    # Send password reset email
    email_sent = await email_service.send_password_reset_email(user.email, user.username, reset_token)

    if not email_sent:
        # Log error but still return success to prevent enumeration
        from loguru import logger
        logger.error(f"Failed to send password reset email to {user.email}")

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
    tokens = await create_user_tokens(user.id, session)

    return {
        "message": "Password reset successful! You are now logged in. Please go to Settings to change your password.",
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "user_id": str(user.id),
        "username": user.username,
        "redirect_to_settings": True
    }
