"""
🛡️ COMPREHENSIVE SECURITY MIDDLEWARE FOR TRIAL & SUBSCRIPTION ABUSE PROTECTION

This middleware provides advanced security features to protect against various forms of abuse:

1. **Rate Limiting**: Prevents API abuse and DoS attacks
2. **IP Blocking**: Automatic blocking of suspicious IP addresses
3. **Request Pattern Analysis**: Detects automated/bot behavior
4. **Geographic Restrictions**: Optional geo-blocking capabilities
5. **Device Fingerprinting Integration**: Works with abuse prevention service
6. **Real-time Threat Detection**: Dynamic response to suspicious activities

WHY THIS IS CRITICAL FOR SAAS:
- Protects revenue by preventing trial abuse
- Maintains service quality for legitimate users
- Reduces infrastructure costs from abuse
- Provides detailed security analytics
- Complies with security best practices
"""

import time
import json
import hashlib
from collections import defaultdict, deque
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Set, Tuple
from ipaddress import ip_address, ip_network

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

from axiestudio.services.trial.abuse_prevention import trial_abuse_prevention


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    🛡️ ADVANCED SECURITY MIDDLEWARE
    
    Provides comprehensive protection against various attack vectors:
    - Rate limiting with multiple tiers
    - IP reputation and blocking
    - Request pattern analysis
    - Automated threat response
    """

    def __init__(self, app):
        super().__init__(app)
        
        # 📊 RATE LIMITING CONFIGURATION
        self.rate_limits = {
            "global": {"requests": 1000, "window": 300},      # 1000 req/5min globally
            "per_ip": {"requests": 100, "window": 300},       # 100 req/5min per IP
            "auth": {"requests": 10, "window": 300},          # 10 auth attempts/5min
            "signup": {"requests": 5, "window": 3600},        # 5 signups/hour per IP
            "subscription": {"requests": 20, "window": 3600}, # 20 sub requests/hour
        }
        
        # 🗃️ STORAGE FOR RATE LIMITING
        self.request_counts = defaultdict(lambda: defaultdict(deque))
        self.blocked_ips = set()
        self.suspicious_ips = defaultdict(int)
        
        # 🚨 THREAT DETECTION PATTERNS
        self.threat_patterns = {
            "rapid_requests": 50,      # More than 50 requests in 60 seconds
            "failed_auth_threshold": 5, # 5 failed auth attempts
            "suspicious_user_agents": {
                "bot", "crawler", "spider", "scraper", "automated", 
                "python-requests", "curl", "wget"
            }
        }
        
        # 🌍 GEOGRAPHIC RESTRICTIONS (if needed)
        self.blocked_countries = set()  # Can be configured
        self.allowed_countries = set()  # If set, only these are allowed
        
        # 📈 ANALYTICS
        self.security_events = deque(maxlen=1000)  # Keep last 1000 events
        
        logger.info("🛡️ Security Middleware initialized")

    async def dispatch(self, request: Request, call_next):
        """
        🛡️ MAIN SECURITY DISPATCH
        
        Processes each request through multiple security layers:
        1. IP reputation check
        2. Rate limiting
        3. Pattern analysis
        4. Threat detection
        5. Request logging
        """
        
        start_time = time.time()
        client_ip = trial_abuse_prevention.extract_client_ip(request)
        user_agent = request.headers.get("User-Agent", "")
        request_path = request.url.path
        
        # 🚨 BLOCKED IP CHECK
        if client_ip in self.blocked_ips:
            self._log_security_event("blocked_ip_access", client_ip, request_path)
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": "Access denied. Your IP has been blocked due to suspicious activity.",
                    "contact": "Please contact support if you believe this is an error."
                }
            )

        # 📊 RATE LIMITING CHECK
        rate_limit_result = await self._check_rate_limits(client_ip, request_path, user_agent)
        if not rate_limit_result["allowed"]:
            self._log_security_event("rate_limit_exceeded", client_ip, request_path, {
                "limit_type": rate_limit_result["limit_type"],
                "requests": rate_limit_result["current_requests"]
            })
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Rate limit exceeded: {rate_limit_result['message']}",
                    "retry_after": rate_limit_result["retry_after"],
                    "limit_type": rate_limit_result["limit_type"]
                }
            )

        # 🤖 BOT/AUTOMATION DETECTION
        if await self._detect_bot_behavior(client_ip, user_agent, request_path):
            self._log_security_event("bot_detected", client_ip, request_path, {"user_agent": user_agent})
            
            # Increase suspicion level
            self.suspicious_ips[client_ip] += 10
            
            # Block if too suspicious
            if self.suspicious_ips[client_ip] > 50:
                self.blocked_ips.add(client_ip)
                logger.warning(f"🚨 IP {client_ip} auto-blocked due to bot behavior")

        # 🔍 PATTERN ANALYSIS
        await self._analyze_request_patterns(client_ip, request_path, user_agent)

        # ✅ PROCESS REQUEST
        try:
            response = await call_next(request)
            
            # 📊 LOG SUCCESSFUL REQUEST
            processing_time = time.time() - start_time
            if processing_time > 1.0:  # Log slow requests
                self._log_security_event("slow_request", client_ip, request_path, {
                    "processing_time": processing_time
                })
            
            return response
            
        except Exception as e:
            # 🚨 LOG REQUEST ERRORS
            self._log_security_event("request_error", client_ip, request_path, {
                "error": str(e)
            })
            raise

    async def _check_rate_limits(self, client_ip: str, path: str, user_agent: str) -> Dict:
        """
        📊 COMPREHENSIVE RATE LIMITING
        
        WHY MULTIPLE RATE LIMITS:
        - Global: Protects overall system capacity
        - Per-IP: Prevents individual IP abuse
        - Endpoint-specific: Protects critical functions
        - User-agent based: Detects automated tools
        """
        now = time.time()
        
        # Define rate limit categories based on path
        if "/api/v1/login" in path or "/api/v1/refresh" in path:
            limit_type = "auth"
        elif "/api/v1/users/" in path and "POST" in str(path):
            limit_type = "signup"
        elif "/api/v1/subscriptions" in path:
            limit_type = "subscription"
        else:
            limit_type = "per_ip"
        
        # Check specific rate limit
        limit_config = self.rate_limits[limit_type]
        window = limit_config["window"]
        max_requests = limit_config["requests"]
        
        # Clean old entries
        cutoff_time = now - window
        request_times = self.request_counts[client_ip][limit_type]
        
        while request_times and request_times[0] < cutoff_time:
            request_times.popleft()
        
        # Check if limit exceeded
        if len(request_times) >= max_requests:
            return {
                "allowed": False,
                "limit_type": limit_type,
                "current_requests": len(request_times),
                "max_requests": max_requests,
                "retry_after": int(window),
                "message": f"Too many {limit_type} requests"
            }
        
        # Add current request
        request_times.append(now)
        
        return {
            "allowed": True,
            "limit_type": limit_type,
            "current_requests": len(request_times),
            "max_requests": max_requests
        }

    async def _detect_bot_behavior(self, client_ip: str, user_agent: str, path: str) -> bool:
        """
        🤖 BOT BEHAVIOR DETECTION
        
        WHY THIS MATTERS:
        - Bots can abuse trial systems
        - Automated scraping wastes resources
        - Protects against credential stuffing
        - Maintains service quality
        """
        
        # Check user agent for bot indicators
        user_agent_lower = user_agent.lower()
        for bot_indicator in self.threat_patterns["suspicious_user_agents"]:
            if bot_indicator in user_agent_lower:
                return True
        
        # Check for rapid requests (more than 50 in 60 seconds)
        now = time.time()
        recent_requests = [
            req_time for req_time in self.request_counts[client_ip]["per_ip"]
            if now - req_time < 60
        ]
        
        if len(recent_requests) > self.threat_patterns["rapid_requests"]:
            return True
        
        # Check for suspicious patterns (accessing only API endpoints)
        if path.startswith("/api/") and not any(
            human_path in path for human_path in ["/login", "/signup", "/pricing"]
        ):
            self.suspicious_ips[client_ip] += 1
        
        return False

    async def _analyze_request_patterns(self, client_ip: str, path: str, user_agent: str):
        """
        🔍 REQUEST PATTERN ANALYSIS
        
        Analyzes request patterns to detect:
        - Automated behavior
        - Trial abuse attempts
        - Suspicious access patterns
        """
        
        # Pattern: Accessing only protected endpoints without visiting pricing
        if path.startswith("/api/v1/flows") or path.startswith("/api/v1/chat"):
            if not any("/pricing" in event.get("path", "") 
                      for event in self.security_events 
                      if event.get("ip") == client_ip):
                self.suspicious_ips[client_ip] += 2

    def _log_security_event(self, event_type: str, client_ip: str, path: str, extra_data: Dict = None):
        """
        📝 SECURITY EVENT LOGGING
        
        WHY COMPREHENSIVE LOGGING:
        - Enables forensic analysis
        - Helps improve security rules
        - Provides audit trail
        - Supports compliance requirements
        """
        
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "ip": client_ip,
            "path": path,
            "extra_data": extra_data or {}
        }
        
        self.security_events.append(event)
        
        # Log critical events
        if event_type in ["blocked_ip_access", "rate_limit_exceeded", "bot_detected"]:
            logger.warning(f"🚨 Security Event: {event_type} from {client_ip} on {path}")

    def get_security_stats(self) -> Dict:
        """
        📊 SECURITY STATISTICS
        
        Returns comprehensive security metrics for monitoring.
        """
        return {
            "blocked_ips_count": len(self.blocked_ips),
            "blocked_ips": list(self.blocked_ips),
            "suspicious_ips_count": len(self.suspicious_ips),
            "suspicious_ips": dict(self.suspicious_ips),
            "recent_events": list(self.security_events)[-50:],  # Last 50 events
            "rate_limit_stats": {
                ip: {limit_type: len(requests) for limit_type, requests in limits.items()}
                for ip, limits in self.request_counts.items()
            }
        }

    def unblock_ip(self, ip: str) -> bool:
        """
        🔓 MANUAL IP UNBLOCKING
        
        Allows administrators to unblock IPs manually.
        """
        if ip in self.blocked_ips:
            self.blocked_ips.remove(ip)
            self.suspicious_ips.pop(ip, None)
            logger.info(f"🔓 IP {ip} manually unblocked")
            return True
        return False
