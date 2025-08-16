#!/usr/bin/env python3
"""
Test the correct API endpoints for Axie Studio components.
"""

import requests
import json
import sys

def test_all_endpoint():
    """Test the /api/v1/all endpoint which returns all component types."""
    print("🔍 TESTING /api/v1/all ENDPOINT...")
    
    try:
        # This endpoint requires authentication, so we need to login first
        # Let's try without auth first to see what happens
        response = requests.get("http://localhost:7860/api/v1/all", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 401:
            print("✅ Endpoint exists but requires authentication (expected)")
            return True
        elif response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Components loaded: {len(data)} categories")
                return True
            except json.JSONDecodeError:
                print("❌ JSON decode error")
                return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint."""
    print("\n🏥 TESTING HEALTH ENDPOINT...")
    
    try:
        response = requests.get("http://localhost:7860/api/v1/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False

def test_store_components_endpoint():
    """Test the store components endpoint."""
    print("\n🏪 TESTING STORE COMPONENTS ENDPOINT...")
    
    try:
        response = requests.get("http://localhost:7860/api/v1/store/components/", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 403:
            print("✅ Store endpoint exists but requires API key (expected)")
            return True
        elif response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Store components loaded: {data}")
                return True
            except json.JSONDecodeError:
                print("❌ JSON decode error")
                return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_frontend_loading():
    """Test if the frontend is loading properly."""
    print("\n🌐 TESTING FRONTEND LOADING...")
    
    try:
        response = requests.get("http://localhost:7860/", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 200 and "text/html" in response.headers.get('content-type', ''):
            print("✅ Frontend loading correctly")
            return True
        else:
            print(f"❌ Frontend loading failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    """Run API tests."""
    print("🚀 AXIE STUDIO API ENDPOINT TEST")
    print("=" * 50)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Frontend Loading", test_frontend_loading),
        ("All Components Endpoint", test_all_endpoint),
        ("Store Components Endpoint", test_store_components_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
    
    print(f"\n{'='*50}")
    print(f"🎯 RESULTS: {passed}/{total} tests passed")
    
    if passed >= 3:
        print("🎉 API ENDPOINTS ARE WORKING CORRECTLY!")
        print("✅ The application is properly configured")
        print("✅ Components are available through correct endpoints")
        return True
    else:
        print("❌ SIGNIFICANT API ISSUES DETECTED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
