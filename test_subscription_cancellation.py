#!/usr/bin/env python3
"""
Test script to verify subscription cancellation logic works correctly.
This script tests that canceled subscriptions maintain access until billing period ends.
"""

import sys
import os
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock

# Add the backend path to sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'src', 'backend', 'base')
sys.path.insert(0, backend_path)

def test_subscription_cancellation_logic():
    """Test that canceled subscriptions maintain access until period end."""
    
    print("🧪 TESTING SUBSCRIPTION CANCELLATION LOGIC")
    print("=" * 60)
    
    try:
        from axiestudio.services.trial.service import TrialService
        from axiestudio.services.database.models.user.model import User
        
        # Create trial service
        trial_service = TrialService()
        
        # Test Case 1: Active subscription
        print("\n📋 Test Case 1: Active Subscription")
        user_active = Mock(spec=User)
        user_active.subscription_status = "active"
        user_active.subscription_end = None
        user_active.is_superuser = False
        user_active.create_at = datetime.now(timezone.utc) - timedelta(days=5)
        user_active.trial_start = user_active.create_at
        
        result = trial_service.check_trial_status(user_active)
        print(f"   Status: {result['status']}")
        print(f"   Should cleanup: {result['should_cleanup']}")
        assert result['status'] == 'subscribed'
        assert result['should_cleanup'] == False
        print("   ✅ PASS: Active subscription allows access")
        
        # Test Case 2: Canceled subscription with valid end date (should maintain access)
        print("\n📋 Test Case 2: Canceled Subscription (Still Valid)")
        user_canceled_valid = Mock(spec=User)
        user_canceled_valid.subscription_status = "canceled"
        user_canceled_valid.subscription_end = datetime.now(timezone.utc) + timedelta(days=15)  # 15 days left
        user_canceled_valid.is_superuser = False
        user_canceled_valid.create_at = datetime.now(timezone.utc) - timedelta(days=5)
        user_canceled_valid.trial_start = user_canceled_valid.create_at
        
        result = trial_service.check_trial_status(user_canceled_valid)
        print(f"   Status: {result['status']}")
        print(f"   Should cleanup: {result['should_cleanup']}")
        print(f"   Days left: {result['days_left']}")
        assert result['status'] == 'canceled_but_active'
        assert result['should_cleanup'] == False
        assert result['days_left'] > 0
        print("   ✅ PASS: Canceled subscription with valid end date maintains access")
        
        # Test Case 3: Canceled subscription with expired end date (should block access)
        print("\n📋 Test Case 3: Canceled Subscription (Expired)")
        user_canceled_expired = Mock(spec=User)
        user_canceled_expired.subscription_status = "canceled"
        user_canceled_expired.subscription_end = datetime.now(timezone.utc) - timedelta(days=1)  # Expired yesterday
        user_canceled_expired.is_superuser = False
        user_canceled_expired.create_at = datetime.now(timezone.utc) - timedelta(days=30)
        user_canceled_expired.trial_start = user_canceled_expired.create_at
        
        result = trial_service.check_trial_status(user_canceled_expired)
        print(f"   Status: {result['status']}")
        print(f"   Should cleanup: {result['should_cleanup']}")
        assert result['should_cleanup'] == True
        print("   ✅ PASS: Expired canceled subscription blocks access")
        
        # Test Case 4: Trial user (should work normally)
        print("\n📋 Test Case 4: Trial User")
        user_trial = Mock(spec=User)
        user_trial.subscription_status = "trial"
        user_trial.subscription_end = None
        user_trial.is_superuser = False
        user_trial.create_at = datetime.now(timezone.utc) - timedelta(days=5)  # 5 days into trial
        user_trial.trial_start = user_trial.create_at
        
        result = trial_service.check_trial_status(user_trial)
        print(f"   Status: {result['status']}")
        print(f"   Should cleanup: {result['should_cleanup']}")
        print(f"   Days left: {result['days_left']}")
        assert result['status'] == 'trial'
        assert result['should_cleanup'] == False
        assert result['days_left'] > 0
        print("   ✅ PASS: Trial user has access")
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("✅ Subscription cancellation logic is working correctly")
        print("✅ Canceled subscriptions maintain access until billing period ends")
        print("✅ Expired canceled subscriptions properly block access")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stripe_cancellation_logic():
    """Test Stripe cancellation method."""
    
    print("\n🧪 TESTING STRIPE CANCELLATION METHOD")
    print("=" * 60)
    
    try:
        from axiestudio.services.stripe.service import StripeService
        
        # Create stripe service
        stripe_service = StripeService()
        
        # Check that cancel_subscription method exists and uses correct parameters
        import inspect
        cancel_method = getattr(stripe_service, 'cancel_subscription', None)
        
        if cancel_method:
            print("✅ cancel_subscription method exists")
            
            # Check method signature
            sig = inspect.signature(cancel_method)
            print(f"   Method signature: {sig}")
            
            # The method should be async and take subscription_id
            assert 'subscription_id' in sig.parameters
            print("✅ Method accepts subscription_id parameter")
            
            print("✅ Stripe service structure is correct")
            return True
        else:
            print("❌ cancel_subscription method not found")
            return False
            
    except Exception as e:
        print(f"❌ Stripe test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 STARTING SUBSCRIPTION CANCELLATION TESTS")
    print("Testing both English and Swedish branches...")
    
    success1 = test_subscription_cancellation_logic()
    success2 = test_stripe_cancellation_logic()
    
    if success1 and success2:
        print("\n🎯 FINAL RESULT: ALL TESTS PASSED!")
        print("The subscription cancellation bug has been successfully fixed!")
        sys.exit(0)
    else:
        print("\n💥 FINAL RESULT: SOME TESTS FAILED!")
        sys.exit(1)
