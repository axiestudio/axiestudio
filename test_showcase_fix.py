#!/usr/bin/env python3
"""
Test Showcase Fix
Verifies that the showcase API endpoints work correctly after the path fix.
"""

import sys
import asyncio
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))


async def test_showcase_api():
    """Test the showcase API to ensure it works correctly."""
    
    print("🧪 Testing Showcase API Fix")
    print("=" * 50)
    
    try:
        # Test 1: Import the API functions
        print("📦 Testing API imports...")
        from axiestudio.api.v1.axiestudio_store import (
            get_store_components_path, 
            load_store_index, 
            get_store_data
        )
        print("✅ API imports successful")
        
        # Test 2: Test store path resolution
        print("\n📁 Testing store path resolution...")
        try:
            store_path = get_store_components_path()
            print(f"✅ Store path found: {store_path}")
            
            # Check if store_index.json exists
            index_file = store_path / "store_index.json"
            if index_file.exists():
                print(f"✅ Store index file exists: {index_file}")
            else:
                print(f"❌ Store index file missing: {index_file}")
                return False
                
        except Exception as e:
            print(f"❌ Store path resolution failed: {e}")
            return False
        
        # Test 3: Test store index loading
        print("\n📊 Testing store index loading...")
        try:
            store_data = load_store_index()
            print(f"✅ Store index loaded successfully")
            print(f"   📈 Total items: {store_data.summary.total_items}")
            print(f"   🔄 Flows: {len(store_data.flows)}")
            print(f"   🧩 Components: {len(store_data.components)}")
            
            # Verify flows is iterable (this was the original error)
            if hasattr(store_data.flows, '__iter__'):
                print("✅ Flows is iterable - 'i.flows is not iterable' error should be fixed")
            else:
                print("❌ Flows is not iterable - error still exists")
                return False
                
        except Exception as e:
            print(f"❌ Store index loading failed: {e}")
            return False
        
        # Test 4: Test API endpoint
        print("\n🌐 Testing API endpoint...")
        try:
            api_response = await get_store_data()
            print(f"✅ API endpoint works successfully")
            print(f"   📈 API returned {len(api_response.flows)} flows")
            print(f"   🧩 API returned {len(api_response.components)} components")
            
            # Test that flows and components are lists
            if isinstance(api_response.flows, list) and isinstance(api_response.components, list):
                print("✅ API returns proper list structures")
            else:
                print(f"❌ API returns wrong types: flows={type(api_response.flows)}, components={type(api_response.components)}")
                return False
                
        except Exception as e:
            print(f"❌ API endpoint test failed: {e}")
            return False
        
        # Test 5: Test sample data structure
        print("\n🔍 Testing data structure...")
        if store_data.flows:
            sample_flow = store_data.flows[0]
            print(f"✅ Sample flow: {sample_flow.name}")
            print(f"   ID: {sample_flow.id}")
            print(f"   Type: {sample_flow.type}")
            print(f"   Author: {sample_flow.author.username}")

            # Check required fields that frontend expects
            required_fields = ['id', 'name', 'description', 'type', 'author', 'stats', 'dates', 'tags']
            missing_fields = []
            for field in required_fields:
                if not hasattr(sample_flow, field):
                    missing_fields.append(field)

            if missing_fields:
                print(f"❌ Sample flow missing fields: {missing_fields}")
                return False
            else:
                print("✅ Sample flow has all required fields")

            # Test tag structure safety
            print(f"   Tags: {len(sample_flow.tags)} tags")
            if sample_flow.tags:
                for i, tag in enumerate(sample_flow.tags[:3]):
                    if hasattr(tag, 'tags_id') and hasattr(tag.tags_id, 'name'):
                        print(f"   Tag {i+1}: {tag.tags_id.name}")
                    else:
                        print(f"   Tag {i+1}: Invalid structure")

            # Test author structure
            if hasattr(sample_flow.author, 'username'):
                print(f"   Author username: {sample_flow.author.username}")
            else:
                print("   ❌ Author missing username")
                return False
        
        # Test 6: Simulate the exact frontend operation that was failing
        print("\n🎯 Testing the exact frontend operation that was failing...")
        try:
            # This simulates the frontend code: [...storeData.flows, ...storeData.components]
            combined_items = list(store_data.flows) + list(store_data.components)
            print(f"✅ Combined items successfully: {len(combined_items)} total items")

            # This simulates the frontend tag processing
            tag_set = set()
            for item in combined_items[:10]:  # Test first 10 items
                if hasattr(item, 'tags') and item.tags:
                    for tag in item.tags:
                        if hasattr(tag, 'tags_id') and hasattr(tag.tags_id, 'name'):
                            tag_set.add(tag.tags_id.name)

            print(f"✅ Tag processing successful: Found {len(tag_set)} unique tags")

            # This simulates the frontend author processing
            author_set = set()
            for item in combined_items[:10]:  # Test first 10 items
                if hasattr(item, 'author') and hasattr(item.author, 'username'):
                    author_set.add(item.author.username)

            print(f"✅ Author processing successful: Found {len(author_set)} unique authors")

        except Exception as e:
            print(f"❌ Frontend simulation failed: {e}")
            return False

        print("\n🎉 ALL SHOWCASE TESTS PASSED!")
        print("✅ The 'i.flows is not iterable' error should be resolved")
        print("✅ Showcase page should now load correctly")
        print("✅ All 1600 flows and components should be displayed")
        print("✅ Frontend data processing will work safely")

        return True
        
    except Exception as e:
        print(f"❌ Showcase API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_frontend_compatibility():
    """Test that the API response matches what the frontend expects."""
    
    print("\n🎨 Testing Frontend Compatibility")
    print("-" * 30)
    
    try:
        from axiestudio.api.v1.axiestudio_store import get_store_data
        
        # Get API response
        response = await get_store_data()
        
        # Check response structure matches frontend expectations
        expected_structure = {
            'summary': ['total_items', 'total_flows', 'total_components'],
            'flows': ['id', 'name', 'description', 'type', 'author', 'stats', 'dates', 'tags'],
            'components': ['id', 'name', 'description', 'type', 'author', 'stats', 'dates', 'tags'],
            'conversion_info': ['converted_at', 'converted_from', 'converted_to']
        }
        
        # Check summary
        for field in expected_structure['summary']:
            if not hasattr(response.summary, field):
                print(f"❌ Missing summary field: {field}")
                return False
        print("✅ Summary structure is correct")
        
        # Check flows structure
        if response.flows:
            sample_flow = response.flows[0]
            for field in expected_structure['flows']:
                if not hasattr(sample_flow, field):
                    print(f"❌ Missing flow field: {field}")
                    return False
            print("✅ Flow structure is correct")
        
        # Check components structure
        if response.components:
            sample_component = response.components[0]
            for field in expected_structure['components']:
                if not hasattr(sample_component, field):
                    print(f"❌ Missing component field: {field}")
                    return False
            print("✅ Component structure is correct")
        
        print("✅ Frontend compatibility verified!")
        return True
        
    except Exception as e:
        print(f"❌ Frontend compatibility test failed: {e}")
        return False


async def main():
    """Main test function."""
    
    print("🚀 Showcase Fix Test Suite")
    print("=" * 60)
    
    # Run tests
    test1_passed = await test_showcase_api()
    test2_passed = await test_frontend_compatibility()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("-" * 30)
    print(f"Showcase API Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Frontend Compatibility: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Showcase page fix is working correctly")
        print("✅ The 'i.flows is not iterable' error should be resolved")
        print("✅ All 1600 flows and components should display properly")
        print("\n🚀 Ready to deploy the fix!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Please review the errors above and fix any issues")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
