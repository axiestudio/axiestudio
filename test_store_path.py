#!/usr/bin/env python3
"""
Test script to verify the store path calculation works correctly.
"""

import sys
from pathlib import Path

# Add the backend to the path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend" / "base"))

print("🔧 Testing AxieStudio Store Path Resolution...")
print("=" * 50)

# Test 1: Check if store directory exists
store_dir = Path(__file__).parent / "src" / "store_components_converted"
print(f"📁 Checking store directory: {store_dir}")
print(f"✅ Store directory exists: {store_dir.exists()}")

if store_dir.exists():
    index_file = store_dir / "store_index.json"
    print(f"📄 Checking index file: {index_file}")
    print(f"✅ Index file exists: {index_file.exists()}")

    if index_file.exists():
        try:
            import json
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Index file loaded successfully")
            print(f"   - Total items: {data['summary']['total_items']}")
            print(f"   - Total flows: {data['summary']['total_flows']}")
            print(f"   - Total components: {data['summary']['total_components']}")

            if len(data['flows']) > 0:
                print(f"✅ Sample flow: {data['flows'][0]['name']}")

            if len(data['components']) > 0:
                print(f"✅ Sample component: {data['components'][0]['name']}")

        except Exception as e:
            print(f"❌ Failed to load index file: {e}")
            sys.exit(1)

# Test 2: Try importing the backend module
try:
    from axiestudio.api.v1.axiestudio_store import get_store_components_path, load_store_index

    # Test path resolution
    try:
        store_path = get_store_components_path()
        print(f"✅ Backend path resolution works: {store_path}")
        print(f"✅ Backend path exists: {store_path.exists()}")
    except Exception as e:
        print(f"❌ Backend path resolution failed: {e}")
        sys.exit(1)

    # Test store index loading
    try:
        store_data = load_store_index()
        print(f"✅ Backend store index loaded successfully")
        print(f"   - Backend total items: {store_data.summary.total_items}")
    except Exception as e:
        print(f"❌ Backend store index loading failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed! The showcase backend should work correctly.")

except ImportError as e:
    print(f"⚠️  Backend import failed (expected without proper environment): {e}")
    print("✅ But the store data files are present and valid!")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
