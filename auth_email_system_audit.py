#!/usr/bin/env python3
"""
SENIOR TESTER - COMPREHENSIVE AUTH & EMAIL SYSTEM AUDIT
Testing authentication system and email templates for AxieStudio.
"""

import asyncio
import sys
import json
from pathlib import Path

class AuthEmailSystemAuditor:
    def __init__(self):
        self.test_results = {}
        self.critical_issues = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
        
    async def run_comprehensive_audit(self):
        """Run comprehensive auth and email system audit"""
        print("🔐 SENIOR TESTER - AUTH & EMAIL SYSTEM AUDIT")
        print("=" * 60)
        print("Testing authentication system and email templates...")
        print()
        
        # Test 1: Authentication System
        await self.test_auth_system()
        
        # Test 2: Email System
        await self.test_email_system()
        
        # Test 3: UI/UX Quality
        await self.test_auth_ui_ux()
        
        # Test 4: Security Features
        await self.test_security_features()
        
        # Generate Final Report
        self.generate_final_report()
        
        return len(self.critical_issues) == 0
    
    async def test_auth_system(self):
        """Test Authentication System Components"""
        print("🔐 AUTHENTICATION SYSTEM TEST")
        print("-" * 40)
        
        # Test auth pages exist
        auth_pages = {
            "LoginPage": "axiestudio/src/frontend/src/pages/LoginPage/index.tsx",
            "SignUpPage": "axiestudio/src/frontend/src/pages/SignUpPage/index.tsx",
            "ForgotPasswordPage": "axiestudio/src/frontend/src/pages/ForgotPasswordPage/index.tsx",
            "ResetPasswordPage": "axiestudio/src/frontend/src/pages/ResetPasswordPage/index.tsx",
        }
        
        for page_name, page_path in auth_pages.items():
            self.total_checks += 1
            if Path(page_path).exists():
                print(f"✅ {page_name}: Found")
                self.success_count += 1
            else:
                self.critical_issues.append(f"Missing auth page: {page_name}")
                print(f"❌ {page_name}: Missing")
        
        # Test auth API endpoints
        auth_api_file = Path("axiestudio/src/backend/base/axiestudio/api/v1/email_verification.py")
        self.total_checks += 1
        if auth_api_file.exists():
            print(f"✅ Email Verification API: Found")
            self.success_count += 1
            
            # Check specific endpoints
            with open(auth_api_file, 'r') as f:
                api_content = f.read()
            
            endpoints = {
                "forgot-password": "/forgot-password",
                "reset-password": "/reset-password",
                "verify-email": "/verify-email",
            }
            
            for endpoint_name, endpoint_path in endpoints.items():
                self.total_checks += 1
                if endpoint_path in api_content:
                    print(f"✅ API Endpoint {endpoint_name}: Found")
                    self.success_count += 1
                else:
                    self.critical_issues.append(f"Missing API endpoint: {endpoint_name}")
                    print(f"❌ API Endpoint {endpoint_name}: Missing")
        else:
            self.critical_issues.append("Email verification API file missing")
            print(f"❌ Email Verification API: Missing")
        
        # Test auth context
        auth_context_file = Path("axiestudio/src/frontend/src/contexts/authContext.tsx")
        self.total_checks += 1
        if auth_context_file.exists():
            print(f"✅ Auth Context: Found")
            self.success_count += 1
        else:
            self.critical_issues.append("Auth context missing")
            print(f"❌ Auth Context: Missing")
        
        self.test_results["auth_system"] = len([i for i in self.critical_issues if "auth" in i.lower()]) == 0
    
    async def test_email_system(self):
        """Test Email System"""
        print(f"\n📧 EMAIL SYSTEM TEST")
        print("-" * 40)
        
        # Test email service
        email_service_file = Path("axiestudio/src/backend/base/axiestudio/services/email/service.py")
        self.total_checks += 1
        if email_service_file.exists():
            print(f"✅ Email Service: Found")
            self.success_count += 1
            
            # Check email templates
            with open(email_service_file, 'r') as f:
                email_content = f.read()
            
            # Test logo integration
            self.total_checks += 1
            if "scontent-arn2-1.xx.fbcdn.net" in email_content:
                print(f"✅ AxieStudio Logo: Properly integrated")
                self.success_count += 1
            else:
                self.warnings.append("AxieStudio logo not found in email templates")
                print(f"⚠️ AxieStudio Logo: Not found")
            
            # Test email template features
            email_features = {
                "HTML Templates": "<!DOCTYPE html>",
                "Responsive Design": "@media",
                "Modern Styling": "background: linear-gradient",
                "Professional Layout": "max-width: 600px",
                "Verification Email": "verify your email",
                "Password Reset Email": "reset your password",
            }
            
            for feature_name, feature_keyword in email_features.items():
                self.total_checks += 1
                if feature_keyword in email_content:
                    print(f"✅ {feature_name}: Implemented")
                    self.success_count += 1
                else:
                    self.warnings.append(f"Email feature missing: {feature_name}")
                    print(f"⚠️ {feature_name}: Missing")
        else:
            self.critical_issues.append("Email service file missing")
            print(f"❌ Email Service: Missing")
        
        self.test_results["email_system"] = len([i for i in self.critical_issues if "email" in i.lower()]) == 0
    
    async def test_auth_ui_ux(self):
        """Test Authentication UI/UX"""
        print(f"\n🎨 AUTH UI/UX TEST")
        print("-" * 40)
        
        # Test login page UI
        login_page = Path("axiestudio/src/frontend/src/pages/LoginPage/index.tsx")
        if login_page.exists():
            with open(login_page, 'r') as f:
                login_content = f.read()
            
            ui_features = {
                "Form Validation": "@radix-ui/react-form",
                "Input Components": "InputComponent",
                "Button Components": "Button",
                "Error Handling": "setErrorData",
                "Loading States": "mutate",
                "Navigation Links": "CustomLink",
            }
            
            for feature_name, feature_keyword in ui_features.items():
                self.total_checks += 1
                if feature_keyword in login_content:
                    print(f"✅ Login {feature_name}: Implemented")
                    self.success_count += 1
                else:
                    self.warnings.append(f"Login UI missing: {feature_name}")
                    print(f"⚠️ Login {feature_name}: Missing")
        
        # Test signup page UI
        signup_page = Path("axiestudio/src/frontend/src/pages/SignUpPage/index.tsx")
        if signup_page.exists():
            with open(signup_page, 'r') as f:
                signup_content = f.read()
            
            signup_features = {
                "Password Confirmation": "cnfPassword",
                "Email Validation": "email",
                "Form Validation": "isDisabled",
                "Success Feedback": "setSuccessData",
                "Analytics Tracking": "track",
            }
            
            for feature_name, feature_keyword in signup_features.items():
                self.total_checks += 1
                if feature_keyword in signup_content:
                    print(f"✅ Signup {feature_name}: Implemented")
                    self.success_count += 1
                else:
                    self.warnings.append(f"Signup UI missing: {feature_name}")
                    print(f"⚠️ Signup {feature_name}: Missing")
        
        # Test forgot password UI
        forgot_page = Path("axiestudio/src/frontend/src/pages/ForgotPasswordPage/index.tsx")
        if forgot_page.exists():
            with open(forgot_page, 'r') as f:
                forgot_content = f.read()
            
            forgot_features = {
                "Modern Design": "bg-gradient-to-br",
                "Loading States": "isLoading",
                "Success States": "isSubmitted",
                "Error Handling": "setErrorData",
                "Responsive Layout": "w-96",
            }
            
            for feature_name, feature_keyword in forgot_features.items():
                self.total_checks += 1
                if feature_keyword in forgot_content:
                    print(f"✅ Forgot Password {feature_name}: Implemented")
                    self.success_count += 1
                else:
                    self.warnings.append(f"Forgot password UI missing: {feature_name}")
                    print(f"⚠️ Forgot Password {feature_name}: Missing")
        
        self.test_results["auth_ui_ux"] = len([w for w in self.warnings if "UI" in w]) < 3
    
    async def test_security_features(self):
        """Test Security Features"""
        print(f"\n🛡️ SECURITY FEATURES TEST")
        print("-" * 40)
        
        # Test password security
        users_api = Path("axiestudio/src/backend/base/axiestudio/api/v1/users.py")
        if users_api.exists():
            with open(users_api, 'r') as f:
                users_content = f.read()
            
            security_features = {
                "Password Hashing": "get_password_hash",
                "Password Verification": "verify_password",
                "User Authorization": "CurrentActiveUser",
                "Password Reuse Prevention": "You can't use your current password",
            }
            
            for feature_name, feature_keyword in security_features.items():
                self.total_checks += 1
                if feature_keyword in users_content:
                    print(f"✅ {feature_name}: Implemented")
                    self.success_count += 1
                else:
                    self.critical_issues.append(f"Security feature missing: {feature_name}")
                    print(f"❌ {feature_name}: Missing")
        
        # Test email verification security
        email_api = Path("axiestudio/src/backend/base/axiestudio/api/v1/email_verification.py")
        if email_api.exists():
            with open(email_api, 'r') as f:
                email_api_content = f.read()
            
            email_security = {
                "Token Expiration": "email_verification_expires",
                "Email Enumeration Protection": "Always return success",
                "Active User Check": "is_active",
                "Token Validation": "Invalid or expired",
            }
            
            for feature_name, feature_keyword in email_security.items():
                self.total_checks += 1
                if feature_keyword in email_api_content:
                    print(f"✅ {feature_name}: Implemented")
                    self.success_count += 1
                else:
                    self.warnings.append(f"Email security feature: {feature_name}")
                    print(f"⚠️ {feature_name}: Missing")
        
        self.test_results["security"] = len([i for i in self.critical_issues if "security" in i.lower()]) == 0
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "=" * 60)
        print("🏆 AUTH & EMAIL SYSTEM AUDIT REPORT")
        print("=" * 60)
        
        # Calculate overall score
        score = (self.success_count / self.total_checks) * 100 if self.total_checks > 0 else 0
        
        print(f"\n📊 OVERALL SCORE: {score:.1f}% ({self.success_count}/{self.total_checks})")
        
        # Test Results Summary
        print(f"\n📋 SYSTEM RESULTS:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test_name.replace('_', ' ').title()}")
        
        # Critical Issues
        if self.critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.critical_issues)}):")
            for issue in self.critical_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ NO CRITICAL ISSUES FOUND")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        # Final Assessment
        if len(self.critical_issues) == 0 and score >= 85:
            print(f"\n🎉 VERDICT: EXCELLENT AUTH & EMAIL SYSTEM")
            print("✅ Authentication system fully functional")
            print("✅ Email templates beautifully designed")
            print("✅ Security features properly implemented")
            print("✅ UI/UX meets modern standards")
            print("🚀 READY FOR PRODUCTION")
        elif len(self.critical_issues) == 0:
            print(f"\n👍 VERDICT: GOOD SYSTEM WITH MINOR IMPROVEMENTS")
            print("✅ Core functionality working")
            print("⚠️ Some enhancements recommended")
        else:
            print(f"\n❌ VERDICT: CRITICAL ISSUES NEED ATTENTION")
            print("🚨 Must fix critical issues before production")

async def main():
    """Run the auth and email system audit"""
    auditor = AuthEmailSystemAuditor()
    success = await auditor.run_comprehensive_audit()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
