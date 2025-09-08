"""Subscription API endpoints."""

import os
from datetime import datetime, timezone, timedelta
from typing import Annotated
from collections import defaultdict
import time

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query
from pydantic import BaseModel
from loguru import logger

from axiestudio.api.utils import CurrentActiveUser, DbSession
from axiestudio.services.auth.utils import get_current_active_user
from axiestudio.services.deps import get_session
from axiestudio.services.stripe.service import stripe_service
from axiestudio.services.database.models.user.crud import update_user
from axiestudio.services.database.models.user.model import UserUpdate

# Import subscription setup for manual migration
try:
    from axiestudio.services.startup.subscription_setup import setup_subscription_schema
    SUBSCRIPTION_SETUP_AVAILABLE = True
except ImportError:
    SUBSCRIPTION_SETUP_AVAILABLE = False

# Simple rate limiting for subscription endpoints
_rate_limit_store = defaultdict(list)
RATE_LIMIT_WINDOW = 300  # 5 minutes
RATE_LIMIT_MAX_REQUESTS = 10  # Max 10 subscription requests per 5 minutes per user

def check_rate_limit(user_id: str, endpoint: str) -> bool:
    """Check if user has exceeded rate limit for subscription endpoints."""
    now = time.time()
    key = f"{user_id}:{endpoint}"

    # Clean old entries
    _rate_limit_store[key] = [
        timestamp for timestamp in _rate_limit_store[key]
        if now - timestamp < RATE_LIMIT_WINDOW
    ]

    # Check if limit exceeded
    if len(_rate_limit_store[key]) >= RATE_LIMIT_MAX_REQUESTS:
        return False

    # Add current request
    _rate_limit_store[key].append(now)
    return True

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
    # Rate limiting check
    if not check_rate_limit(str(current_user.id), "create-checkout"):
        raise HTTPException(
            status_code=429,
            detail="För många prenumerationsförfrågningar. Vänligen vänta några minuter innan du försöker igen."
        )

    if not stripe_service.is_configured():
        raise HTTPException(status_code=503, detail="Stripe är inte konfigurerat. Vänligen kontakta support.")

    try:
        # Create Stripe customer if not exists
        stripe_customer_id = getattr(current_user, 'stripe_customer_id', None)
        if not stripe_customer_id:
            # Use user's email (handle case where email might be None for existing users)
            user_email = current_user.email
            if not user_email:
                raise HTTPException(
                    status_code=400,
                    detail="E-postadress krävs för prenumeration. Vänligen uppdatera din profil med en giltig e-postadress."
                )

            customer_id = await stripe_service.create_customer(
                email=user_email,
                name=current_user.username
            )
            
            # Update user with Stripe customer ID
            update_data = UserUpdate(stripe_customer_id=customer_id)
            await update_user(session, current_user.id, update_data)
        else:
            customer_id = current_user.stripe_customer_id
        
        # Calculate remaining trial days (don't give double trial)
        now = datetime.now(timezone.utc)

        # Handle trial dates safely with timezone consistency
        trial_start = getattr(current_user, 'trial_start', None)
        trial_end = getattr(current_user, 'trial_end', None)

        # CRITICAL FIX: Ensure all datetime objects are timezone-aware
        if trial_start is None:
            trial_start = now
        elif trial_start.tzinfo is None:
            trial_start = trial_start.replace(tzinfo=timezone.utc)

        if trial_end is None:
            trial_end = trial_start + timedelta(days=7)
        elif trial_end.tzinfo is None:
            trial_end = trial_end.replace(tzinfo=timezone.utc)

        # FIXED: Proper trial logic for expired vs active users
        remaining_trial_days = 0
        if trial_end and now < trial_end:
            # User still has active trial - give them remaining days
            remaining_seconds = (trial_end - now).total_seconds()
            remaining_trial_days = max(1, int(remaining_seconds / 86400))  # Minimum 1 day for Stripe
        else:
            # User's trial is expired or they have no trial - NO TRIAL, direct payment
            remaining_trial_days = 0

        # Create checkout session with remaining trial days
        checkout_url = await stripe_service.create_checkout_session(
            customer_id=customer_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            trial_days=remaining_trial_days
        )
        
        return CheckoutResponse(checkout_url=checkout_url)
        
    except Exception as e:
        logger.error(f"Failed to create checkout session for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Misslyckades med att skapa checkout-session. Vänligen försök igen eller kontakta support.")


