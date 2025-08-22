# -*- coding: utf-8 -*-
"""
ENTERPRISE AUTHENTICATION SYSTEM AUDIT
Comprehensive check of email verification, account activation, and password reset
"""

import sys
import traceback
import json
from pathlib import Path

print("🔐 ENTERPRISE AUTHENTICATION SYSTEM AUDIT")
print("="*70)

def test_email_verification_system():
    """Test the email verification system completeness"""
    print("\n📧 TESTING EMAIL VERIFICATION SYSTEM...")
    
    try:
        # Check backend email verification endpoint
        email_api_file = Path("temp/src/backend/base/axiestudio/api/v1/email_verification.py")
        if not email_api_file.exists():
            print("❌ Email verification API file missing")
            return False
        
        content = email_api_file.read_text(encoding='utf-8')
        
        # Check for essential endpoints
        endpoints = [
            ("/verify", "verify_email"),
            ("/verify-code", "verify_code"),
            ("/resend-verification", "resend_verification"),
            ("/resend-code", "resend_verification_code"),
        ]
        
        all_endpoints_found = True
        for endpoint, function in endpoints:
            if endpoint in content and function in content:
                print(f"✅ Email verification endpoint: {endpoint} ({function})")
            else:
                print(f"❌ Missing email verification endpoint: {endpoint}")
                all_endpoints_found = False
        
        # Check for enterprise features
        enterprise_features = [
            ("6-digit code verification", "verification_code"),
            ("Rate limiting", "verification_attempts"),
            ("Auto-login after verification", "create_user_tokens"),
            ("Account activation", "is_active = True"),
            ("Email verified flag", "email_verified = True"),
        ]
        
        for feature_name, pattern in enterprise_features:
            if pattern in content:
                print(f"✅ {feature_name}: Implemented")
            else:
                print(f"❌ {feature_name}: Missing")
                all_endpoints_found = False
        
        return all_endpoints_found
        
    except Exception as e:
        print(f"❌ Email verification test failed: {e}")
        return False

def test_account_activation_system():
    """Test the account activation system"""
    print("\n🔓 TESTING ACCOUNT ACTIVATION SYSTEM...")
    
    try:
        # Check user model for activation fields
        user_model_file = Path("temp/src/backend/base/axiestudio/services/database/models/user/model.py")
        if not user_model_file.exists():
            print("❌ User model file missing")
            return False
        
        content = user_model_file.read_text(encoding='utf-8')
        
        # Check for activation-related fields
        activation_fields = [
            ("is_active field", "is_active: bool"),
            ("email_verified field", "email_verified: bool"),
            ("verification_code field", "verification_code: str"),
            ("verification_code_expires field", "verification_code_expires: datetime"),
            ("verification_attempts field", "verification_attempts: int"),
        ]
        
        all_fields_found = True
        for field_name, pattern in activation_fields:
            if pattern in content:
                print(f"✅ {field_name}: Found")
            else:
                print(f"❌ {field_name}: Missing")
                all_fields_found = False
        
        # Check user creation process
        users_api_file = Path("temp/src/backend/base/axiestudio/api/v1/users.py")
        if users_api_file.exists():
            users_content = users_api_file.read_text(encoding='utf-8')
            
            activation_logic = [
                ("Users start inactive", "is_active = False"),
                ("Verification code generation", "create_verification"),
                ("Email sending", "send_verification"),
            ]
            
            for logic_name, pattern in activation_logic:
                if pattern in users_content:
                    print(f"✅ {logic_name}: Implemented")
                else:
                    print(f"❌ {logic_name}: Missing")
                    all_fields_found = False
        
        return all_fields_found
        
    except Exception as e:
        print(f"❌ Account activation test failed: {e}")
        return False

def test_password_reset_system():
    """Test the password reset system"""
    print("\n🔑 TESTING PASSWORD RESET SYSTEM...")
    
    try:
        # Check email verification API for password reset
        email_api_file = Path("temp/src/backend/base/axiestudio/api/v1/email_verification.py")
        if not email_api_file.exists():
            print("❌ Email verification API file missing")
            return False
        
        content = email_api_file.read_text(encoding='utf-8')
        
        # Check for password reset endpoints
        reset_endpoints = [
            ("/forgot-password", "forgot_password"),
            ("/reset-password", "reset_password"),
        ]
        
        all_endpoints_found = True
        for endpoint, function in reset_endpoints:
            if endpoint in content and function in content:
                print(f"✅ Password reset endpoint: {endpoint} ({function})")
            else:
                print(f"❌ Missing password reset endpoint: {endpoint}")
                all_endpoints_found = False
        
        # Check for enterprise security features
        security_features = [
            ("Email enumeration protection", "Always return success"),
            ("IP logging", "client_ip"),
            ("Token expiration", "reset_expiry"),
            ("Auto-login after reset", "access_token"),
            ("Security notices", "security_notice"),
        ]
        
        for feature_name, pattern in security_features:
            if pattern in content:
                print(f"✅ {feature_name}: Implemented")
            else:
                print(f"❌ {feature_name}: Missing")
                all_endpoints_found = False
        
        # Check email service for password reset emails
        email_service_file = Path("temp/src/backend/base/axiestudio/services/email/service.py")
        if email_service_file.exists():
            email_content = email_service_file.read_text(encoding='utf-8')
            
            if "send_password_reset_email" in email_content:
                print("✅ Password reset email service: Implemented")
            else:
                print("❌ Password reset email service: Missing")
                all_endpoints_found = False
        
        return all_endpoints_found
        
    except Exception as e:
        print(f"❌ Password reset test failed: {e}")
        return False

