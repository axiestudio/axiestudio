"""Subscription API endpoints."""

import os
from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel

from axiestudio.api.utils import CurrentActiveUser, DbSession
from axiestudio.services.stripe.service import stripe_service
from axiestudio.services.database.models.user.crud import update_user
from axiestudio.services.database.models.user.model import UserUpdate


router = APIRouter(tags=["Subscriptions"], prefix="/subscriptions")


class CreateCheckoutRequest(BaseModel):
    success_url: str
    cancel_url: str


class CheckoutResponse(BaseModel):
    checkout_url: str


class CustomerPortalResponse(BaseModel):
    portal_url: str


@router.post("/create-checkout", response_model=CheckoutResponse)
async def create_checkout_session(
    request: CreateCheckoutRequest,
    current_user: CurrentActiveUser,
    session: DbSession,
):
    """Create a Stripe checkout session for subscription."""
    if not stripe_service.is_configured():
        raise HTTPException(status_code=503, detail="Stripe is not configured. Please contact support.")

    try:
        # Create Stripe customer if not exists
        if not current_user.stripe_customer_id:
            customer_id = await stripe_service.create_customer(
                email=current_user.username,  # Using username as email
                name=current_user.username
            )
            
            # Update user with Stripe customer ID
            update_data = UserUpdate(stripe_customer_id=customer_id)
            await update_user(session, current_user.id, update_data)
        else:
            customer_id = current_user.stripe_customer_id
        
        # Create checkout session with 7-day trial
        checkout_url = await stripe_service.create_checkout_session(
            customer_id=customer_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            trial_days=7
        )
        
        return CheckoutResponse(checkout_url=checkout_url)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create checkout session: {str(e)}")


@router.post("/customer-portal", response_model=CustomerPortalResponse)
async def create_customer_portal(
    current_user: CurrentActiveUser,
    session: DbSession,
):
    """Create a Stripe customer portal session."""
    if not stripe_service.is_configured():
        raise HTTPException(status_code=503, detail="Stripe is not configured. Please contact support.")

    try:
        # Create Stripe customer if not exists
        if not current_user.stripe_customer_id:
            customer_id = await stripe_service.create_customer(
                email=current_user.username,  # Using username as email
                name=current_user.username
            )

            # Update user with Stripe customer ID
            update_data = UserUpdate(stripe_customer_id=customer_id)
            await update_user(session, current_user.id, update_data)
        else:
            customer_id = current_user.stripe_customer_id

        # Get the frontend URL from environment or use default
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:7860")
        return_url = f"{frontend_url}/settings"

        portal_url = await stripe_service.create_customer_portal_session(
            customer_id=customer_id,
            return_url=return_url
        )
        
        return CustomerPortalResponse(portal_url=portal_url)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create customer portal: {str(e)}")


@router.get("/health")
async def subscription_health():
    """Check if subscription service is healthy."""
    return {
        "stripe_configured": stripe_service.is_configured(),
        "service_status": "healthy"
    }


@router.get("/status")
async def get_subscription_status(current_user: CurrentActiveUser):
    """Get current user's subscription status."""
    try:
        # Calculate trial status
        trial_expired = False
        days_left = 0
        
        if current_user.trial_start:
            trial_end = current_user.trial_end or (current_user.trial_start + timedelta(days=7))
            now = datetime.now(timezone.utc)
            
            if now > trial_end:
                trial_expired = True
            else:
                days_left = (trial_end - now).days
        
        return {
            "subscription_status": current_user.subscription_status or "trial",
            "subscription_id": current_user.subscription_id,
            "trial_start": current_user.trial_start,
            "trial_end": current_user.trial_end,
            "trial_expired": trial_expired,
            "trial_days_left": max(0, days_left),
            "subscription_start": current_user.subscription_start,
            "subscription_end": current_user.subscription_end,
            "has_stripe_customer": bool(current_user.stripe_customer_id)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get subscription status: {str(e)}")


@router.post("/webhook")
async def stripe_webhook(request: Request, session: DbSession):
    """Handle Stripe webhook events."""
    try:
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        
        if not webhook_secret:
            raise HTTPException(status_code=500, detail="Webhook secret not configured")
        
        # Verify webhook signature
        import stripe
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Handle the event
        success = await stripe_service.handle_webhook_event(event, session)
        
        if success:
            return {"status": "success"}
        else:
            raise HTTPException(status_code=500, detail="Failed to process webhook")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook error: {str(e)}")


@router.delete("/cancel")
async def cancel_subscription(
    current_user: CurrentActiveUser,
    session: DbSession,
):
    """Cancel current user's subscription."""
    try:
        if not current_user.subscription_id:
            raise HTTPException(status_code=400, detail="No active subscription found")
        
        success = await stripe_service.cancel_subscription(current_user.subscription_id)
        
        if success:
            # Update user status
            update_data = UserUpdate(
                subscription_status="canceled",
                subscription_id=None
            )
            await update_user(session, current_user.id, update_data)
            
            return {"status": "success", "message": "Subscription cancelled"}
        else:
            raise HTTPException(status_code=500, detail="Failed to cancel subscription")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel subscription: {str(e)}")
