#!/usr/bin/env python3
"""Test script to verify AXX rebranding was successful."""

import sys
import os
from pathlib import Path

# Add the AXX source directory to Python path
axx_src = Path("C:/Users/mist24lk/Downloads/aaa/axiestudio/axx/src")
sys.path.insert(0, str(axx_src))

def test_basic_imports():
    """Test that basic AXX imports work."""
    print("🧪 Testing basic AXX imports...")
    
    try:
        # Test main module import
        import axx
        print("✅ Successfully imported 'axx' module")
        
        # Test CLI import
        from axx.cli import serve_command
        print("✅ Successfully imported 'axx.cli.serve_command'")
        
        # Test main entry point
        from axx.__main__ import main
        print("✅ Successfully imported 'axx.__main__.main'")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_component_imports():
    """Test that component imports work."""
    print("\n🧪 Testing AXX component imports...")
    
    try:
        # Test components module
        import axx.components
        print("✅ Successfully imported 'axx.components'")
        
        # Test flattened component access
        from axx import components as cp
        print("✅ Successfully imported flattened components as 'cp'")
        
        return True
        
    except ImportError as e:
        print(f"❌ Component import failed: {e}")
        return False

def check_no_lfx_references():
    """Check that no LFX references remain in key files."""
    print("\n🔍 Checking for remaining LFX references...")
    
    key_files = [
        "axx/src/axx/__main__.py",
        "axx/src/axx/cli/commands.py", 
        "axx/src/axx/components/__init__.py",
        "axx/pyproject.toml",
        "axx/README.md"
    ]
    
    base_path = Path("C:/Users/mist24lk/Downloads/aaa/axiestudio")
    issues_found = 0
    
    for file_path in key_files:
        full_path = base_path / file_path
        if full_path.exists():
            try:
                content = full_path.read_text(encoding='utf-8')
                if 'from lfx' in content or 'import lfx' in content:
                    print(f"⚠️  Found LFX reference in: {file_path}")
                    issues_found += 1
                else:
                    print(f"✅ Clean: {file_path}")
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    if issues_found == 0:
        print("🎉 No LFX references found in key files!")
    else:
        print(f"⚠️  Found {issues_found} files with LFX references")
    
    return issues_found == 0

def main():
    """Run all tests."""
    print("🚀 AXX Rebranding Verification Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test basic imports (will fail due to missing dependencies, but structure should be correct)
    try:
        all_passed &= test_basic_imports()
    except Exception as e:
        print(f"❌ Basic import test failed with exception: {e}")
        all_passed = False
    
    # Test component imports
    try:
        all_passed &= test_component_imports()
    except Exception as e:
        print(f"❌ Component import test failed with exception: {e}")
        all_passed = False
    
    # Check for remaining LFX references
    all_passed &= check_no_lfx_references()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! AXX rebranding appears successful!")
    else:
        print("⚠️  Some tests failed. Review the output above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