@router.post("/customer-portal", response_model=CustomerPortalResponse)
async def create_customer_portal(
    current_user: CurrentActiveUser,
    session: DbSession,
):
    """Create a Stripe customer portal session."""
    # Rate limiting check
    if not check_rate_limit(str(current_user.id), "customer-portal"):
        raise HTTPException(
            status_code=429,
            detail="För många portalförfrågningar. Vänligen vänta några minuter innan du försöker igen."
        )

    if not stripe_service.is_configured():
        raise HTTPException(status_code=503, detail="Stripe är inte konfigurerat. Vänligen kontakta support.")

    try:
        # Create Stripe customer if not exists
        if not current_user.stripe_customer_id:
            # Use user's email (handle case where email might be None for existing users)
            user_email = current_user.email
            if not user_email:
                raise HTTPException(
                    status_code=400,
                    detail="E-postadress krävs för kundportal. Vänligen uppdatera din profil med en giltig e-postadress."
                )

            customer_id = await stripe_service.create_customer(
                email=user_email,
                name=current_user.username
            )

            # Update user with Stripe customer ID
            update_data = UserUpdate(stripe_customer_id=customer_id)
            await update_user(session, current_user.id, update_data)
        else:
            customer_id = current_user.stripe_customer_id

        # Get the frontend URL from environment or use default
        # Try multiple environment variables for different deployment platforms
        frontend_url = (
            os.getenv("FRONTEND_URL") or
            os.getenv("RAILWAY_PUBLIC_DOMAIN") and f"https://{os.getenv('RAILWAY_PUBLIC_DOMAIN')}" or
            os.getenv("VERCEL_URL") and f"https://{os.getenv('VERCEL_URL')}" or
            os.getenv("RENDER_EXTERNAL_URL") or
            "http://localhost:7860"
        )
        return_url = f"{frontend_url}/settings"

        logger.info(f"Creating customer portal with return_url: {return_url}")
        logger.debug(f"Environment variables - FRONTEND_URL: {os.getenv('FRONTEND_URL')}, RAILWAY_PUBLIC_DOMAIN: {os.getenv('RAILWAY_PUBLIC_DOMAIN')}")

        portal_url = await stripe_service.create_customer_portal_session(
            customer_id=customer_id,
            return_url=return_url
        )
        
        return CustomerPortalResponse(portal_url=portal_url)
        
    except Exception as e:
        logger.error(f"Failed to create customer portal for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Misslyckades med att skapa kundportal. Vänligen försök igen eller kontakta support.")


@router.get("/health")
async def subscription_health():
    """Check if subscription service is healthy."""
    return {
        "stripe_configured": stripe_service.is_configured(),
        "service_status": "healthy"
    }


