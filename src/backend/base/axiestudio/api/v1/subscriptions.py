"""Subscription API endpoints."""

import os
from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from loguru import logger

from axiestudio.api.utils import CurrentActiveUser, DbSession
from axiestudio.services.stripe.service import stripe_service
from axiestudio.services.database.models.user.crud import update_user
from axiestudio.services.database.models.user.model import UserUpdate

# Import subscription setup for manual migration
try:
    from axiestudio.services.startup.subscription_setup import setup_subscription_schema
    SUBSCRIPTION_SETUP_AVAILABLE = True
except ImportError:
    SUBSCRIPTION_SETUP_AVAILABLE = False


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
        # Create Stripe customer if not exists (handle missing column gracefully)
        stripe_customer_id = getattr(current_user, 'stripe_customer_id', None)
        if not stripe_customer_id:
            customer_id = await stripe_service.create_customer(
                email=current_user.username,  # Using username as email
                name=current_user.username
            )
            
            # Update user with Stripe customer ID
            update_data = UserUpdate(stripe_customer_id=customer_id)
            await update_user(session, current_user.id, update_data)
        else:
            customer_id = current_user.stripe_customer_id
        
        # Calculate remaining trial days (don't give double trial)
        now = datetime.now(timezone.utc)
        trial_end = current_user.trial_end or (current_user.trial_start + timedelta(days=7))

        # Only give Stripe trial if user's trial hasn't expired yet
        remaining_trial_days = 0
        if now < trial_end:
            remaining_trial_days = max(0, (trial_end - now).days)

        # Create checkout session with remaining trial days
        checkout_url = await stripe_service.create_checkout_session(
            customer_id=customer_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            trial_days=remaining_trial_days
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


@router.post("/migrate-schema")
async def migrate_subscription_schema():
    """Manually trigger subscription schema migration (for debugging)."""
    if not SUBSCRIPTION_SETUP_AVAILABLE:
        raise HTTPException(status_code=503, detail="Subscription setup not available")

    try:
        result = await setup_subscription_schema()
        return {
            "success": True,
            "message": "Subscription schema migration completed",
            "result": result
        }
    except Exception as e:
        logger.error(f"Manual schema migration failed: {e}")
        raise HTTPException(status_code=500, detail=f"Schema migration failed: {str(e)}")


@router.get("/debug/schema")
async def debug_database_schema(session: DbSession):
    """Debug endpoint to check what columns exist in the user table."""
    try:
        from sqlalchemy import text

        # Check if we're using SQLite or PostgreSQL
        db_url = str(session.bind.url).lower()
        is_sqlite = "sqlite" in db_url

        if is_sqlite:
            # SQLite: Check table schema
            result = await session.execute(text("PRAGMA table_info(user);"))
            rows = result.fetchall()
            columns = [{"name": row[1], "type": row[2], "nullable": bool(row[3]), "default": row[4]} for row in rows]
        else:
            # PostgreSQL: Check information_schema
            result = await session.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'user' AND table_schema = 'public'
                ORDER BY ordinal_position;
            """))
            rows = result.fetchall()
            columns = [{"name": row[0], "type": row[1], "nullable": row[2] == "YES", "default": row[3]} for row in rows]

        # Check which subscription columns are missing
        subscription_columns = [
            'stripe_customer_id', 'subscription_status', 'subscription_id',
            'trial_start', 'trial_end', 'subscription_start', 'subscription_end'
        ]

        existing_column_names = {col["name"] for col in columns}
        missing_columns = [col for col in subscription_columns if col not in existing_column_names]

        return {
            "database_type": "sqlite" if is_sqlite else "postgresql",
            "total_columns": len(columns),
            "all_columns": columns,
            "subscription_columns_missing": missing_columns,
            "subscription_columns_present": [col for col in subscription_columns if col in existing_column_names]
        }

    except Exception as e:
        logger.error(f"Error checking database schema: {e}")
        raise HTTPException(status_code=500, detail=f"Schema check failed: {str(e)}")


@router.get("/status")
async def get_subscription_status(current_user: CurrentActiveUser):
    """Get current user's subscription status."""
    try:
        # Handle missing subscription columns gracefully
        trial_start = getattr(current_user, 'trial_start', None)
        trial_end = getattr(current_user, 'trial_end', None)
        subscription_status = getattr(current_user, 'subscription_status', 'trial')
        subscription_id = getattr(current_user, 'subscription_id', None)
        subscription_start = getattr(current_user, 'subscription_start', None)
        subscription_end = getattr(current_user, 'subscription_end', None)
        stripe_customer_id = getattr(current_user, 'stripe_customer_id', None)

        # Calculate trial status
        trial_expired = False
        days_left = 7  # Default to 7 days if no trial_start

        if trial_start:
            trial_end_date = trial_end or (trial_start + timedelta(days=7))
            now = datetime.now(timezone.utc)

            if now > trial_end_date:
                trial_expired = True
                days_left = 0
            else:
                days_left = (trial_end_date - now).days
        else:
            # If no trial_start, assume user just signed up
            trial_start = current_user.create_at
            trial_end = trial_start + timedelta(days=7) if trial_start else None

        return {
            "subscription_status": subscription_status,
            "subscription_id": subscription_id,
            "trial_start": trial_start,
            "trial_end": trial_end,
            "trial_expired": trial_expired,
            "trial_days_left": max(0, days_left),
            "subscription_start": subscription_start,
            "subscription_end": subscription_end,
            "has_stripe_customer": bool(stripe_customer_id)
        }

    except Exception as e:
        logger.error(f"Error getting subscription status: {e}")
        # Return safe defaults if there's an error
        return {
            "subscription_status": "trial",
            "subscription_id": None,
            "trial_start": current_user.create_at,
            "trial_end": current_user.create_at + timedelta(days=7) if current_user.create_at else None,
            "trial_expired": False,
            "trial_days_left": 7,
            "subscription_start": None,
            "subscription_end": None,
            "has_stripe_customer": False
        }


@router.delete("/cancel")
async def cancel_subscription(
    current_user: CurrentActiveUser,
    session: DbSession,
):
    """Cancel current user's subscription."""
    if not stripe_service.is_configured():
        raise HTTPException(status_code=503, detail="Stripe is not configured. Please contact support.")

    try:
        if not current_user.subscription_id:
            raise HTTPException(status_code=400, detail="No active subscription found")

        # Cancel subscription in Stripe
        success = await stripe_service.cancel_subscription(current_user.subscription_id)

        if success:
            # Update user subscription status
            update_data = UserUpdate(subscription_status="canceled")
            await update_user(session, current_user.id, update_data)

            return {
                "status": "success",
                "message": "Subscription cancelled successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to cancel subscription")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel subscription: {str(e)}")


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
    if not stripe_service.is_configured():
        raise HTTPException(status_code=503, detail="Stripe is not configured. Please contact support.")

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
