"""Stripe service for handling subscriptions and payments."""

import os
from datetime import datetime, timezone, timedelta
from typing import Optional

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None

from loguru import logger

from axiestudio.services.database.models.user.model import UserUpdate
from axiestudio.services.database.models.user.crud import update_user


class StripeService:
    """Service for handling Stripe operations."""
    
    def __init__(self):
        """Initialize Stripe service with API key."""
        if not STRIPE_AVAILABLE:
            logger.warning("Stripe package not available - Stripe functionality will be disabled")
            self.stripe_secret_key = None
            self.stripe_price_id = None
            self.is_railway = False
            return

        self.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
        self.stripe_price_id = os.getenv("STRIPE_PRICE_ID")
        self.is_railway = os.getenv("RAILWAY_ENVIRONMENT") == "production"

        if not self.stripe_secret_key:
            logger.warning("STRIPE_SECRET_KEY not found - Stripe functionality will be disabled")
            return

        if not self.stripe_price_id:
            logger.warning("STRIPE_PRICE_ID not found - using default price ID")
            self.stripe_price_id = "price_1RxD0RBacFXEnBmNI6T0IkOd"

        stripe.api_key = self.stripe_secret_key
        logger.info(f"Stripe service initialized for {'production' if self.is_railway else 'development'} environment")

    def is_configured(self) -> bool:
        """Check if Stripe is properly configured."""
        return bool(STRIPE_AVAILABLE and self.stripe_secret_key and self.stripe_price_id)
    
    async def create_customer(self, email: str, name: str) -> str:
        """Create a Stripe customer."""
        try:
            logger.info(f"Creating Stripe customer for email: {email[:3]}***@{email.split('@')[1] if '@' in email else 'unknown'}")
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={"source": "axiestudio"}
            )
            logger.info(f"Created Stripe customer: {customer.id}")
            return customer.id
        except stripe.error.StripeError as e:
            logger.error(f"Stripe API error creating customer: {e.user_message} (Code: {e.code})")
            raise Exception(f"Stripe customer creation failed: {e.user_message}")
        except Exception as e:
            logger.error(f"Unexpected error creating Stripe customer: {e}")
            raise
    
    async def create_checkout_session(
        self,
        customer_id: str,
        success_url: str,
        cancel_url: str,
        trial_days: int = 7
    ) -> str:
        """Create a Stripe checkout session with trial."""
        try:
            # FIXED: Handle trial_days = 0 case (Stripe doesn't accept 0-day trials)
            subscription_data = {
                'metadata': {
                    'source': 'axiestudio'
                }
            }

            # Only add trial if trial_days > 0 (Stripe requirement)
            if trial_days > 0:
                subscription_data['trial_period_days'] = trial_days
                logger.info(f"Creating checkout with {trial_days} trial days")
            else:
                logger.info("Creating checkout with no trial (immediate payment)")

            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': self.stripe_price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                subscription_data=subscription_data,
                allow_promotion_codes=True,
            )
            logger.info(f"Created checkout session: {session.id}")
            return session.url
        except stripe.error.StripeError as e:
            logger.error(f"Stripe API error creating checkout session: {e.user_message} (Code: {e.code})")
            logger.error(f"Stripe error details - customer_id: {customer_id}, price_id: {self.stripe_price_id}, trial_days: {trial_days}")
            raise Exception(f"Stripe checkout creation failed: {e.user_message}")
        except Exception as e:
            logger.error(f"Unexpected error creating checkout session: {e}")
            logger.error(f"Checkout parameters - customer_id: {customer_id}, price_id: {self.stripe_price_id}, trial_days: {trial_days}")
            raise
    
    async def create_customer_portal_session(self, customer_id: str, return_url: str) -> str:
        """Create a Stripe customer portal session."""
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            logger.info(f"Created customer portal session: {session.id}")
            return session.url
        except Exception as e:
            logger.error(f"Failed to create customer portal session: {e}")
            raise
    
    async def get_subscription(self, subscription_id: str) -> Optional[dict]:
        """Get subscription details from Stripe."""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                'id': subscription.id,
                'status': subscription.status,
                'current_period_start': datetime.fromtimestamp(subscription.current_period_start, tz=timezone.utc),
                'current_period_end': datetime.fromtimestamp(subscription.current_period_end, tz=timezone.utc),
                'trial_start': datetime.fromtimestamp(subscription.trial_start, tz=timezone.utc) if subscription.trial_start else None,
                'trial_end': datetime.fromtimestamp(subscription.trial_end, tz=timezone.utc) if subscription.trial_end else None,
                'customer_id': subscription.customer
            }
        except Exception as e:
            logger.error(f"Failed to get subscription: {e}")
            return None
    
    async def cancel_subscription(self, subscription_id: str) -> dict:
        """Cancel a subscription and return subscription details."""
        try:
            # Cancel the subscription (this sets it to cancel at period end)
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )

            # Get the period end date
            period_end = datetime.fromtimestamp(subscription.current_period_end, tz=timezone.utc)

            logger.info(f"Cancelled subscription: {subscription_id}, will end at: {period_end}")
            return {
                "success": True,
                "subscription_end": period_end,
                "current_period_end": subscription.current_period_end
            }
        except Exception as e:
            logger.error(f"Failed to cancel subscription: {e}")
            return {"success": False}

    async def reactivate_subscription(self, subscription_id: str) -> dict:
        """
        🔄 ROBUST SUBSCRIPTION REACTIVATION

        Reactivates a canceled subscription with comprehensive error handling.
        Validates subscription state and handles all Stripe edge cases.
        """
        try:
            logger.info(f"🔄 Attempting to reactivate subscription: {subscription_id}")

            # STEP 1: Retrieve current subscription to validate state
            try:
                current_subscription = stripe.Subscription.retrieve(subscription_id)
            except stripe.error.InvalidRequestError as e:
                logger.error(f"❌ Invalid subscription ID {subscription_id}: {e}")
                return {
                    "success": False,
                    "error": f"Prenumeration hittades inte: {subscription_id}"
                }

            # STEP 2: Validate subscription can be reactivated
            if current_subscription.status not in ["active", "past_due"]:
                logger.warning(f"⚠️  Cannot reactivate subscription {subscription_id} with status: {current_subscription.status}")
                return {
                    "success": False,
                    "error": f"Prenumeration kan inte återaktiveras från status: {current_subscription.status}"
                }

            # Check if subscription is actually canceled (has cancel_at_period_end=True)
            if not current_subscription.cancel_at_period_end:
                logger.warning(f"⚠️  Subscription {subscription_id} is not canceled (cancel_at_period_end=False)")
                return {
                    "success": False,
                    "error": "Prenumerationen är inte avbruten och behöver inte återaktiveras"
                }

            # STEP 3: Reactivate by removing cancellation
            try:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=False
                )
                logger.info(f"✅ Successfully modified subscription {subscription_id}")
            except stripe.error.StripeError as e:
                logger.error(f"❌ Stripe error modifying subscription {subscription_id}: {e}")
                return {
                    "success": False,
                    "error": f"Stripe-fel vid återaktivering: {e.user_message or str(e)}"
                }

            # STEP 4: Calculate subscription end date
            try:
                period_end = datetime.fromtimestamp(subscription.current_period_end, tz=timezone.utc)
            except (ValueError, OSError) as e:
                logger.error(f"❌ Error parsing period end timestamp: {e}")
                # Fallback: use current time + 30 days
                period_end = datetime.now(timezone.utc) + timedelta(days=30)

            # STEP 5: Validate reactivation was successful
            if subscription.cancel_at_period_end:
                logger.error(f"❌ Reactivation failed - subscription {subscription_id} still has cancel_at_period_end=True")
                return {
                    "success": False,
                    "error": "Återaktivering misslyckades - prenumerationen är fortfarande avbruten"
                }

            logger.info(f"🎉 Successfully reactivated subscription: {subscription_id}, continues until: {period_end}")
            return {
                "success": True,
                "subscription_end": period_end,
                "current_period_end": subscription.current_period_end,
                "status": subscription.status,
                "cancel_at_period_end": subscription.cancel_at_period_end,
                "reactivated_at": datetime.now(timezone.utc)
            }

        except stripe.error.AuthenticationError as e:
            logger.error(f"❌ Stripe authentication error: {e}")
            return {
                "success": False,
                "error": "Stripe-autentiseringsfel. Kontakta support."
            }
        except stripe.error.RateLimitError as e:
            logger.error(f"❌ Stripe rate limit error: {e}")
            return {
                "success": False,
                "error": "För många förfrågningar till Stripe. Försök igen om en stund."
            }
        except stripe.error.StripeError as e:
            logger.error(f"❌ General Stripe error during reactivation: {e}")
            return {
                "success": False,
                "error": f"Stripe-fel: {e.user_message or 'Okänt fel'}"
            }
        except Exception as e:
            logger.error(f"❌ Unexpected error during subscription reactivation: {e}")
            return {
                "success": False,
                "error": f"Oväntat fel vid återaktivering: {str(e)}"
            }
    
    async def handle_webhook_event(self, event_data: dict, session) -> bool:
        """Handle Stripe webhook events."""
        try:
            event_type = event_data.get('type')
            data = event_data.get('data', {}).get('object', {})
            
            if event_type == 'customer.subscription.created':
                await self._handle_subscription_created(data, session)
            elif event_type == 'customer.subscription.updated':
                await self._handle_subscription_updated(data, session)
            elif event_type == 'customer.subscription.deleted':
                await self._handle_subscription_deleted(data, session)
            elif event_type == 'invoice.payment_succeeded':
                await self._handle_payment_succeeded(data, session)
            elif event_type == 'invoice.payment_failed':
                await self._handle_payment_failed(data, session)
            
            return True
        except Exception as e:
            logger.error(f"Failed to handle webhook event: {e}")
            return False
    
    async def _handle_subscription_created(self, subscription_data: dict, session):
        """Handle subscription created event."""
        customer_id = subscription_data.get('customer')
        subscription_id = subscription_data.get('id')
        status = subscription_data.get('status')
        
        # Find user by Stripe customer ID
        from axiestudio.services.database.models.user.crud import get_user_by_stripe_customer_id
        user = await get_user_by_stripe_customer_id(session, customer_id)
        
        if user:
            trial_end = None
            if subscription_data.get('trial_end'):
                trial_end = datetime.fromtimestamp(subscription_data['trial_end'], tz=timezone.utc)
            
            update_data = UserUpdate(
                subscription_id=subscription_id,
                subscription_status=status,
                trial_end=trial_end,
                subscription_start=datetime.fromtimestamp(subscription_data['current_period_start'], tz=timezone.utc),
                subscription_end=datetime.fromtimestamp(subscription_data['current_period_end'], tz=timezone.utc)
            )
            await update_user(session, user.id, update_data)
            logger.info(f"Updated user {user.id} with subscription {subscription_id}")

            # Send subscription welcome email (Swedish)
            if status == 'active' and user.email:
                try:
                    from axiestudio.services.email.service import EmailService
                    email_service = EmailService()
                    await email_service.send_subscription_welcome_email(
                        email=user.email,
                        username=user.username,
                        plan_name="Pro"  # Default plan name
                    )
                    logger.info(f"✅ Sent subscription welcome email to {user.username}")
                except Exception as e:
                    logger.error(f"❌ Failed to send subscription welcome email to {user.username}: {e}")
    
    async def _handle_subscription_updated(self, subscription_data: dict, session):
        """Handle subscription updated event."""
        await self._handle_subscription_created(subscription_data, session)  # Same logic
    
    async def _handle_subscription_deleted(self, subscription_data: dict, session):
        """Handle subscription deleted event - this happens when subscription actually ends."""
        customer_id = subscription_data.get('customer')

        from axiestudio.services.database.models.user.crud import get_user_by_stripe_customer_id
        user = await get_user_by_stripe_customer_id(session, customer_id)

        if user:
            # Get the subscription end date from the webhook data
            subscription_end = None
            if subscription_data.get('current_period_end'):
                subscription_end = datetime.fromtimestamp(subscription_data['current_period_end'], tz=timezone.utc)

            update_data = UserUpdate(
                subscription_status='canceled',
                subscription_id=None,  # Now it's safe to clear this since subscription has actually ended
                subscription_end=subscription_end  # Set the actual end date
            )
            await update_user(session, user.id, update_data)
            logger.info(f"Subscription ended for user {user.id} at {subscription_end}")
    
    async def _handle_payment_succeeded(self, invoice_data: dict, session):
        """Handle successful payment."""
        subscription_id = invoice_data.get('subscription')
        if subscription_id:
            subscription_data = await self.get_subscription(subscription_id)
            if subscription_data:
                await self._handle_subscription_updated(subscription_data, session)
    
    async def _handle_payment_failed(self, invoice_data: dict, session):
        """Handle failed payment."""
        customer_id = invoice_data.get('customer')
        
        from axiestudio.services.database.models.user.crud import get_user_by_stripe_customer_id
        user = await get_user_by_stripe_customer_id(session, customer_id)
        
        if user:
            update_data = UserUpdate(subscription_status='past_due')
            await update_user(session, user.id, update_data)
            logger.info(f"Marked user {user.id} as past due")


# Global instance
stripe_service = StripeService()
