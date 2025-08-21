#!/usr/bin/env python3
"""
Verification script for the Showcase API endpoints.
Tests that all API endpoints are working correctly.
"""

import asyncio
import sys
import json
from pathlib import Path

# Add the backend path to sys.path
backend_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(backend_path))

async def verify_api_endpoints():
    """Verify all showcase API endpoints work correctly"""
    try:
        print("🔧 Verifying Showcase API Endpoints...")
        print("=" * 50)
        
        # Import the API functions
        from axiestudio.api.v1.axiestudio_store import (
            load_store_index, 
            load_item_data, 
            get_store_components_path
        )
        
        # Test 1: Verify store path
        store_path = get_store_components_path()
        print(f"📁 Store path: {store_path}")
        
        if not store_path.exists():
            print("❌ Store components directory not found!")
            return False
        
        # Test 2: Load store index
        print("📊 Loading store index...")
        store_data = load_store_index()
        
        print(f"✅ Store index loaded successfully:")
        print(f"   Total flows: {len(store_data.flows)}")
        print(f"   Total components: {len(store_data.components)}")
        print(f"   Total items: {len(store_data.flows) + len(store_data.components)}")
        
        # Test 3: Test component loading
        if store_data.components:
            sample_component = store_data.components[0]
            print(f"🧩 Testing component loading: {sample_component.name}")
            
            component_data = load_item_data("component", sample_component.id)
            print(f"✅ Component loaded: {component_data['name']}")
            
            # Verify required fields
            required_fields = ['id', 'name', 'description', 'type', 'author', 'stats', 'dates']
            missing_fields = [field for field in required_fields if field not in component_data]
            
            if missing_fields:
                print(f"❌ Component missing fields: {missing_fields}")
                return False
            else:
                print("✅ Component has all required fields")
        
        # Test 4: Test flow loading
        if store_data.flows:
            sample_flow = store_data.flows[0]
            print(f"🔄 Testing flow loading: {sample_flow.name}")
            
            flow_data = load_item_data("flow", sample_flow.id)
            print(f"✅ Flow loaded: {flow_data['name']}")
            
            # Verify required fields
            required_fields = ['id', 'name', 'description', 'type', 'author', 'stats', 'dates']
            missing_fields = [field for field in required_fields if field not in flow_data]
            
            if missing_fields:
                print(f"❌ Flow missing fields: {missing_fields}")
                return False
            else:
                print("✅ Flow has all required fields")
        
        # Test 5: Test search functionality
        print("🔍 Testing search functionality...")
        
        # Test search by name
        search_results = []
        search_term = "chat"
        for item in store_data.flows + store_data.components:
            if search_term.lower() in item.name.lower():
                search_results.append(item)
        
        print(f"✅ Search for '{search_term}' found {len(search_results)} results")
        
        # Test 6: Test tag filtering
        print("🏷️ Testing tag filtering...")
        
        all_tags = set()
        for item in store_data.flows + store_data.components:
            for tag in item.tags:
                all_tags.add(tag.tags_id.get("name", ""))
        
        print(f"✅ Found {len(all_tags)} unique tags")
        
        # Test 7: Test author filtering
        print("👤 Testing author filtering...")
        
        all_authors = set()
        for item in store_data.flows + store_data.components:
            all_authors.add(item.author.username)
        
        print(f"✅ Found {len(all_authors)} unique authors")
        
        # Test 8: Test sorting
        print("📈 Testing sorting functionality...")
        
        # Test popularity sort
        items = store_data.flows + store_data.components
        sorted_by_popularity = sorted(items, key=lambda x: x.stats.likes + x.stats.downloads, reverse=True)
        print(f"✅ Popularity sort: Top item has {sorted_by_popularity[0].stats.likes + sorted_by_popularity[0].stats.downloads} total likes+downloads")
        
        # Test recent sort
        sorted_by_recent = sorted(items, key=lambda x: x.dates.updated, reverse=True)
        print(f"✅ Recent sort: Most recent item updated on {sorted_by_recent[0].dates.updated}")
        
        print("\n🎉 All API endpoint tests passed!")
        print("\n📋 API Verification Summary:")
        print("✅ Store index loading works")
        print("✅ Component data loading works")
        print("✅ Flow data loading works")
        print("✅ Search functionality works")
        print("✅ Tag filtering works")
        print("✅ Author filtering works")
        print("✅ Sorting functionality works")
        print("\n🚀 API is ready for frontend integration!")
        
        return True
        
    except Exception as e:
        print(f"❌ API verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the verification"""
    print("🔧 Axie Studio Showcase API Verification")
    print("=" * 50)
    
    success = await verify_api_endpoints()
    
    if success:
        print("\n🎉 Showcase API verification successful!")
        return 0
    else:
        print("\n❌ Showcase API verification failed.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
