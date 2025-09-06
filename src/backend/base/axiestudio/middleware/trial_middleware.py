"""Enhanced middleware for trial status checking and comprehensive abuse protection."""

import time
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Set

from fastapi import HTTPException, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

from axiestudio.services.trial.service import trial_service
from axiestudio.services.auth.utils import get_current_user_by_jwt
from axiestudio.services.deps import get_db_service
from axiestudio.services.trial.abuse_prevention import trial_abuse_prevention


class EnhancedTrialMiddleware(BaseHTTPMiddleware):
    """
    🛡️ ENHANCED TRIAL PROTECTION MIDDLEWARE

    This middleware provides comprehensive trial abuse protection with multiple layers:

    1. **Trial Status Enforcement**: Blocks expired trial users from accessing protected resources
    2. **Admin Bypass**: Superusers always have unlimited access
    3. **Smart Path Management**: Different protection levels for different endpoints
    4. **Abuse Prevention Integration**: Works with abuse prevention service
    5. **Real-time Monitoring**: Logs all trial-related access attempts

    WHY THIS IMPLEMENTATION:
    - Prevents revenue loss from expired trial users continuing to use the service
    - Protects against trial abuse (multiple accounts, extended usage without payment)
    - Maintains good UX by allowing access to essential paths (login, pricing, etc.)
    - Provides clear feedback to users about their trial status
    - Integrates with Stripe subscription system for seamless payment flow
    """

    def __init__(self, app):
        super().__init__(app)

        # 🔒 CRITICAL PROTECTION PATHS - These require active trial/subscription
        self.protected_paths = {
            "/api/v1/flows",           # Core AI/ML functionality
            "/api/v1/files",           # File operations
            "/api/v1/chat",            # Chat/AI features
            "/api/v1/components",      # Component access
            "/api/v1/projects",        # Project management
            "/api/v1/builds",          # Build operations
            "/api/v1/variables",       # Variable management
        }

        # 🟡 TRIAL-ACCESSIBLE PATHS - Allow even with expired trial for UX
        self.trial_exempt_paths = {
            "/api/v1/subscriptions",   # Must allow subscription management
            "/api/v1/login",           # Authentication required
            "/api/v1/logout",          # Always allow logout
            "/api/v1/refresh",         # Token refresh needed
            "/api/v1/users/whoami",    # User info needed for UI
            "/api/v1/users/trial-status",  # Trial status checking
            "/api/v1/users/",          # User creation (signup)
            "/api/v1/email",           # Email verification
        }

        # 🟢 ALWAYS ALLOW PATHS - No restrictions whatsoever
        self.always_allow_paths = {
            "/health",                 # Health checks
            "/docs",                   # API documentation
            "/openapi.json",           # OpenAPI spec
            "/static",                 # Static assets
            "/login",                  # Login page
            "/signup",                 # Signup page
            "/pricing",                # Pricing page (critical for conversions)
            "/subscription-success",   # Post-payment success
            "/subscription-cancel",    # Payment cancellation
        }

        # 📊 Rate limiting for trial users (prevent abuse)
        self.trial_rate_limits = defaultdict(list)
        self.trial_rate_window = 300  # 5 minutes
        self.trial_max_requests = 100  # Max requests per window for trial users

        # 🚨 Suspicious activity tracking
        self.suspicious_ips = set()
        self.failed_trial_checks = defaultdict(int)

        logger.info("🛡️ Enhanced Trial Protection Middleware initialized")
        logger.info(f"🔒 Protected paths: {len(self.protected_paths)}")
        logger.info(f"🟡 Trial-exempt paths: {len(self.trial_exempt_paths)}")
        logger.info(f"🟢 Always-allow paths: {len(self.always_allow_paths)}")

    async def dispatch(self, request: Request, call_next):
        """
        🛡️ ENHANCED TRIAL PROTECTION DISPATCH

        This method implements a comprehensive trial protection system with multiple layers:

        1. **Path-based Protection**: Different rules for different endpoint types
        2. **Rate Limiting**: Prevents abuse from trial users
        3. **Suspicious Activity Detection**: Identifies and blocks potential abuse
        4. **Admin Bypass**: Superusers get unlimited access
        5. **Graceful Degradation**: Fails safely if services are unavailable

        WHY THIS APPROACH:
        - Prevents revenue loss from expired users continuing to use premium features
        - Maintains good UX by allowing access to essential functions
        - Protects against automated abuse and bot attacks
        - Provides clear feedback for legitimate users to upgrade
        - Integrates seamlessly with existing authentication flow
        """

        start_time = time.time()
        client_ip = trial_abuse_prevention.extract_client_ip(request)
        request_path = request.url.path

        try:
            # 🟢 ALWAYS ALLOW - No restrictions for essential paths
            if any(request_path.startswith(path) for path in self.always_allow_paths):
                logger.debug(f"🟢 Always allowing path: {request_path}")
                return await call_next(request)

            # 🔍 SUSPICIOUS IP CHECK - Block known bad actors
            if client_ip in self.suspicious_ips:
                logger.warning(f"🚨 Blocking request from suspicious IP: {client_ip}")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Access temporarily restricted. Please contact support if you believe this is an error.",
                        "retry_after": 3600  # 1 hour
                    }
                )

            # 🔐 AUTHENTICATION CHECK - Get user if authenticated
            auth_header = request.headers.get("Authorization")
            user = None

            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                db_service = get_db_service()

                if db_service:
                    try:
                        async with db_service.with_session() as session:
                            user = await get_current_user_by_jwt(token, session)
                    except Exception as e:
                        logger.debug(f"JWT validation failed: {e}")

            # 🟡 TRIAL-EXEMPT PATHS - Allow even for expired trials (UX critical)
            if any(request_path.startswith(path) for path in self.trial_exempt_paths):
                logger.debug(f"🟡 Trial-exempt path: {request_path}")
                if user:
                    request.state.user = user
                return await call_next(request)

            # 🔓 NON-API REQUESTS - Let frontend handle routing
            if not request_path.startswith("/api/"):
                return await call_next(request)

            # 🔒 PROTECTED API ENDPOINTS - Require active trial/subscription
            if any(request_path.startswith(path) for path in self.protected_paths):
                if not user:
                    # No authentication for protected resource
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Authentication required for this resource"}
                    )

                # 👑 ADMIN BYPASS - Superusers get unlimited access
                if user.is_superuser:
                    logger.debug(f"👑 Admin bypass for user: {user.username}")
                    request.state.user = user
                    request.state.trial_status = {"status": "admin", "unlimited": True}
                    return await call_next(request)

                # 📊 RATE LIMITING FOR TRIAL USERS
                if not await self._check_rate_limit(user, client_ip):
                    logger.warning(f"📊 Rate limit exceeded for user: {user.username}")
                    return JSONResponse(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        content={
                            "detail": "Rate limit exceeded. Please upgrade to remove limits.",
                            "upgrade_url": "/pricing"
                        }
                    )

                # 🔍 TRIAL STATUS CHECK
                try:
                    trial_status = await trial_service.check_trial_status(user)

                    # 🚨 TRIAL EXPIRED - Block access to protected resources
                    if trial_status.get("should_cleanup", False):
                        logger.info(f"🚨 Blocking expired trial user: {user.username} from {request_path}")

                        # Track failed attempts for abuse detection
                        self.failed_trial_checks[client_ip] += 1
                        if self.failed_trial_checks[client_ip] > 10:
                            self.suspicious_ips.add(client_ip)
                            logger.warning(f"🚨 IP {client_ip} marked as suspicious due to repeated trial violations")

                        return JSONResponse(
                            status_code=status.HTTP_402_PAYMENT_REQUIRED,
                            content={
                                "detail": "Your free trial has expired. Please subscribe to continue using Axie Studio.",
                                "trial_expired": True,
                                "subscription_required": True,
                                "redirect_to": "/pricing",
                                "days_expired": abs(trial_status.get("days_left", 0)),
                                "upgrade_benefits": [
                                    "Unlimited AI/ML workflows",
                                    "Advanced components access",
                                    "Priority support",
                                    "Export capabilities"
                                ]
                            }
                        )

                    # ✅ VALID TRIAL/SUBSCRIPTION - Allow access
                    request.state.trial_status = trial_status
                    request.state.user = user

                    # Log successful access for monitoring
                    logger.debug(f"✅ Trial access granted: {user.username} -> {request_path} (status: {trial_status.get('status')})")

                except Exception as e:
                    logger.warning(f"Trial service error for user {user.username}: {e}")
                    # Fail safely - allow access but log the issue
                    request.state.user = user

            # 🔓 OTHER API ENDPOINTS - Allow with user context if available
            else:
                if user:
                    request.state.user = user

        except Exception as e:
            # 🛡️ FAIL SAFELY - Never break the application due to middleware errors
            logger.error(f"🛡️ Trial middleware error: {e}")
            if user:
                request.state.user = user

        # 📈 PERFORMANCE MONITORING
        processing_time = time.time() - start_time
        if processing_time > 0.1:  # Log slow middleware operations
            logger.warning(f"📈 Slow trial middleware: {processing_time:.3f}s for {request_path}")

        return await call_next(request)

    async def _check_rate_limit(self, user, client_ip: str) -> bool:
        """
        📊 RATE LIMITING FOR TRIAL USERS

        WHY THIS IS IMPORTANT:
        - Prevents abuse of free trial resources
        - Protects against automated scraping/bot attacks
        - Encourages legitimate users to upgrade to paid plans
        - Maintains service quality for all users

        IMPLEMENTATION DETAILS:
        - Trial users: 100 requests per 5 minutes
        - Subscribed users: No limits
        - Rate limiting based on user ID + IP combination
        - Automatic cleanup of old rate limit data
        """
        now = time.time()

        # Subscribed users have no rate limits
        if hasattr(user, 'subscription_status') and user.subscription_status == "active":
            return True

        # Create rate limit key combining user and IP
        rate_key = f"{user.id}:{client_ip}"

        # Clean old entries
        self.trial_rate_limits[rate_key] = [
            timestamp for timestamp in self.trial_rate_limits[rate_key]
            if now - timestamp < self.trial_rate_window
        ]

        # Check if limit exceeded
        if len(self.trial_rate_limits[rate_key]) >= self.trial_max_requests:
            return False

        # Add current request
        self.trial_rate_limits[rate_key].append(now)
        return True

    def get_protection_stats(self) -> dict:
        """
        📊 GET PROTECTION STATISTICS

        Returns current protection statistics for monitoring and debugging.
        Useful for admin dashboards and security monitoring.
        """
        return {
            "suspicious_ips_count": len(self.suspicious_ips),
            "suspicious_ips": list(self.suspicious_ips),
            "failed_trial_checks": dict(self.failed_trial_checks),
            "active_rate_limits": len(self.trial_rate_limits),
            "protected_paths": list(self.protected_paths),
            "trial_exempt_paths": list(self.trial_exempt_paths),
            "always_allow_paths": list(self.always_allow_paths)
        }


# 🔄 BACKWARD COMPATIBILITY - Keep old class name as alias
TrialMiddleware = EnhancedTrialMiddleware


# 📊 GLOBAL INSTANCE FOR MONITORING
enhanced_trial_middleware_instance = None

def get_trial_middleware_stats() -> dict:
    """Get current trial middleware protection statistics."""
    global enhanced_trial_middleware_instance
    if enhanced_trial_middleware_instance:
        return enhanced_trial_middleware_instance.get_protection_stats()
    return {"error": "Middleware not initialized"}
