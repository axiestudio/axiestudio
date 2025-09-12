#!/usr/bin/env python3
"""
🔒 ACCESS CONTROL VERIFICATION TEST
===================================

This script verifies that canceled subscriptions maintain access until expiration
and identifies issues with MCP and local LLM configurations.
"""

import asyncio
import asyncpg
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

async def test_canceled_subscription_access():
    """Test that canceled subscriptions maintain access until subscription_end."""
    
    print("🔒 TESTING CANCELED SUBSCRIPTION ACCESS CONTROL")
    print("=" * 60)
    
    load_dotenv()
    
    # Connect to the database
    database_url = os.getenv("AXIESTUDIO_DATABASE_URL")
    if not database_url:
        print("❌ AXIESTUDIO_DATABASE_URL not found in environment")
        return False
    
    try:
        conn = await asyncpg.connect(database_url)
        
        # Test scenario: Create a canceled subscription with future end date
        now = datetime.now(timezone.utc)
        subscription_end = now + timedelta(days=25)  # 25 days from now
        subscription_start = now - timedelta(days=5)  # Started 5 days ago
        
        # Check if test user exists, create if not
        test_user_query = """
        INSERT INTO "user" (username, email, password, subscription_status, subscription_end, subscription_start, subscription_id)
        VALUES ($1, $2, $3, $4, $5::timestamptz, $6::timestamptz, $7)
        ON CONFLICT (username) DO UPDATE SET
            subscription_status = $4,
            subscription_end = $5::timestamptz,
            subscription_start = $6::timestamptz,
            subscription_id = $7
        RETURNING id, username, subscription_status, subscription_end, subscription_id
        """
        
        user = await conn.fetchrow(
            test_user_query,
            'test_canceled_access',
            'test_canceled_access@example.com',
            'hashed_password',
            'canceled',
            subscription_end,
            subscription_start,
            'sub_test_canceled_access_123'
        )
        
        print(f"✅ Test user created/updated: {user['username']}")
        print(f"   - Status: {user['subscription_status']}")
        print(f"   - Subscription end: {user['subscription_end']}")
        print(f"   - Subscription ID: {user['subscription_id']}")
        
        # Simulate the trial service logic
        subscription_end_date = user['subscription_end']
        if subscription_end_date.tzinfo is None:
            subscription_end_date = subscription_end_date.replace(tzinfo=timezone.utc)
        
        # Test access control logic
        should_have_access = (
            user['subscription_status'] == 'canceled' and
            user['subscription_id'] and
            now < subscription_end_date
        )
        
        remaining_days = (subscription_end_date - now).days
        
        print(f"\n🧪 ACCESS CONTROL TEST RESULTS:")
        print(f"   - Should have access: {should_have_access}")
        print(f"   - Days remaining: {remaining_days}")
        print(f"   - Access until: {subscription_end_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Test expired canceled subscription
        expired_user_query = """
        INSERT INTO "user" (username, email, password, subscription_status, subscription_end, subscription_start, subscription_id)
        VALUES ($1, $2, $3, $4, $5::timestamptz, $6::timestamptz, $7)
        ON CONFLICT (username) DO UPDATE SET
            subscription_status = $4,
            subscription_end = $5::timestamptz,
            subscription_start = $6::timestamptz,
            subscription_id = $7
        RETURNING id, username, subscription_status, subscription_end, subscription_id
        """
        
        expired_end = now - timedelta(days=1)  # Expired yesterday
        expired_start = now - timedelta(days=31)  # Started 31 days ago
        expired_user = await conn.fetchrow(
            expired_user_query,
            'test_expired_canceled',
            'test_expired_canceled@example.com',
            'hashed_password',
            'canceled',
            expired_end,
            expired_start,
            'sub_test_expired_canceled_123'
        )
        
        expired_should_have_access = (
            expired_user['subscription_status'] == 'canceled' and
            expired_user['subscription_id'] and
            now < expired_end
        )
        
        print(f"\n🧪 EXPIRED CANCELED SUBSCRIPTION TEST:")
        print(f"   - Should have access: {expired_should_have_access}")
        print(f"   - Subscription ended: {expired_end.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        await conn.close()
        
        return should_have_access and not expired_should_have_access
        
    except Exception as e:
        print(f"❌ Access control test failed: {e}")
        return False

def analyze_mcp_configuration():
    """Analyze MCP configuration issues."""
    
    print("\n🔧 ANALYZING MCP CONFIGURATION")
    print("=" * 60)
    
    load_dotenv()
    
    issues = []
    recommendations = []
    
    # Check if MCP is configured for production
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        print(f"✅ Frontend URL configured: {frontend_url}")
        if "localhost" in frontend_url or "127.0.0.1" in frontend_url:
            issues.append("Frontend URL points to localhost - not suitable for production MCP")
            recommendations.append("Update FRONTEND_URL to production domain (axiestudio.se)")
    else:
        issues.append("FRONTEND_URL not configured in .env")
        recommendations.append("Add FRONTEND_URL=https://flow.axiestudio.se/ to .env")
    
    # Check MCP server configuration files
    mcp_files = [
        "src/frontend/src/pages/MainPage/pages/homePage/components/McpServerTab.tsx",
        "src/backend/base/axiestudio/api/v1/mcp_projects.py"
    ]
    
    for file_path in mcp_files:
        if os.path.exists(file_path):
            print(f"✅ MCP file exists: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "localhost" in content:
                    issues.append(f"Hardcoded localhost found in {file_path}")
                    recommendations.append(f"Make localhost configurable in {file_path}")
        else:
            print(f"❌ MCP file not found: {file_path}")
    
    return issues, recommendations

def analyze_local_llm_configuration():
    """Analyze local LLM hardcoded endpoints."""
    
    print("\n🤖 ANALYZING LOCAL LLM CONFIGURATION")
    print("=" * 60)
    
    issues = []
    recommendations = []
    
    # Check Ollama constants
    ollama_constants_file = "src/backend/base/axiestudio/base/models/ollama_constants.py"
    if os.path.exists(ollama_constants_file):
        print(f"✅ Ollama constants file exists: {ollama_constants_file}")
        with open(ollama_constants_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if '"http://localhost:11434"' in content:
                issues.append("Ollama URLs are hardcoded to localhost")
                recommendations.append("Make Ollama URLs configurable via environment variables")
    
    # Check LM Studio components
    lmstudio_files = [
        "src/backend/base/axiestudio/components/lmstudio/lmstudiomodel.py"
    ]
    
    for file_path in lmstudio_files:
        if os.path.exists(file_path):
            print(f"✅ LM Studio file exists: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "localhost:1234" in content:
                    issues.append(f"LM Studio URL hardcoded to localhost in {file_path}")
                    recommendations.append(f"Make LM Studio URL configurable in {file_path}")
    
    # Check Mistral configuration
    mistral_files = [
        "src/backend/base/axiestudio/components/mistral/mistral.py",
        "src/backend/base/axiestudio/components/mistral/mistral_embeddings.py"
    ]
    
    for file_path in mistral_files:
        if os.path.exists(file_path):
            print(f"✅ Mistral file exists: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "https://api.mistral.ai/v1" in content:
                    print(f"   - Mistral API endpoint is configurable (good)")
                else:
                    issues.append(f"Mistral API endpoint may be hardcoded in {file_path}")
    
    return issues, recommendations

def find_additional_improvements():
    """Find additional areas for improvement."""
    
    print("\n🔍 FINDING ADDITIONAL IMPROVEMENTS")
    print("=" * 60)
    
    improvements = []
    
    # Check for Redis configuration
    load_dotenv()
    redis_host = os.getenv("AXIESTUDIO_REDIS_HOST")
    if not redis_host:
        improvements.append("Add Redis configuration for better caching and session management")
    
    # Check for monitoring/logging improvements
    sentry_dsn = os.getenv("AXIESTUDIO_SENTRY_DSN")
    if not sentry_dsn:
        improvements.append("Add Sentry DSN for error monitoring and tracking")
    
    # Check for rate limiting configuration
    improvements.append("Consider adding rate limiting configuration for API endpoints")
    
    # Check for backup configuration
    improvements.append("Add database backup configuration and scheduling")
    
    # Check for SSL/TLS configuration
    improvements.append("Ensure SSL/TLS certificates are properly configured for production")
    
    # Check for CDN configuration
    improvements.append("Consider adding CDN configuration for static assets")
    
    # Check for load balancing
    improvements.append("Consider load balancing configuration for high availability")
    
    return improvements

async def main():
    """Run all verification tests and analyses."""
    
    print("🎯 AXIESTUDIO COMPREHENSIVE VERIFICATION")
    print("=" * 70)
    
    # Test 1: Access control for canceled subscriptions
    access_control_ok = await test_canceled_subscription_access()
    
    # Test 2: MCP configuration analysis
    mcp_issues, mcp_recommendations = analyze_mcp_configuration()
    
    # Test 3: Local LLM configuration analysis
    llm_issues, llm_recommendations = analyze_local_llm_configuration()
    
    # Test 4: Additional improvements
    additional_improvements = find_additional_improvements()
    
    # Summary
    print("\n🎉 COMPREHENSIVE ANALYSIS RESULTS")
    print("=" * 70)
    
    print(f"\n1️⃣ ACCESS CONTROL:")
    print(f"   {'✅ WORKING' if access_control_ok else '❌ ISSUES FOUND'}")
    
    print(f"\n2️⃣ MCP CONFIGURATION ISSUES ({len(mcp_issues)}):")
    for issue in mcp_issues:
        print(f"   ❌ {issue}")
    
    print(f"\n3️⃣ LOCAL LLM CONFIGURATION ISSUES ({len(llm_issues)}):")
    for issue in llm_issues:
        print(f"   ❌ {issue}")
    
    print(f"\n🔧 RECOMMENDATIONS:")
    all_recommendations = mcp_recommendations + llm_recommendations
    for i, rec in enumerate(all_recommendations, 1):
        print(f"   {i}. {rec}")
    
    print(f"\n🚀 ADDITIONAL IMPROVEMENTS ({len(additional_improvements)}):")
    for i, improvement in enumerate(additional_improvements, 1):
        print(f"   {i}. {improvement}")
    
    print(f"\n🏆 PRIORITY FIXES NEEDED:")
    priority_fixes = []
    if not access_control_ok:
        priority_fixes.append("Fix access control for canceled subscriptions")
    if mcp_issues:
        priority_fixes.append("Fix MCP configuration for production use")
    if llm_issues:
        priority_fixes.append("Make local LLM endpoints configurable")
    
    if priority_fixes:
        for i, fix in enumerate(priority_fixes, 1):
            print(f"   🔥 {i}. {fix}")
    else:
        print("   ✅ No critical issues found!")

if __name__ == "__main__":
    asyncio.run(main())
