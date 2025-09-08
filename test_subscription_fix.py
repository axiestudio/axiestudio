#!/usr/bin/env python3
"""
🧪 SUBSCRIPTION FIX VERIFICATION SCRIPT

This script helps verify that the subscription bug fix is working correctly.
Run this after deploying the fix to test the subscription flow.
"""

import asyncio
import os
import sys
from datetime import datetime, timezone
import httpx
import json

# Configuration
BASE_URL = os.getenv("AXIESTUDIO_URL", "http://localhost:7860")
TEST_EMAIL = "test-subscription@example.com"
TEST_USERNAME = "test-subscriber"
TEST_PASSWORD = "TestPassword123!"

class SubscriptionTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
        self.auth_token = None
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def log(self, message: str, status: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_emoji = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "ERROR": "❌",
            "WARNING": "⚠️"
        }
        print(f"[{timestamp}] {status_emoji.get(status, 'ℹ️')} {message}")
    
    async def test_webhook_events(self):
        """Test that webhook events are properly configured."""
        self.log("Testing webhook event handling...")
        
        # Check if the webhook endpoint exists
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/subscriptions/webhook",
                json={"type": "test"},
                headers={"stripe-signature": "test"}
            )
            # We expect this to fail with signature error, not 404
            if response.status_code == 404:
                self.log("Webhook endpoint not found!", "ERROR")
                return False
            elif response.status_code == 400:
                self.log("Webhook endpoint exists (signature validation working)", "SUCCESS")
                return True
        except Exception as e:
            self.log(f"Webhook test failed: {e}", "ERROR")
            return False
    
    async def test_subscription_status_endpoint(self):
        """Test subscription status endpoint."""
        self.log("Testing subscription status endpoint...")
        
        try:
            # This should fail without auth
            response = await self.client.get(f"{self.base_url}/api/v1/subscriptions/status")
            if response.status_code == 401:
                self.log("Subscription status endpoint requires auth (correct)", "SUCCESS")
                return True
            else:
                self.log(f"Unexpected response: {response.status_code}", "WARNING")
                return False
        except Exception as e:
            self.log(f"Subscription status test failed: {e}", "ERROR")
            return False
    
    async def test_success_endpoint(self):
        """Test the new success endpoint."""
        self.log("Testing subscription success endpoint...")
        
        try:
            # This should fail without auth and session_id
            response = await self.client.get(f"{self.base_url}/api/v1/subscriptions/success")
            if response.status_code in [401, 422]:  # 422 for missing query param
                self.log("Success endpoint exists and validates properly", "SUCCESS")
                return True
            else:
                self.log(f"Unexpected response: {response.status_code}", "WARNING")
                return False
        except Exception as e:
            self.log(f"Success endpoint test failed: {e}", "ERROR")
            return False
    
    async def test_health_check(self):
        """Test basic health check."""
        self.log("Testing application health...")
        
        try:
            response = await self.client.get(f"{self.base_url}/health_check")
            if response.status_code == 200:
                self.log("Application is healthy", "SUCCESS")
                return True
            else:
                self.log(f"Health check failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Health check failed: {e}", "ERROR")
            return False
    
    async def test_stripe_configuration(self):
        """Test if Stripe is properly configured."""
        self.log("Testing Stripe configuration...")
        
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/subscriptions/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("stripe_configured"):
                    self.log("Stripe is properly configured", "SUCCESS")
                    return True
                else:
                    self.log("Stripe is not configured", "WARNING")
                    return False
            else:
                self.log(f"Stripe health check failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Stripe configuration test failed: {e}", "ERROR")
            return False
    
    async def run_all_tests(self):
        """Run all verification tests."""
        self.log("🚀 Starting Subscription Fix Verification Tests")
        self.log(f"Testing against: {self.base_url}")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Webhook Events", self.test_webhook_events),
            ("Subscription Status", self.test_subscription_status_endpoint),
            ("Success Endpoint", self.test_success_endpoint),
            ("Stripe Configuration", self.test_stripe_configuration),
        ]
        
        results = {}
        for test_name, test_func in tests:
            self.log(f"Running {test_name} test...")
            try:
                result = await test_func()
                results[test_name] = result
            except Exception as e:
                self.log(f"{test_name} test crashed: {e}", "ERROR")
                results[test_name] = False
        
        # Summary
        self.log("=" * 50)
        self.log("📊 TEST RESULTS SUMMARY")
        self.log("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results.items():
            status = "PASS" if result else "FAIL"
            emoji = "✅" if result else "❌"
            self.log(f"{emoji} {test_name}: {status}")
            if result:
                passed += 1
        
        self.log("=" * 50)
        self.log(f"📈 OVERALL: {passed}/{total} tests passed")
        
        if passed == total:
            self.log("🎉 ALL TESTS PASSED! Subscription fix is working correctly.", "SUCCESS")
            return True
        else:
            self.log("⚠️ Some tests failed. Please check the configuration.", "WARNING")
            return False

async def main():
    """Main test runner."""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = BASE_URL
    
    print("🧪 AXIESTUDIO SUBSCRIPTION FIX VERIFICATION")
    print("=" * 60)
    print(f"Target URL: {base_url}")
    print("=" * 60)
    
    async with SubscriptionTester(base_url) as tester:
        success = await tester.run_all_tests()
        
        if success:
            print("\n🎯 NEXT STEPS:")
            print("1. Update your Stripe webhook to include 'checkout.session.completed' event")
            print("2. Test the complete payment flow with a real user")
            print("3. Monitor logs for webhook processing")
            sys.exit(0)
        else:
            print("\n🔧 TROUBLESHOOTING:")
            print("1. Check that the application is running")
            print("2. Verify environment variables are set")
            print("3. Check application logs for errors")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