@router.post("/migrate-schema")
async def migrate_subscription_schema(session: DbSession):
    """Manually trigger subscription schema migration."""
    try:
        from sqlalchemy import text

        logger.info("Starting manual subscription schema migration...")

        # Check database type
        db_url = str(session.bind.url).lower()
        is_sqlite = "sqlite" in db_url

        # Check existing columns
        if is_sqlite:
            result = await session.exec(text("PRAGMA table_info(user);"))
            existing_columns = {row[1] for row in result.fetchall()}
        else:
            result = await session.exec(text("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'user' AND table_schema = 'public';
            """))
            existing_columns = {row[0] for row in result.fetchall()}

        # Define subscription columns
        subscription_columns = [
            ('stripe_customer_id', 'VARCHAR(255)'),
            ('subscription_status', "VARCHAR(50) DEFAULT 'trial'"),
            ('subscription_id', 'VARCHAR(255)'),
            ('trial_start', 'TIMESTAMP'),
            ('trial_end', 'TIMESTAMP'),
            ('subscription_start', 'TIMESTAMP'),
            ('subscription_end', 'TIMESTAMP')
        ]

        added_columns = []
        errors = []

        # Add missing columns
        for column_name, column_def in subscription_columns:
            if column_name not in existing_columns:
                try:
                    if is_sqlite:
                        sql = f"ALTER TABLE user ADD COLUMN {column_name} {column_def};"
                    else:
                        sql = f'ALTER TABLE "user" ADD COLUMN {column_name} {column_def};'

                    await session.exec(text(sql))
                    added_columns.append(column_name)
                    logger.info(f"Added column: {column_name}")
                except Exception as e:
                    error_msg = f"Failed to add {column_name}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(error_msg)

        # Commit changes
        if added_columns:
            await session.commit()

            # Update existing users
            try:
                if is_sqlite:
                    update_sql = """
                        UPDATE user SET
                            trial_start = COALESCE(trial_start, create_at),
                            trial_end = COALESCE(trial_end, datetime(create_at, '+7 days')),
                            subscription_status = COALESCE(subscription_status, 'trial')
                        WHERE trial_start IS NULL OR subscription_status IS NULL;
                    """
                else:
                    update_sql = """
                        UPDATE "user" SET
                            trial_start = COALESCE(trial_start, create_at),
                            trial_end = COALESCE(trial_end, create_at + INTERVAL '7 days'),
                            subscription_status = COALESCE(subscription_status, 'trial')
                        WHERE trial_start IS NULL OR subscription_status IS NULL;
                    """

                await session.exec(text(update_sql))
                await session.commit()
                logger.info("Updated existing users with trial defaults")
            except Exception as e:
                errors.append(f"Failed to update users: {str(e)}")

        return {
            "success": len(errors) == 0,
            "database_type": "sqlite" if is_sqlite else "postgresql",
            "existing_columns": sorted(existing_columns),
            "added_columns": added_columns,
            "errors": errors,
            "message": f"Added {len(added_columns)} columns" if added_columns else "All columns already exist"
        }

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise HTTPException(status_code=500, detail=f"Migrering misslyckades: {str(e)}")


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
            result = await session.exec(text("PRAGMA table_info(user);"))
            rows = result.fetchall()
            columns = [{"name": row[1], "type": row[2], "nullable": bool(row[3]), "default": row[4]} for row in rows]
        else:
            # PostgreSQL: Check information_schema
            result = await session.exec(text("""
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
        raise HTTPException(status_code=500, detail=f"Schemakontroll misslyckades: {str(e)}")


@router.get("/status")
async def get_subscription_status(current_user: CurrentActiveUser):
    """Get current user's subscription status."""
    try:
        # Superusers don't have subscriptions - they have unlimited access
        if current_user.is_superuser:
            return {
                "subscription_status": "admin",
                "subscription_id": None,
                "trial_start": None,
                "trial_end": None,
                "trial_expired": False,
                "trial_days_left": None,
                "subscription_start": None,
                "subscription_end": None,
                "has_stripe_customer": False,
                "is_superuser": True
            }

        # Handle missing subscription columns gracefully
        trial_start = getattr(current_user, 'trial_start', None)
        trial_end = getattr(current_user, 'trial_end', None)
        subscription_status = getattr(current_user, 'subscription_status', 'trial')
        subscription_id = getattr(current_user, 'subscription_id', None)
        subscription_start = getattr(current_user, 'subscription_start', None)
        subscription_end = getattr(current_user, 'subscription_end', None)
        stripe_customer_id = getattr(current_user, 'stripe_customer_id', None)

        # CRITICAL FIX: Ensure timezone awareness for subscription dates
        if subscription_start and subscription_start.tzinfo is None:
            subscription_start = subscription_start.replace(tzinfo=timezone.utc)
        if subscription_end and subscription_end.tzinfo is None:
            subscription_end = subscription_end.replace(tzinfo=timezone.utc)

        # Calculate trial status
        trial_expired = False
        days_left = 7  # Default to 7 days if no trial_start

        if trial_start:
            trial_end_date = trial_end or (trial_start + timedelta(days=7))
            now = datetime.now(timezone.utc)

            # Ensure timezone consistency for comparisons
            if trial_start.tzinfo is None:
                trial_start = trial_start.replace(tzinfo=timezone.utc)
            if trial_end_date.tzinfo is None:
                trial_end_date = trial_end_date.replace(tzinfo=timezone.utc)

            if now > trial_end_date:
                trial_expired = True
                days_left = 0
            else:
                # FIXED: Use total_seconds() for accurate days calculation
                remaining_seconds = (trial_end_date - now).total_seconds()
                days_left = max(0, int(remaining_seconds / 86400))  # 86400 seconds = 1 day
        else:
            # If no trial_start, assume user just signed up
            trial_start = current_user.create_at
            if trial_start:
                # CRITICAL FIX: Ensure timezone awareness for create_at
                if trial_start.tzinfo is None:
                    trial_start = trial_start.replace(tzinfo=timezone.utc)
                trial_end = trial_start + timedelta(days=7)
            else:
                # Fallback if create_at is somehow None
                trial_start = datetime.now(timezone.utc)
                trial_end = trial_start + timedelta(days=7)

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
        # Return safe defaults if there's an error with proper timezone handling
        safe_create_at = current_user.create_at
        if safe_create_at and safe_create_at.tzinfo is None:
            safe_create_at = safe_create_at.replace(tzinfo=timezone.utc)
        elif not safe_create_at:
            safe_create_at = datetime.now(timezone.utc)

        return {
            "subscription_status": "trial",
            "subscription_id": None,
            "trial_start": safe_create_at,
            "trial_end": safe_create_at + timedelta(days=7),
            "trial_expired": False,
            "trial_days_left": 7,
            "subscription_start": None,
            "subscription_end": None,
            "has_stripe_customer": False
        }


@router.post("/webhook")
async def stripe_webhook(request: Request, session: DbSession):
    """Handle Stripe webhook events."""
    try:
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        
        if not webhook_secret:
            raise HTTPException(status_code=500, detail="Webhook-hemlighet inte konfigurerad")
        
        # Verify webhook signature
        import stripe
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Ogiltig nyttolast")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Ogiltig signatur")
        
        # Handle the event
        success = await stripe_service.handle_webhook_event(event, session)
        
        if success:
            return {"status": "success"}
        else:
            raise HTTPException(status_code=500, detail="Misslyckades med att bearbeta webhook")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook-fel: {str(e)}")


@router.delete("/cancel")
async def cancel_subscription(
    current_user: CurrentActiveUser,
    session: DbSession,
):
    """Cancel current user's subscription."""
    if not stripe_service.is_configured():
        raise HTTPException(status_code=503, detail="Stripe är inte konfigurerat. Vänligen kontakta support.")

    try:
        if not current_user.subscription_id:
            raise HTTPException(status_code=400, detail="Ingen aktiv prenumeration hittades")

        cancel_result = await stripe_service.cancel_subscription(current_user.subscription_id)

        if cancel_result["success"]:
            # CRITICAL FIX: Update user status with subscription end date but KEEP subscription_id
            # This allows users to maintain access until the billing period ends
            update_data = UserUpdate(
                subscription_status="canceled",
                subscription_end=cancel_result.get("subscription_end")
                # IMPORTANT: Do NOT set subscription_id=None here - keep it until subscription actually ends
            )
            await update_user(session, current_user.id, update_data)

            # Send subscription cancellation email (Swedish)
            if current_user.email:
                try:
                    from axiestudio.services.email.service import EmailService
                    email_service = EmailService()

                    # Format subscription end date for email
                    subscription_end_date = "okänt datum"
                    if cancel_result.get("subscription_end"):
                        subscription_end_date = cancel_result["subscription_end"].strftime("%d %B %Y")

                    await email_service.send_subscription_cancelled_email(
                        email=current_user.email,
                        username=current_user.username,
                        subscription_end_date=subscription_end_date
                    )
                    logger.info(f"✅ Sent subscription cancellation email to {current_user.username}")
                except Exception as e:
                    logger.error(f"❌ Failed to send subscription cancellation email to {current_user.username}: {e}")

            return {
                "status": "success",
                "message": "Prenumeration avbruten. Du behåller åtkomst till slutet av din nuvarande faktureringsperiod.",
                "subscription_end": cancel_result.get("subscription_end").isoformat() if cancel_result.get("subscription_end") else None
            }
        else:
            raise HTTPException(status_code=500, detail="Misslyckades med att avbryta prenumeration")

    except Exception as e:
        logger.error(f"Failed to cancel subscription for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Misslyckades med att avbryta prenumeration. Vänligen försök igen eller kontakta support.")


@router.post("/reactivate")
async def reactivate_subscription(
    current_user: CurrentActiveUser,
    session: DbSession,
):
    """
    🔄 ROBUST SUBSCRIPTION REACTIVATION ENDPOINT

    Reactivates a canceled subscription with comprehensive validation and error handling.
    Handles all edge cases and provides detailed error messages.
    """
    # Rate limiting check
    if not check_rate_limit(str(current_user.id), "reactivate-subscription"):
        raise HTTPException(
            status_code=429,
            detail="För många återaktiveringsförfrågningar. Vänligen vänta några minuter innan du försöker igen."
        )

    if not stripe_service.is_configured():
        raise HTTPException(status_code=503, detail="Stripe är inte konfigurerat. Vänligen kontakta support.")

    try:
        # COMPREHENSIVE VALIDATION

        # Check if user has any subscription
        if not current_user.subscription_id:
            logger.warning(f"Reactivation attempt by user {current_user.id} with no subscription_id")
            raise HTTPException(
                status_code=400,
                detail="Ingen prenumeration hittades. Du behöver först skapa en prenumeration."
            )

        # Check if subscription is actually canceled
        if current_user.subscription_status != "canceled":
            logger.warning(f"Reactivation attempt by user {current_user.id} with status: {current_user.subscription_status}")

            if current_user.subscription_status == "active":
                raise HTTPException(
                    status_code=400,
                    detail="Din prenumeration är redan aktiv. Ingen återaktivering behövs."
                )
            elif current_user.subscription_status == "trial":
                raise HTTPException(
                    status_code=400,
                    detail="Du är för närvarande på en provperiod. Återaktivering är inte tillämplig."
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Prenumerationen kan inte återaktiveras från status: {current_user.subscription_status}"
                )

        # Check if subscription has expired (can't reactivate expired subscriptions)
        if current_user.subscription_end:
            now = datetime.now(timezone.utc)
            subscription_end = current_user.subscription_end

            # CRITICAL FIX: Ensure timezone awareness for subscription_end
            if subscription_end.tzinfo is None:
                subscription_end = subscription_end.replace(tzinfo=timezone.utc)

            if now >= subscription_end:
                logger.warning(f"Reactivation attempt by user {current_user.id} for expired subscription (ended: {subscription_end})")
                raise HTTPException(
                    status_code=400,
                    detail="Prenumerationen har redan löpt ut och kan inte återaktiveras. Vänligen skapa en ny prenumeration."
                )

        # STRIPE REACTIVATION
        logger.info(f"Attempting to reactivate subscription {current_user.subscription_id} for user {current_user.id}")
        reactivate_result = await stripe_service.reactivate_subscription(current_user.subscription_id)

        if reactivate_result.get("success"):
            # DATABASE UPDATE
            update_data = UserUpdate(
                subscription_status="active",
                subscription_end=reactivate_result.get("subscription_end")
            )
            await update_user(session, current_user.id, update_data)
            logger.info(f"✅ Updated user {current_user.id} status to active")

            # EMAIL NOTIFICATION (Non-blocking)
            if current_user.email:
                try:
                    from axiestudio.services.email.service import EmailService
                    email_service = EmailService()

                    # Format subscription end date for email
                    subscription_end_date = "okänt datum"
                    if reactivate_result.get("subscription_end"):
                        subscription_end_date = reactivate_result["subscription_end"].strftime("%d %B %Y")

                    await email_service.send_subscription_reactivated_email(
                        email=current_user.email,
                        username=current_user.username,
                        subscription_end_date=subscription_end_date
                    )
                    logger.info(f"✅ Sent subscription reactivation email to {current_user.username}")
                except Exception as e:
                    # Email failure should not block the reactivation
                    logger.error(f"❌ Failed to send subscription reactivation email to {current_user.username}: {e}")

            # SUCCESS RESPONSE
            return {
                "status": "success",
                "message": "Prenumeration återaktiverad! Du kommer att fortsätta ha åtkomst till Pro-funktioner.",
                "subscription_end": reactivate_result.get("subscription_end").isoformat() if reactivate_result.get("subscription_end") else None,
                "reactivated_at": datetime.now(timezone.utc).isoformat()
            }
        else:
            # Stripe reactivation failed
            error_msg = reactivate_result.get("error", "Okänd Stripe-fel")
            logger.error(f"Stripe reactivation failed for user {current_user.id}: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail=f"Misslyckades med att återaktivera prenumeration i Stripe: {error_msg}"
            )

    except HTTPException:
        # Re-raise HTTP exceptions (they have proper error messages)
        raise
    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Unexpected error during reactivation for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Ett oväntat fel uppstod vid återaktivering. Vänligen försök igen eller kontakta support."
        )