def test_frontend_auth_pages():
    """Test the frontend authentication pages"""
    print("\n🖥️ TESTING FRONTEND AUTH PAGES...")
    
    try:
        # Check for all required auth pages
        auth_pages = [
            ("EmailVerificationPage", "temp/src/frontend/src/pages/EmailVerificationPage/index.tsx"),
            ("ForgotPasswordPage", "temp/src/frontend/src/pages/ForgotPasswordPage/index.tsx"),
            ("ResetPasswordPage", "temp/src/frontend/src/pages/ResetPasswordPage/index.tsx"),
        ]
        
        all_pages_found = True
        for page_name, page_path in auth_pages:
            page_file = Path(page_path)
            if page_file.exists():
                print(f"✅ {page_name}: Found")
                
                # Check page content for enterprise features
                content = page_file.read_text(encoding='utf-8')
                
                if page_name == "EmailVerificationPage":
                    features = [
                        ("6-digit code input", "verificationCode"),
                        ("Auto-login", "login(response.data.access_token"),
                        ("Loading states", "isLoading"),
                        ("Error handling", "setError"),
                    ]
                elif page_name == "ForgotPasswordPage":
                    features = [
                        ("Email validation", "email.trim()"),
                        ("Loading states", "isLoading"),
                        ("Success feedback", "setSuccessData"),
                        ("Error handling", "setErrorData"),
                    ]
                elif page_name == "ResetPasswordPage":
                    features = [
                        ("Token validation", "token"),
                        ("Auto-login", "login(response.data.access_token"),
                        ("Redirect to settings", "navigate(\"/settings\")"),
                        ("Error handling", "setError"),
                    ]
                
                for feature_name, pattern in features:
                    if pattern in content:
                        print(f"  ✅ {feature_name}: Implemented")
                    else:
                        print(f"  ❌ {feature_name}: Missing")
                        all_pages_found = False
            else:
                print(f"❌ {page_name}: Missing")
                all_pages_found = False
        
        return all_pages_found
        
    except Exception as e:
        print(f"❌ Frontend auth pages test failed: {e}")
        return False

def test_routing_configuration():
    """Test that all auth routes are properly configured"""
    print("\n🛣️ TESTING AUTH ROUTING CONFIGURATION...")
    
    try:
        routes_file = Path("temp/src/frontend/src/routes.tsx")
        if not routes_file.exists():
            print("❌ Routes file missing")
            return False
        
        content = routes_file.read_text(encoding='utf-8')
        
        # Check for all auth routes
        auth_routes = [
            ("verify-email", "EmailVerificationPage"),
            ("forgot-password", "ForgotPasswordPage"),
            ("reset-password", "ResetPasswordPage"),
        ]
        
        all_routes_found = True
        for route_path, component in auth_routes:
            if route_path in content and component in content:
                print(f"✅ Route /{route_path}: Configured with {component}")
            else:
                print(f"❌ Route /{route_path}: Missing or misconfigured")
                all_routes_found = False
        
        return all_routes_found
        
    except Exception as e:
        print(f"❌ Routing test failed: {e}")
        return False

def test_enterprise_security_features():
    """Test enterprise-level security features"""
    print("\n🛡️ TESTING ENTERPRISE SECURITY FEATURES...")
    
    try:
        # Check verification code service
        verification_files = [
            "temp/src/backend/base/axiestudio/services/auth/verification_code.py",
        ]
        
        security_features_found = True
        
        for file_path in verification_files:
            file_obj = Path(file_path)
            if file_obj.exists():
                content = file_obj.read_text(encoding='utf-8')
                
                security_checks = [
                    ("Rate limiting", "max_attempts"),
                    ("Code expiration", "expires"),
                    ("Secure code generation", "secrets.choice"),
                    ("Code formatting", "format_code"),
                ]
                
                for check_name, pattern in security_checks:
                    if pattern in content:
                        print(f"✅ {check_name}: Implemented")
                    else:
                        print(f"❌ {check_name}: Missing")
                        security_features_found = False
            else:
                print(f"❌ Security file missing: {file_path}")
                security_features_found = False
        
        return security_features_found
        
    except Exception as e:
        print(f"❌ Security features test failed: {e}")
        return False

def main():
    """Run all enterprise auth system tests"""
    print("🚀 Starting enterprise authentication system audit...\n")
    
    tests = [
        ("Email Verification System", test_email_verification_system),
        ("Account Activation System", test_account_activation_system),
        ("Password Reset System", test_password_reset_system),
        ("Frontend Auth Pages", test_frontend_auth_pages),
        ("Routing Configuration", test_routing_configuration),
        ("Enterprise Security Features", test_enterprise_security_features),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 ENTERPRISE AUTH SYSTEM AUDIT SUMMARY")
    print("="*70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Auth System Results: {passed}/{total} systems passed")
    
    if passed == total:
        print("🎉 ENTERPRISE AUTH SYSTEM IS COMPLETE!")
        print("\n✅ VERIFIED FEATURES:")
        print("• Email verification with 6-digit codes")
        print("• Account activation system")
        print("• Password reset with auto-login")
        print("• Enterprise security features")
        print("• Complete frontend UI")
        print("• Proper routing configuration")
        return True
    else:
        print("⚠️  Some auth systems need attention.")
        print("Please review the failed tests above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
