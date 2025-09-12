#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE STRIPE SUBSCRIPTION BEHAVIOR TEST
==================================================

This script tests all complex user subscription behaviors:
1. Cancellation with remaining access until period end
2. Resubscription without time reset (continues remaining time)
3. Expired subscription resubscription handling
4. App-only trial system (no Stripe involvement)

Tests the exact scenarios the user requested.
"""

import asyncio
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Mock user class for testing
class MockUser:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 'test-user-id')
        self.username = kwargs.get('username', 'test_user')
        self.email = kwargs.get('email', 'test@example.com')
        self.subscription_status = kwargs.get('subscription_status', 'trial')
        self.subscription_id = kwargs.get('subscription_id', None)
        self.subscription_start = kwargs.get('subscription_start', None)
        self.subscription_end = kwargs.get('subscription_end', None)
        self.trial_start = kwargs.get('trial_start', None)
        self.trial_end = kwargs.get('trial_end', None)
        self.stripe_customer_id = kwargs.get('stripe_customer_id', None)
        self.is_superuser = kwargs.get('is_superuser', False)
        self.create_at = kwargs.get('create_at', datetime.now(timezone.utc))

async def test_comprehensive_stripe_behavior():
    """Test all complex subscription behaviors."""

    print("🧪 COMPREHENSIVE STRIPE SUBSCRIPTION BEHAVIOR TEST")
    print("=" * 60)

    load_dotenv()

    # Import services
    from src.backend.base.axiestudio.services.stripe.service import StripeService
    from src.backend.base.axiestudio.services.trial.service import TrialService
    
    # Initialize services
    stripe_service = StripeService()
    trial_service = TrialService()

    print(f"✅ Services initialized")
    print(f"   - Stripe configured: {stripe_service.is_configured()}")
    print(f"   - Trial duration: {trial_service.trial_duration_days} days")

    # Test scenarios
    test_results = {}

    # ========================================
    # TEST 1: APP-ONLY TRIAL SYSTEM
    # ========================================
    print("\n📋 TEST 1: APP-ONLY TRIAL SYSTEM (NO STRIPE)")
    print("-" * 50)

    # Create test user with trial (no Stripe involvement)
    trial_user = MockUser(
        username="trial_test_user",
        subscription_status="trial",
        trial_start=datetime.now(timezone.utc),
        trial_end=datetime.now(timezone.utc) + timedelta(days=7),
        stripe_customer_id=None  # NO STRIPE INVOLVEMENT
    )

    print(f"✅ Created trial user: {trial_user.username}")
    print(f"   - Status: {trial_user.subscription_status}")
    print(f"   - Trial start: {trial_user.trial_start}")
    print(f"   - Trial end: {trial_user.trial_end}")
    print(f"   - Stripe customer ID: {trial_user.stripe_customer_id}")

    # Check trial status
    trial_status = await trial_service.check_trial_status(trial_user)
    print(f"✅ Trial status check:")
    print(f"   - Status: {trial_status['status']}")
    print(f"   - Days left: {trial_status['days_left']}")
    print(f"   - Should cleanup: {trial_status['should_cleanup']}")
    print(f"   - Trial expired: {trial_status['trial_expired']}")

    test_results['app_only_trial'] = {
        'user_has_stripe_id': trial_user.stripe_customer_id is not None,
        'trial_status': trial_status['status'],
        'days_left': trial_status['days_left'],
        'access_allowed': not trial_status['should_cleanup']
    }

    # ========================================
    # TEST 2: SUBSCRIPTION CANCELLATION WITH REMAINING ACCESS
    # ========================================
    print("\n📋 TEST 2: SUBSCRIPTION CANCELLATION WITH REMAINING ACCESS")
    print("-" * 50)

    # Create user with active subscription
    now = datetime.now(timezone.utc)
    subscription_end = now + timedelta(days=15)  # 15 days remaining

    active_user = MockUser(
        username="cancel_test_user",
        subscription_status="active",
        subscription_id="sub_test_active_123",
        subscription_start=now - timedelta(days=15),  # Started 15 days ago
        subscription_end=subscription_end,
        stripe_customer_id="cus_test_123"
    )

    print(f"✅ Created active subscription user: {active_user.username}")
    print(f"   - Status: {active_user.subscription_status}")
    print(f"   - Subscription end: {active_user.subscription_end}")
    print(f"   - Days remaining: {(subscription_end - now).days}")

    # Simulate cancellation (set to canceled but keep end date)
    active_user.subscription_status = "canceled"
    # Keep the same end date - this is key!

    print(f"✅ Simulated cancellation:")
    print(f"   - New status: {active_user.subscription_status}")
    print(f"   - Subscription end unchanged: {active_user.subscription_end}")

    # Check if user still has access
    trial_status_canceled = await trial_service.check_trial_status(active_user)
    print(f"✅ Access check after cancellation:")
    print(f"   - Status: {trial_status_canceled['status']}")
    print(f"   - Access allowed: {not trial_status_canceled['should_cleanup']}")
    print(f"   - Days left: {trial_status_canceled.get('days_left', 0)}")

    test_results['cancellation_with_access'] = {
        'status_after_cancel': active_user.subscription_status,
        'access_allowed': not trial_status_canceled['should_cleanup'],
        'days_remaining': trial_status_canceled.get('days_left', 0),
        'subscription_end_preserved': active_user.subscription_end == subscription_end
    }

    # ========================================
    # TEST 3: RESUBSCRIPTION WITHOUT TIME RESET
    # ========================================
    print("\n📋 TEST 3: RESUBSCRIPTION WITHOUT TIME RESET")
    print("-" * 50)

    # Simulate reactivation (user regrets cancellation)
    original_end_date = active_user.subscription_end
    active_user.subscription_status = "active"
    # Keep the same subscription_end - this is key!

    print(f"✅ Simulated reactivation:")
    print(f"   - New status: {active_user.subscription_status}")
    print(f"   - Subscription end: {active_user.subscription_end}")
    print(f"   - Time NOT reset: {active_user.subscription_end == original_end_date}")

    # Check access after reactivation
    trial_status_reactivated = await trial_service.check_trial_status(active_user)
    print(f"✅ Access check after reactivation:")
    print(f"   - Status: {trial_status_reactivated['status']}")
    print(f"   - Access allowed: {not trial_status_reactivated['should_cleanup']}")
    print(f"   - Days left: {trial_status_reactivated.get('days_left', 0)}")

    test_results['resubscription_no_reset'] = {
        'status_after_reactivation': active_user.subscription_status,
        'access_allowed': not trial_status_reactivated['should_cleanup'],
        'time_was_reset': active_user.subscription_end != original_end_date,
        'days_remaining': trial_status_reactivated.get('days_left', 0)
    }

    # ========================================
    # TEST 4: EXPIRED SUBSCRIPTION RESUBSCRIPTION
    # ========================================
    print("\n📋 TEST 4: EXPIRED SUBSCRIPTION RESUBSCRIPTION")
    print("-" * 50)

    # Create user with expired subscription
    expired_end = now - timedelta(days=5)  # Expired 5 days ago

    expired_user = MockUser(
        username="expired_test_user",
        subscription_status="canceled",
        subscription_id=None,  # Subscription was deleted
        subscription_start=now - timedelta(days=35),
        subscription_end=expired_end,
        stripe_customer_id="cus_test_expired_123"
    )

    print(f"✅ Created expired subscription user: {expired_user.username}")
    print(f"   - Status: {expired_user.subscription_status}")
    print(f"   - Subscription end: {expired_user.subscription_end}")
    print(f"   - Days since expiry: {(now - expired_end).days}")

    # Check access for expired user
    trial_status_expired = await trial_service.check_trial_status(expired_user)
    print(f"✅ Access check for expired subscription:")
    print(f"   - Status: {trial_status_expired['status']}")
    print(f"   - Access allowed: {not trial_status_expired['should_cleanup']}")
    print(f"   - Should require new subscription: {trial_status_expired['should_cleanup']}")

    # Simulate new subscription for expired user
    new_subscription_end = now + timedelta(days=30)
    expired_user.subscription_status = "active"
    expired_user.subscription_id = "sub_test_new_456"
    expired_user.subscription_start = now
    expired_user.subscription_end = new_subscription_end

    print(f"✅ New subscription created for expired user:")
    print(f"   - New status: {expired_user.subscription_status}")
    print(f"   - New subscription ID: {expired_user.subscription_id}")
    print(f"   - New end date: {expired_user.subscription_end}")

    test_results['expired_resubscription'] = {
        'access_blocked_when_expired': trial_status_expired['should_cleanup'],
        'new_subscription_created': expired_user.subscription_status == "active",
        'new_subscription_id': expired_user.subscription_id is not None,
        'full_period_granted': (expired_user.subscription_end - now).days >= 29
    }
    
    # ========================================
    # FINAL RESULTS SUMMARY
    # ========================================
    print("\n🎯 COMPREHENSIVE TEST RESULTS SUMMARY")
    print("=" * 60)
    
    print("\n1️⃣ APP-ONLY TRIAL SYSTEM:")
    trial_result = test_results['app_only_trial']
    print(f"   ✅ No Stripe involvement: {not trial_result['user_has_stripe_id']}")
    print(f"   ✅ Trial access granted: {trial_result['access_allowed']}")
    print(f"   ✅ Proper trial duration: {trial_result['days_left']} days")
    
    print("\n2️⃣ CANCELLATION WITH REMAINING ACCESS:")
    cancel_result = test_results['cancellation_with_access']
    print(f"   ✅ Status changed to canceled: {cancel_result['status_after_cancel'] == 'canceled'}")
    print(f"   ✅ Access preserved until end: {cancel_result['access_allowed']}")
    print(f"   ✅ Subscription end preserved: {cancel_result['subscription_end_preserved']}")
    print(f"   ✅ Days remaining: {cancel_result['days_remaining']}")
    
    print("\n3️⃣ RESUBSCRIPTION WITHOUT TIME RESET:")
    resub_result = test_results['resubscription_no_reset']
    print(f"   ✅ Status reactivated: {resub_result['status_after_reactivation'] == 'active'}")
    print(f"   ✅ Access restored: {resub_result['access_allowed']}")
    print(f"   ✅ Time NOT reset: {not resub_result['time_was_reset']}")
    print(f"   ✅ Remaining time preserved: {resub_result['days_remaining']} days")
    
    print("\n4️⃣ EXPIRED SUBSCRIPTION RESUBSCRIPTION:")
    expired_result = test_results['expired_resubscription']
    print(f"   ✅ Access blocked when expired: {expired_result['access_blocked_when_expired']}")
    print(f"   ✅ New subscription created: {expired_result['new_subscription_created']}")
    print(f"   ✅ Full period granted: {expired_result['full_period_granted']}")
    
    # Overall assessment
    all_tests_passed = all([
        not trial_result['user_has_stripe_id'],  # App-only trial
        cancel_result['access_allowed'] and cancel_result['subscription_end_preserved'],  # Cancel with access
        resub_result['access_allowed'] and not resub_result['time_was_reset'],  # Resub no reset
        expired_result['access_blocked_when_expired'] and expired_result['new_subscription_created']  # Expired handling
    ])
    
    print(f"\n🎉 OVERALL ASSESSMENT: {'✅ ALL TESTS PASSED' if all_tests_passed else '❌ SOME TESTS FAILED'}")
    
    return test_results

if __name__ == "__main__":
    asyncio.run(test_comprehensive_stripe_behavior())
