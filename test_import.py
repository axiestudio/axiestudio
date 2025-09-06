#!/usr/bin/env python3
"""
Quick test to verify timezone import works in master branch (Swedish app).
"""

import sys
import os

# Add the backend path to sys.path so we can import our modules
backend_path = os.path.join(os.path.dirname(__file__), 'src', 'backend', 'base')
sys.path.insert(0, backend_path)

try:
    from axiestudio.utils.timezone import ensure_timezone_aware, safe_datetime_comparison, get_utc_now
    print("✅ SUCCESS: Timezone utilities imported successfully in master branch (Swedish app)")
    
    # Test basic functionality
    from datetime import datetime
    naive_dt = datetime(2025, 1, 15, 12, 0, 0)
    aware_dt = ensure_timezone_aware(naive_dt)
    print(f"✅ SUCCESS: Timezone conversion works: {naive_dt} -> {aware_dt}")
    
except ImportError as e:
    print(f"❌ FAILED: Import error in master branch: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ FAILED: Unexpected error: {e}")
    sys.exit(1)

print("🎉 Master branch (Swedish app) timezone utilities are working correctly!")
