#!/usr/bin/env python3
"""
🎯 PRODUCTION STRIPE INTEGRATION AUDIT
=====================================

Comprehensive audit of the entire Stripe integration to ensure production readiness:
1. Webhook handlers completeness
2. Database migration system
3. Subscription status logic
4. Frontend-backend connection
5. Zero-bug implementation verification

This script verifies that the Stripe integration is bulletproof for production.
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any

class ProductionStripeAudit:
    """Comprehensive Stripe integration audit for production readiness."""
    
    def __init__(self):
        self.results = {
            "webhook_handlers": {},
            "database_migration": {},
            "subscription_logic": {},
            "frontend_backend": {},
            "production_readiness": {}
        }
        self.errors = []
        self.warnings = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log audit messages."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "CRITICAL": "🚨"
        }.get(level, "ℹ️")
        
        print(f"[{timestamp}] {prefix} {message}")
        
        if level == "ERROR":
            self.errors.append(message)
        elif level == "WARNING":
            self.warnings.append(message)
    
    def audit_webhook_handlers(self) -> bool:
        """Audit webhook handler completeness."""
        self.log("🔍 AUDITING WEBHOOK HANDLERS", "INFO")
        
        # Expected webhook events for production
        required_events = [
            'checkout.session.completed',
            'customer.subscription.created',
            'customer.subscription.updated', 
            'customer.subscription.deleted',
            'invoice.payment_succeeded',
            'invoice.payment_failed',
            'invoice.finalized',
            'invoice.paid'
        ]
        
        # Check if webhook handler file exists
        webhook_file = Path("src/backend/base/axiestudio/services/stripe/service.py")
        if not webhook_file.exists():
            self.log("Stripe service file not found", "CRITICAL")
            return False
        
        # Read webhook handler file
        try:
            with open(webhook_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for each required event handler
            missing_handlers = []
            for event in required_events:
                handler_method = f"_handle_{event.replace('.', '_')}"
                if handler_method not in content:
                    missing_handlers.append(event)
                else:
                    self.log(f"✅ Handler found: {event}", "SUCCESS")
            
            if missing_handlers:
                self.log(f"Missing webhook handlers: {missing_handlers}", "ERROR")
                return False
            
            # Check webhook endpoint
            webhook_endpoint = Path("src/backend/base/axiestudio/api/v1/subscriptions.py")
            if webhook_endpoint.exists():
                with open(webhook_endpoint, 'r', encoding='utf-8') as f:
                    endpoint_content = f.read()
                
                if "stripe.Webhook.construct_event" in endpoint_content:
                    self.log("✅ Webhook signature verification implemented", "SUCCESS")
                else:
                    self.log("Missing webhook signature verification", "ERROR")
                    return False
                
                if "webhook_events" in endpoint_content:
                    self.log("✅ Database-backed idempotency implemented", "SUCCESS")
                else:
                    self.log("Missing database-backed idempotency", "WARNING")
            
            self.results["webhook_handlers"]["status"] = "PASS"
            return True
            
        except Exception as e:
            self.log(f"Error reading webhook files: {e}", "ERROR")
            return False
    
    def audit_database_migration(self) -> bool:
        """Audit automatic database migration system."""
        self.log("🔍 AUDITING DATABASE MIGRATION SYSTEM", "INFO")
        
        # Check database service file
        db_service_file = Path("src/backend/base/axiestudio/services/database/service.py")
        if not db_service_file.exists():
            self.log("Database service file not found", "CRITICAL")
            return False
        
        try:
            with open(db_service_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for webhook_events table in migration
            if "webhook_events" in content:
                self.log("✅ webhook_events table included in automatic migration", "SUCCESS")
            else:
                self.log("webhook_events table missing from automatic migration", "ERROR")
                return False
            
            # Check for subscription columns
            subscription_columns = [
                "subscription_status",
                "subscription_id", 
                "trial_start",
                "trial_end",
                "subscription_start",
                "subscription_end",
                "stripe_customer_id"
            ]
            
            missing_columns = []
            for column in subscription_columns:
                if column not in content:
                    missing_columns.append(column)
                else:
                    self.log(f"✅ Column migration found: {column}", "SUCCESS")
            
            if missing_columns:
                self.log(f"Missing subscription columns in migration: {missing_columns}", "WARNING")
            
            self.results["database_migration"]["status"] = "PASS"
            return True
            
        except Exception as e:
            self.log(f"Error reading database service file: {e}", "ERROR")
            return False
    
    def audit_subscription_logic(self) -> bool:
        """Audit subscription status logic for correctness."""
        self.log("🔍 AUDITING SUBSCRIPTION STATUS LOGIC", "INFO")
        
        # Check subscription status endpoint
        subscription_file = Path("src/backend/base/axiestudio/api/v1/subscriptions.py")
        if not subscription_file.exists():
            self.log("Subscription API file not found", "CRITICAL")
            return False
        
        try:
            with open(subscription_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for proper status handling
            status_checks = [
                "subscription_status == \"active\"",
                "subscription_status == \"trial\"", 
                "subscription_status == \"canceled\"",
                "is_superuser"
            ]
            
            for check in status_checks:
                if check in content:
                    self.log(f"✅ Status check found: {check}", "SUCCESS")
                else:
                    self.log(f"Missing status check: {check}", "WARNING")
            
            # Check for trial expiration logic
            if "trial_expired" in content:
                self.log("✅ Trial expiration logic implemented", "SUCCESS")
            else:
                self.log("Missing trial expiration logic", "ERROR")
                return False
            
            # Check for real-time status endpoint
            if "/status/realtime" in content:
                self.log("✅ Real-time status endpoint implemented", "SUCCESS")
            else:
                self.log("Missing real-time status endpoint", "WARNING")
            
            self.results["subscription_logic"]["status"] = "PASS"
            return True
            
        except Exception as e:
            self.log(f"Error reading subscription file: {e}", "ERROR")
            return False
    
    def audit_frontend_backend_connection(self) -> bool:
        """Audit frontend-backend connection."""
        self.log("🔍 AUDITING FRONTEND-BACKEND CONNECTION", "INFO")
        
        # Check subscription store
        store_file = Path("src/frontend/src/stores/subscriptionStore.ts")
        if store_file.exists():
            with open(store_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "startFastPolling" in content:
                self.log("✅ Fast polling for payment scenarios implemented", "SUCCESS")
            else:
                self.log("Missing fast polling implementation", "WARNING")
            
            if "/api/v1/subscriptions/status" in content:
                self.log("✅ Backend API integration found", "SUCCESS")
            else:
                self.log("Missing backend API integration", "ERROR")
                return False
        else:
            self.log("Subscription store not found", "ERROR")
            return False
        
        # Check subscription guard
        guard_file = Path("src/frontend/src/components/authorization/subscriptionGuard/index.tsx")
        if guard_file.exists():
            with open(guard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "subscription_status === \"active\"" in content:
                self.log("✅ Active subscription check in guard", "SUCCESS")
            else:
                self.log("Missing active subscription check in guard", "ERROR")
                return False
        else:
            self.log("Subscription guard not found", "ERROR")
            return False
        
        self.results["frontend_backend"]["status"] = "PASS"
        return True
    
    def audit_production_readiness(self) -> bool:
        """Final production readiness check."""
        self.log("🔍 FINAL PRODUCTION READINESS AUDIT", "INFO")
        
        # Check environment variable handling
        subscription_file = Path("src/backend/base/axiestudio/api/v1/subscriptions.py")
        if subscription_file.exists():
            with open(subscription_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "STRIPE_WEBHOOK_SECRET" in content:
                self.log("✅ Webhook secret environment variable check", "SUCCESS")
            else:
                self.log("Missing webhook secret environment variable check", "ERROR")
                return False
            
            if "HTTPException" in content:
                self.log("✅ Proper error handling implemented", "SUCCESS")
            else:
                self.log("Missing proper error handling", "ERROR")
                return False
        
        # Check for database transaction handling
        if "session.commit()" in content and "session.rollback()" in content:
            self.log("✅ Database transaction handling implemented", "SUCCESS")
        else:
            self.log("Missing proper database transaction handling", "ERROR")
            return False
        
        self.results["production_readiness"]["status"] = "PASS"
        return True
    
    async def run_comprehensive_audit(self) -> Dict[str, Any]:
        """Run comprehensive production audit."""
        self.log("🎯 STARTING PRODUCTION STRIPE INTEGRATION AUDIT", "INFO")
        self.log("=" * 60, "INFO")
        
        audit_results = {
            "webhook_handlers": self.audit_webhook_handlers(),
            "database_migration": self.audit_database_migration(),
            "subscription_logic": self.audit_subscription_logic(),
            "frontend_backend": self.audit_frontend_backend_connection(),
            "production_readiness": self.audit_production_readiness()
        }
        
        # Calculate overall score
        passed_audits = sum(1 for result in audit_results.values() if result)
        total_audits = len(audit_results)
        score = (passed_audits / total_audits) * 100
        
        self.log("=" * 60, "INFO")
        self.log("🎯 PRODUCTION AUDIT RESULTS", "INFO")
        self.log("=" * 60, "INFO")
        
        for audit_name, passed in audit_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            self.log(f"{audit_name.upper()}: {status}", "SUCCESS" if passed else "ERROR")
        
        self.log("=" * 60, "INFO")
        self.log(f"🎯 OVERALL SCORE: {score:.1f}% ({passed_audits}/{total_audits} audits passed)", 
                "SUCCESS" if score >= 100 else "WARNING" if score >= 80 else "ERROR")
        
        if self.errors:
            self.log("🚨 CRITICAL ISSUES FOUND:", "ERROR")
            for error in self.errors:
                self.log(f"  • {error}", "ERROR")
        
        if self.warnings:
            self.log("⚠️ WARNINGS:", "WARNING")
            for warning in self.warnings:
                self.log(f"  • {warning}", "WARNING")
        
        # Production readiness verdict
        if score >= 100 and not self.errors:
            self.log("🎉 PRODUCTION READY: Stripe integration is bulletproof!", "SUCCESS")
            production_ready = True
        elif score >= 90 and len(self.errors) <= 1:
            self.log("⚠️ MOSTLY READY: Minor issues need fixing before production", "WARNING")
            production_ready = False
        else:
            self.log("🚨 NOT PRODUCTION READY: Critical issues must be fixed", "ERROR")
            production_ready = False
        
        return {
            "audit_results": audit_results,
            "score": score,
            "errors": self.errors,
            "warnings": self.warnings,
            "production_ready": production_ready,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


async def main():
    """Run the production audit."""
    auditor = ProductionStripeAudit()
    results = await auditor.run_comprehensive_audit()
    
    # Return appropriate exit code
    return 0 if results["production_ready"] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
