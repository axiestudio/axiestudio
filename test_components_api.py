#!/usr/bin/env python3
"""
Direct API test to verify components are actually working in the running application.
"""

import requests
import json
import sys

def test_components_api():
    """Test the components API directly."""
    print("🔍 TESTING COMPONENTS API DIRECTLY...")
    
    try:
        response = requests.get("http://localhost:7860/api/v1/components", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)}")
        print(f"Content Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ JSON parsed successfully")
                print(f"📦 Components loaded: {len(data)}")
                print(f"📋 Categories: {list(data.keys())[:10]}")
                
                # Check specific categories
                key_categories = ["openai", "anthropic", "input_output", "processing", "vectorstores"]
                for category in key_categories:
                    if category in data:
                        count = len(data[category]) if isinstance(data[category], dict) else 0
                        print(f"   ✅ {category}: {count} components")
                    else:
                        print(f"   ❌ {category}: Missing")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"Raw content (first 500 chars): {response.text[:500]}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_specific_component():
    """Test a specific component endpoint."""
    print("\n🔧 TESTING SPECIFIC COMPONENT...")
    
    try:
        response = requests.get("http://localhost:7860/api/v1/components/OpenAIModelComponent", timeout=10)
        print(f"OpenAI Component Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ OpenAI component loaded successfully")
            print(f"Display Name: {data.get('display_name', 'Unknown')}")
            print(f"Description: {data.get('description', 'Unknown')[:100]}...")
            return True
        else:
            print(f"❌ Failed to load OpenAI component: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

def test_flow_creation():
    """Test creating a simple flow."""
    print("\n🔄 TESTING FLOW CREATION...")
    
    simple_flow = {
        "name": "Test Flow",
        "description": "Simple test flow",
        "data": {
            "nodes": [
                {
                    "id": "1",
                    "type": "TextInputComponent",
                    "position": {"x": 100, "y": 100},
                    "data": {
                        "type": "TextInputComponent",
                        "node": {
                            "template": {
                                "input_value": {"value": "Hello World"}
                            }
                        }
                    }
                }
            ],
            "edges": []
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:7860/api/v1/flows/",
            json=simple_flow,
            timeout=30
        )
        
        print(f"Flow Creation Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"✅ Flow created successfully: {data.get('id', 'Unknown ID')}")
            return True
        else:
            print(f"❌ Flow creation failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Flow creation test failed: {e}")
        return False

def main():
    """Run comprehensive API tests."""
    print("🚀 COMPREHENSIVE API COMPONENT TEST")
    print("=" * 50)
    
    tests = [
        ("Components API", test_components_api),
        ("Specific Component", test_specific_component),
        ("Flow Creation", test_flow_creation),
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
    
    if passed == total:
        print("🎉 ALL API TESTS PASSED - PRODUCTION READY!")
    elif passed >= 2:
        print("⚠️  MOSTLY WORKING - Minor issues")
    else:
        print("❌ SIGNIFICANT ISSUES DETECTED")
    
    return passed >= 2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
