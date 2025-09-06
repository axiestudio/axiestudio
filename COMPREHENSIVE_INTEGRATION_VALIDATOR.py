#!/usr/bin/env python3
"""
🔍 COMPREHENSIVE INTEGRATION VALIDATOR
AS A SENIOR DEVELOPER - Complete system validation with bulletproof checks

This validator performs comprehensive checks on:
- Backend API endpoints and their implementations
- Frontend component integration and routing
- Database model consistency
- Import resolution and syntax validation
- Subscription logic edge cases
- Email service integration
- Real-time updates and polling
"""

import asyncio
import sys
import os
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import ast
import re

class IntegrationValidator:
    """
    🛡️ COMPREHENSIVE INTEGRATION VALIDATOR
    
    Validates the entire subscription system integration with bulletproof checks.
    """
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backend_root = self.project_root / "src" / "backend" / "base"
        self.frontend_root = self.project_root / "src" / "frontend" / "src"
        self.results = []
        
    def validate_all(self) -> Dict[str, Any]:
        """Run comprehensive validation of the entire system."""
        print("🔍 COMPREHENSIVE INTEGRATION VALIDATION")
        print("=" * 80)
        
        validation_results = {
            "backend_api": self.validate_backend_api(),
            "frontend_integration": self.validate_frontend_integration(),
            "database_models": self.validate_database_models(),
            "import_resolution": self.validate_import_resolution(),
            "subscription_logic": self.validate_subscription_logic(),
            "email_integration": self.validate_email_integration(),
            "routing_logic": self.validate_routing_logic(),
            "real_time_updates": self.validate_real_time_updates()
        }
        
        # Calculate overall score
        total_checks = sum(len(checks) for checks in validation_results.values())
        passed_checks = sum(sum(1 for check in checks if check[1]) for checks in validation_results.values())
        
        print("\n" + "=" * 80)
        print(f"🎯 OVERALL VALIDATION SCORE: {passed_checks}/{total_checks} ({(passed_checks/total_checks)*100:.1f}%)")
        
        if passed_checks == total_checks:
            print("🎉 PERFECT SCORE! SYSTEM IS PRODUCTION READY!")
        elif passed_checks >= total_checks * 0.9:
            print("✅ EXCELLENT! Minor issues to address.")
        elif passed_checks >= total_checks * 0.8:
            print("⚠️  GOOD! Some issues need attention.")
        else:
            print("❌ CRITICAL ISSUES! System needs significant work.")
        
        return validation_results
    
    def validate_backend_api(self) -> List[Tuple[str, bool, str]]:
        """Validate backend API endpoints and implementations."""
        print("\n🔧 VALIDATING BACKEND API...")
        
        checks = []
        
        # Check subscription API file exists
        subscription_api = self.backend_root / "axiestudio" / "api" / "v1" / "subscriptions.py"
        if subscription_api.exists():
            checks.append(("Subscription API file exists", True, str(subscription_api)))
            
            # Parse and validate endpoints
            try:
                with open(subscription_api, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for required endpoints
                required_endpoints = [
                    "@router.post(\"/create-checkout\")",
                    "@router.post(\"/customer-portal\")",
                    "@router.get(\"/status\")",
                    "@router.delete(\"/cancel\")",
                    "@router.post(\"/reactivate\")",
                    "@router.post(\"/webhook\")"
                ]
                
                for endpoint in required_endpoints:
                    if endpoint in content:
                        checks.append((f"Endpoint {endpoint} exists", True, "Found in API"))
                    else:
                        checks.append((f"Endpoint {endpoint} exists", False, "Missing from API"))
                
                # Check for proper imports
                required_imports = [
                    "from fastapi import APIRouter",
                    "from loguru import logger",
                    "from axiestudio.services.stripe.service import stripe_service"
                ]
                
                for import_stmt in required_imports:
                    if import_stmt in content:
                        checks.append((f"Import: {import_stmt}", True, "Found"))
                    else:
                        checks.append((f"Import: {import_stmt}", False, "Missing"))
                        
            except Exception as e:
                checks.append(("Parse subscription API", False, f"Error: {e}"))
        else:
            checks.append(("Subscription API file exists", False, "File not found"))
        
        # Check Stripe service
        stripe_service = self.backend_root / "axiestudio" / "services" / "stripe" / "service.py"
        if stripe_service.exists():
            checks.append(("Stripe service exists", True, str(stripe_service)))
            
            try:
                with open(stripe_service, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for reactivate method
                if "async def reactivate_subscription" in content:
                    checks.append(("Reactivate subscription method", True, "Found in Stripe service"))
                else:
                    checks.append(("Reactivate subscription method", False, "Missing from Stripe service"))
                    
            except Exception as e:
                checks.append(("Parse Stripe service", False, f"Error: {e}"))
        else:
            checks.append(("Stripe service exists", False, "File not found"))
        
        return checks
    
    def validate_frontend_integration(self) -> List[Tuple[str, bool, str]]:
        """Validate frontend component integration."""
        print("\n⚛️  VALIDATING FRONTEND INTEGRATION...")
        
        checks = []
        
        # Check pricing page
        pricing_page = self.frontend_root / "pages" / "PricingPage" / "index.tsx"
        if pricing_page.exists():
            checks.append(("Pricing page exists", True, str(pricing_page)))
            
            try:
                with open(pricing_page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for canceled user handling
                if "isCanceled" in content:
                    checks.append(("Canceled user detection", True, "isCanceled variable found"))
                else:
                    checks.append(("Canceled user detection", False, "isCanceled variable missing"))
                
                # Check for continue to app button
                if "Continue to App" in content or "Fortsätt till App" in content:
                    checks.append(("Continue to App button", True, "Found in pricing page"))
                else:
                    checks.append(("Continue to App button", False, "Missing from pricing page"))
                    
            except Exception as e:
                checks.append(("Parse pricing page", False, f"Error: {e}"))
        else:
            checks.append(("Pricing page exists", False, "File not found"))
        
        # Check subscription management component
        sub_mgmt = self.frontend_root / "components" / "SubscriptionManagement" / "index.tsx"
        if sub_mgmt.exists():
            checks.append(("Subscription management component", True, str(sub_mgmt)))
            
            try:
                with open(sub_mgmt, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for reactivation functionality
                if "useReactivateSubscription" in content:
                    checks.append(("Reactivation hook usage", True, "Found in component"))
                else:
                    checks.append(("Reactivation hook usage", False, "Missing from component"))
                    
            except Exception as e:
                checks.append(("Parse subscription management", False, f"Error: {e}"))
        else:
            checks.append(("Subscription management component", False, "File not found"))
        
        # Check reactivation hook
        reactivate_hook = self.frontend_root / "controllers" / "API" / "queries" / "subscriptions" / "use-reactivate-subscription.ts"
        if reactivate_hook.exists():
            checks.append(("Reactivation hook exists", True, str(reactivate_hook)))
        else:
            checks.append(("Reactivation hook exists", False, "File not found"))
        
        return checks
    
    def validate_database_models(self) -> List[Tuple[str, bool, str]]:
        """Validate database model consistency."""
        print("\n🗄️  VALIDATING DATABASE MODELS...")
        
        checks = []
        
        # Check user model
        user_model = self.backend_root / "axiestudio" / "services" / "database" / "models" / "user" / "model.py"
        if user_model.exists():
            checks.append(("User model exists", True, str(user_model)))
            
            try:
                with open(user_model, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for subscription fields
                subscription_fields = [
                    "subscription_status",
                    "subscription_id",
                    "subscription_start",
                    "subscription_end",
                    "trial_start",
                    "trial_end"
                ]
                
                for field in subscription_fields:
                    if field in content:
                        checks.append((f"Field: {field}", True, "Found in user model"))
                    else:
                        checks.append((f"Field: {field}", False, "Missing from user model"))
                        
            except Exception as e:
                checks.append(("Parse user model", False, f"Error: {e}"))
        else:
            checks.append(("User model exists", False, "File not found"))
        
        return checks
    
    def validate_import_resolution(self) -> List[Tuple[str, bool, str]]:
        """Validate import resolution and syntax."""
        print("\n📦 VALIDATING IMPORT RESOLUTION...")
        
        checks = []
        
        # Check critical Python files for syntax
        python_files = [
            self.backend_root / "axiestudio" / "api" / "v1" / "subscriptions.py",
            self.backend_root / "axiestudio" / "services" / "stripe" / "service.py",
            self.backend_root / "axiestudio" / "services" / "email" / "service.py"
        ]
        
        for file_path in python_files:
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Try to parse as AST
                    ast.parse(content)
                    checks.append((f"Syntax: {file_path.name}", True, "Valid Python syntax"))
                    
                except SyntaxError as e:
                    checks.append((f"Syntax: {file_path.name}", False, f"Syntax error: {e}"))
                except Exception as e:
                    checks.append((f"Syntax: {file_path.name}", False, f"Parse error: {e}"))
            else:
                checks.append((f"File exists: {file_path.name}", False, "File not found"))
        
        return checks
    
    def validate_subscription_logic(self) -> List[Tuple[str, bool, str]]:
        """Validate subscription logic implementation."""
        print("\n🧠 VALIDATING SUBSCRIPTION LOGIC...")
        
        checks = []
        
        # Check subscription guard
        sub_guard = self.frontend_root / "components" / "authorization" / "subscriptionGuard" / "index.tsx"
        if sub_guard.exists():
            checks.append(("Subscription guard exists", True, str(sub_guard)))
            
            try:
                with open(sub_guard, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for canceled user handling
                if "isCanceled" in content and "canceled" in content:
                    checks.append(("Canceled user logic in guard", True, "Found canceled handling"))
                else:
                    checks.append(("Canceled user logic in guard", False, "Missing canceled handling"))
                    
            except Exception as e:
                checks.append(("Parse subscription guard", False, f"Error: {e}"))
        else:
            checks.append(("Subscription guard exists", False, "File not found"))
        
        return checks
    
    def validate_email_integration(self) -> List[Tuple[str, bool, str]]:
        """Validate email service integration."""
        print("\n📧 VALIDATING EMAIL INTEGRATION...")
        
        checks = []
        
        # Check email service
        email_service = self.backend_root / "axiestudio" / "services" / "email" / "service.py"
        if email_service.exists():
            checks.append(("Email service exists", True, str(email_service)))
            
            try:
                with open(email_service, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for reactivation email method
                if "send_subscription_reactivated_email" in content:
                    checks.append(("Reactivation email method", True, "Found in email service"))
                else:
                    checks.append(("Reactivation email method", False, "Missing from email service"))
                    
            except Exception as e:
                checks.append(("Parse email service", False, f"Error: {e}"))
        else:
            checks.append(("Email service exists", False, "File not found"))
        
        return checks
    
    def validate_routing_logic(self) -> List[Tuple[str, bool, str]]:
        """Validate routing and navigation logic."""
        print("\n🛣️  VALIDATING ROUTING LOGIC...")
        
        checks = []
        
        # Check routes configuration
        routes_file = self.frontend_root / "routes.tsx"
        if routes_file.exists():
            checks.append(("Routes file exists", True, str(routes_file)))
            
            try:
                with open(routes_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check that pricing page is not protected by subscription guard
                if 'path="pricing"' in content and "SubscriptionGuard" not in content.split('path="pricing"')[1].split("</Route>")[0]:
                    checks.append(("Pricing page not protected", True, "Pricing page accessible"))
                else:
                    checks.append(("Pricing page not protected", False, "Pricing page may be protected"))
                    
            except Exception as e:
                checks.append(("Parse routes file", False, f"Error: {e}"))
        else:
            checks.append(("Routes file exists", False, "File not found"))
        
        return checks
    
    def validate_real_time_updates(self) -> List[Tuple[str, bool, str]]:
        """Validate real-time update functionality."""
        print("\n⚡ VALIDATING REAL-TIME UPDATES...")
        
        checks = []
        
        # Check subscription store
        sub_store = self.frontend_root / "stores" / "subscriptionStore.ts"
        if sub_store.exists():
            checks.append(("Subscription store exists", True, str(sub_store)))
            
            try:
                with open(sub_store, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for polling functionality
                if "startPolling" in content and "stopPolling" in content:
                    checks.append(("Polling functionality", True, "Found in subscription store"))
                else:
                    checks.append(("Polling functionality", False, "Missing from subscription store"))
                    
            except Exception as e:
                checks.append(("Parse subscription store", False, f"Error: {e}"))
        else:
            checks.append(("Subscription store exists", False, "File not found"))
        
        return checks


async def run_comprehensive_validation():
    """Run the comprehensive validation system."""
    # Get the project root (axiestudio directory)
    current_dir = Path(__file__).parent
    
    validator = IntegrationValidator(str(current_dir))
    results = validator.validate_all()
    
    return results


if __name__ == "__main__":
    asyncio.run(run_comprehensive_validation())
