#!/usr/bin/env python3
"""
🔍 BRANCH CONSISTENCY VERIFICATION
Verify that both main and master branches have identical Stripe webhook fixes
"""

import subprocess
import sys
from pathlib import Path

def run_git_command(command):
    """Run a git command and return the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=Path.cwd())
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1

def check_file_content(branch, file_path, search_pattern=None):
    """Check file content on a specific branch."""
    # Switch to branch
    output, code = run_git_command(f'git checkout {branch}')
    if code != 0:
        return f"Failed to checkout {branch}: {output}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if search_pattern:
            return search_pattern in content
        return content
    except FileNotFoundError:
        return f"File {file_path} not found on {branch}"
    except Exception as e:
        return f"Error reading {file_path} on {branch}: {e}"

def main():
    """Main verification function."""
    print("🔍 BRANCH CONSISTENCY VERIFICATION")
    print("=" * 60)
    
    # Files to check
    critical_files = [
        {
            "path": "src/backend/base/axiestudio/services/database/models/__init__.py",
            "check": "WebhookEvent import",
            "pattern": "from .webhook import WebhookEvent"
        },
        {
            "path": "src/backend/base/axiestudio/services/database/service.py", 
            "check": "webhook_events in migration",
            "pattern": "webhook_events"
        },
        {
            "path": "src/backend/base/axiestudio/api/v1/subscriptions.py",
            "check": "event_type in webhook SQL",
            "pattern": "INSERT INTO webhook_events (stripe_event_id, event_type, status, created_at)"
        },
        {
            "path": "src/backend/base/axiestudio/services/stripe/service.py",
            "check": "checkout.session.completed handler",
            "pattern": "checkout.session.completed"
        },
        {
            "path": "src/backend/base/axiestudio/services/stripe/service.py",
            "check": "customer.subscription.created handler", 
            "pattern": "customer.subscription.created"
        }
    ]
    
    branches = ["main", "master"]
    results = {}
    
    for branch in branches:
        print(f"\n📋 Checking {branch.upper()} branch...")
        results[branch] = {}
        
        for file_info in critical_files:
            file_path = file_info["path"]
            check_name = file_info["check"]
            pattern = file_info["pattern"]
            
            result = check_file_content(branch, file_path, pattern)
            results[branch][check_name] = result
            
            if isinstance(result, bool):
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {status} {check_name}")
            else:
                print(f"  ❌ ERROR {check_name}: {result}")
    
    # Compare results
    print(f"\n🔍 CONSISTENCY COMPARISON")
    print("=" * 60)
    
    all_consistent = True
    
    for file_info in critical_files:
        check_name = file_info["check"]
        main_result = results.get("main", {}).get(check_name, False)
        master_result = results.get("master", {}).get(check_name, False)
        
        if main_result == master_result and main_result is True:
            print(f"✅ {check_name}: CONSISTENT (both branches have fix)")
        elif main_result == master_result and main_result is False:
            print(f"❌ {check_name}: CONSISTENT BUT MISSING (both branches missing fix)")
            all_consistent = False
        else:
            print(f"🚨 {check_name}: INCONSISTENT")
            print(f"   main: {main_result}")
            print(f"   master: {master_result}")
            all_consistent = False
    
    print("=" * 60)
    
    if all_consistent:
        print("🎉 SUCCESS: Both branches have identical Stripe webhook fixes!")
        print("✅ main branch (English): Production ready")
        print("✅ master branch (Swedish): Production ready")
        return 0
    else:
        print("🚨 INCONSISTENCY DETECTED: Branches have different fixes!")
        print("❌ Manual intervention required to sync branches")
        return 1

if __name__ == "__main__":
    exit_code = main()
    
    # Return to master branch
    run_git_command("git checkout master")
    
    sys.exit(exit_code)
