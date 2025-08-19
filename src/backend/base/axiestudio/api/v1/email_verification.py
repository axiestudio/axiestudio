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