@router.get("/success")
async def subscription_success(
    current_user: CurrentActiveUser,
    session: DbSession,
    session_id: str = Query(..., description="Stripe checkout session ID")
):
    """
    Subscription success endpoint - Additional verification layer for Swedish version.

    This endpoint provides an extra safety net to ensure users get immediate access
    after successful Stripe payments, complementing the checkout.session.completed webhook.
    """
    try:
        logger.info(f"🎯 Swedish subscription success verification for session: {session_id}")

        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID krävs")

        # Verify the session with Stripe
        try:
            import stripe
            checkout_session = stripe.checkout.Session.retrieve(session_id)

            if checkout_session.payment_status == 'paid' and checkout_session.customer:
                # Find user by Stripe customer ID
                from axiestudio.services.database.models.user.crud import get_user_by_stripe_customer_id, update_user
                from axiestudio.services.database.models.user.model import UserUpdate

                user = await get_user_by_stripe_customer_id(session, checkout_session.customer)

                if user and user.subscription_status != 'active':
                    # Ensure user is activated (safety net)
                    update_data = UserUpdate(
                        subscription_status='active',
                        subscription_id=checkout_session.subscription
                    )
                    await update_user(session, user.id, update_data)
                    logger.info(f"✅ Swedish safety net: User {user.id} activated via success endpoint")

                return {
                    "status": "success",
                    "message": "Prenumeration bekräftad! Välkommen till AxieStudio Pro!",
                    "payment_status": checkout_session.payment_status,
                    "customer_id": checkout_session.customer
                }
            else:
                return {
                    "status": "pending",
                    "message": "Betalning behandlas fortfarande...",
                    "payment_status": checkout_session.payment_status
                }

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error in Swedish success endpoint: {e}")
            raise HTTPException(status_code=400, detail=f"Stripe-fel: {str(e)}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Swedish subscription success endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internt serverfel")
