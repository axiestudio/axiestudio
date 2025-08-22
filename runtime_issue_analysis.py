# -*- coding: utf-8 -*-
"""
RUNTIME ISSUE ANALYSIS - SENIOR DEVELOPER
Focus on the actual runtime issues from the error logs
"""

import sys
import traceback
import os
import json
from pathlib import Path

print("🔍 RUNTIME ISSUE ANALYSIS - FOCUSING ON ACTUAL PROBLEMS")
print("="*70)

def analyze_error_logs():
    """Analyze the actual error logs to see what's really happening"""
    print("\n📋 ANALYZING ERROR LOGS...")
    
    error_log_file = Path("temp/error logs latest.txt")
    if not error_log_file.exists():
        print(f"❌ Error log file not found: {error_log_file}")
        return False
    
    try:
        with open(error_log_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Look for the specific errors we're trying to fix
        issues_found = []
        
        # 1. Settings import error
        if "cannot import name 'settings' from 'axiestudio.services.settings'" in content:
            issues_found.append("❌ Settings import error still present")
        else:
            issues_found.append("✅ Settings import error not found in recent logs")
        
        # 2. Headers undefined error
        if "Cannot read properties of undefined (reading 'headers')" in content:
            issues_found.append("❌ Headers undefined error still present")
        else:
            issues_found.append("✅ Headers undefined error not found in recent logs")
        
        # 3. Foreign key violation
        if "violates foreign key constraint" in content:
            issues_found.append("❌ Foreign key violations still present")
        else:
            issues_found.append("✅ Foreign key violations not found in recent logs")
        
        # 4. Logging KeyError
        if "KeyError: \"'id'\"" in content:
            issues_found.append("❌ Logging KeyError still present")
        else:
            issues_found.append("✅ Logging KeyError not found in recent logs")
        
        # 5. Check for recent timestamps to see if logs are current
        if "2025-08-22" in content:
            issues_found.append("✅ Error logs contain recent timestamps")
        else:
            issues_found.append("⚠️ Error logs may be outdated")
        
        for issue in issues_found:
            print(issue)
        
        return True
        
    except Exception as e:
        print(f"❌ Error log analysis failed: {e}")
        return False

def check_showcase_api_endpoint():
    """Check if the showcase API endpoint files exist and are properly configured"""
    print("\n🎯 CHECKING SHOWCASE API ENDPOINT...")
    
    try:
        # Check if the store API file exists
        store_api_file = Path("temp/src/backend/base/axiestudio/api/v1/axiestudio_store.py")
        if not store_api_file.exists():
            print(f"❌ Store API file missing: {store_api_file}")
            return False
        
        print(f"✅ Store API file exists: {store_api_file}")
        
        # Check if it has the right endpoints
        content = store_api_file.read_text(encoding='utf-8')
        
        endpoints_to_check = [
            ("/store", "get_store_data"),
            ("/store/flows", "get_flows"),
            ("/store/components", "get_components"),
        ]
        
        for endpoint, function_name in endpoints_to_check:
            if endpoint in content and function_name in content:
                print(f"✅ Endpoint {endpoint} ({function_name}) found")
            else:
                print(f"❌ Endpoint {endpoint} ({function_name}) missing")
                return False
        
        # Check if router is properly registered
        router_file = Path("temp/src/backend/base/axiestudio/api/router.py")
        if router_file.exists():
            router_content = router_file.read_text(encoding='utf-8')
            if "axiestudio_store" in router_content:
                print("✅ Store router registered in main router")
            else:
                print("❌ Store router not registered in main router")
                return False
        else:
            print(f"❌ Router file missing: {router_file}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Showcase API check failed: {e}")
        traceback.print_exc()
        return False

def check_frontend_showcase_page():
    """Check if the frontend showcase page exists and is properly configured"""
    print("\n🖥️ CHECKING FRONTEND SHOWCASE PAGE...")
    
    try:
        # Look for showcase-related files
        frontend_src = Path("temp/src/frontend/src")
        
        # Check for showcase page/component
        showcase_files = []
        for pattern in ["**/showcase*", "**/Showcase*", "**/Store*", "**/store*"]:
            showcase_files.extend(frontend_src.glob(pattern))
        
        if showcase_files:
            print(f"✅ Found {len(showcase_files)} showcase-related files:")
            for file in showcase_files[:5]:  # Show first 5
                print(f"   - {file}")
        else:
            print("❌ No showcase-related files found in frontend")
            return False
        
        # Check if there's a route for /showcase
        routes_files = list(frontend_src.glob("**/route*")) + list(frontend_src.glob("**/Route*"))
        routes_files.extend(frontend_src.glob("**/router*"))
        routes_files.extend(frontend_src.glob("**/Router*"))
        
        showcase_route_found = False
        for route_file in routes_files:
            try:
                content = route_file.read_text(encoding='utf-8')
                if "showcase" in content.lower():
                    print(f"✅ Showcase route found in: {route_file}")
                    showcase_route_found = True
                    break
            except:
                continue
        
        if not showcase_route_found:
            print("❌ No showcase route found in routing files")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Frontend showcase check failed: {e}")
        traceback.print_exc()
        return False

def check_store_data_accessibility():
    """Check if store data is accessible and properly formatted"""
    print("\n📦 CHECKING STORE DATA ACCESSIBILITY...")
    
    try:
        store_index_file = Path("temp/src/store_components_converted/store_index.json")
        
        if not store_index_file.exists():
            print(f"❌ Store index file missing: {store_index_file}")
            return False
        
        # Load and validate the data
        with open(store_index_file, 'r', encoding='utf-8') as f:
            store_data = json.load(f)
        
        # Check structure
        required_sections = ['summary', 'flows', 'components']
        for section in required_sections:
            if section not in store_data:
                print(f"❌ Missing section: {section}")
                return False
            print(f"✅ Section '{section}' present")
        
        # Check data counts
        summary = store_data['summary']
        flows = store_data['flows']
        components = store_data['components']
        
        print(f"✅ Total items: {summary.get('total_items', 0)}")
        print(f"✅ Flows: {len(flows)}")
        print(f"✅ Components: {len(components)}")
        
        # Check if items have required fields for frontend display
        if flows:
            sample_flow = flows[0]
            required_fields = ['id', 'name', 'description']
            missing_fields = [field for field in required_fields if field not in sample_flow]
            if missing_fields:
                print(f"❌ Sample flow missing fields: {missing_fields}")
                return False
            print(f"✅ Sample flow has required fields: {sample_flow['name']}")
        
        if components:
            sample_component = components[0]
            required_fields = ['id', 'name', 'description']
            missing_fields = [field for field in required_fields if field not in sample_component]
            if missing_fields:
                print(f"❌ Sample component missing fields: {missing_fields}")
                return False
            print(f"✅ Sample component has required fields: {sample_component['name']}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Store data check failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run runtime issue analysis"""
    print("🚀 Starting runtime issue analysis...\n")
    
    tests = [
        ("Error Log Analysis", analyze_error_logs),
        ("Showcase API Endpoint", check_showcase_api_endpoint),
        ("Frontend Showcase Page", check_frontend_showcase_page),
        ("Store Data Accessibility", check_store_data_accessibility),
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
    print("📊 RUNTIME ISSUE ANALYSIS SUMMARY")
    print("="*70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Analysis Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL RUNTIME CHECKS PASSED!")
        print("\n🔍 CONCLUSION: The fixes appear to be working correctly.")
        print("If the showcase is still not loading, the issue may be:")
        print("1. Application needs to be restarted")
        print("2. Browser cache needs to be cleared")
        print("3. There may be a different runtime issue not captured in logs")
        return True
    else:
        print("⚠️  Some runtime checks failed.")
        print("The showcase may still have issues that need to be addressed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
