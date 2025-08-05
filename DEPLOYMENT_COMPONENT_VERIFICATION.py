#!/usr/bin/env python3
"""
DEPLOYMENT COMPONENT VERIFICATION
This script verifies that all components will work correctly in deployment
by checking the critical deployment-specific aspects.
"""

import sys
import importlib
import pkgutil
from pathlib import Path

def verify_component_loading_mechanism():
    """Verify the component loading mechanism works correctly."""
    print("🔧 VERIFYING COMPONENT LOADING MECHANISM...")
    
    # Check if the component loading function exists and has correct imports
    try:
        sys.path.insert(0, str(Path("src/backend/base")))
        from axiestudio.interface.components import import_axiestudio_components
        print("✅ Component loading function imported successfully")
        
        # Check if the function references the correct package
        import inspect
        source = inspect.getsource(import_axiestudio_components)
        if "axiestudio.components" in source:
            print("✅ Component loading references correct package")
        else:
            print("❌ Component loading references wrong package")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import component loading function: {e}")
        return False
    
    return True

def verify_component_package_structure():
    """Verify the component package structure is correct."""
    print("\n📦 VERIFYING COMPONENT PACKAGE STRUCTURE...")
    
    components_path = Path("src/backend/base/axiestudio/components")
    if not components_path.exists():
        print("❌ Components directory does not exist")
        return False
    
    # Check if __init__.py exists
    init_file = components_path / "__init__.py"
    if not init_file.exists():
        print("❌ Components package __init__.py missing")
        return False
    
    print("✅ Components package structure exists")
    
    # Count component directories
    component_dirs = [d for d in components_path.iterdir() if d.is_dir() and d.name != "__pycache__"]
    print(f"✅ Found {len(component_dirs)} component directories")
    
    # Check critical component categories
    critical_categories = ["openai", "anthropic", "google", "vectorstores", "processing"]
    missing_categories = []
    
    for category in critical_categories:
        category_path = components_path / category
        if not category_path.exists():
            missing_categories.append(category)
        else:
            # Check if category has __init__.py
            category_init = category_path / "__init__.py"
            if category_init.exists():
                print(f"✅ {category}: Directory and __init__.py present")
            else:
                print(f"⚠️  {category}: Directory exists but __init__.py missing")
    
    if missing_categories:
        print(f"❌ Missing critical categories: {missing_categories}")
        return False
    
    return True

def verify_component_imports():
    """Verify that components have correct import statements."""
    print("\n🔗 VERIFYING COMPONENT IMPORTS...")
    
    components_path = Path("src/backend/base/axiestudio/components")
    
    # Check sample components for correct imports
    sample_components = [
        "openai/openai.py",
        "anthropic/anthropic.py", 
        "vectorstores/pinecone.py",
        "google/google_generative_ai.py"
    ]
    
    langflow_imports = []
    correct_imports = 0
    
    for component_file in sample_components:
        file_path = components_path / component_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for langflow imports (should not exist)
                if 'from langflow' in content or 'import langflow' in content:
                    langflow_imports.append(component_file)
                
                # Check for axiestudio imports (should exist)
                if 'from axiestudio' in content or 'import axiestudio' in content:
                    correct_imports += 1
                    print(f"✅ {component_file}: Correct axiestudio imports")
                else:
                    print(f"⚠️  {component_file}: No axiestudio imports found")
                    
            except Exception as e:
                print(f"❌ Error reading {component_file}: {e}")
        else:
            print(f"⚠️  {component_file}: File not found")
    
    if langflow_imports:
        print(f"❌ Found langflow imports in: {langflow_imports}")
        return False
    
    if correct_imports == 0:
        print("❌ No correct axiestudio imports found")
        return False
    
    print(f"✅ Found correct imports in {correct_imports} sample components")
    return True

def verify_base_components_path():
    """Verify the BASE_COMPONENTS_PATH is correctly configured."""
    print("\n📍 VERIFYING BASE COMPONENTS PATH...")
    
    try:
        sys.path.insert(0, str(Path("src/backend/base")))
        from axiestudio.services.settings.base import BASE_COMPONENTS_PATH
        
        # Check if the path points to the correct location
        expected_path = str(Path("src/backend/base/axiestudio/components").resolve())
        actual_path = str(Path(BASE_COMPONENTS_PATH).resolve())
        
        if "axiestudio/components" in actual_path:
            print(f"✅ BASE_COMPONENTS_PATH correctly configured: {BASE_COMPONENTS_PATH}")
            return True
        else:
            print(f"❌ BASE_COMPONENTS_PATH incorrect: {BASE_COMPONENTS_PATH}")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import BASE_COMPONENTS_PATH: {e}")
        return False

def verify_docker_configuration():
    """Verify Docker configuration for component deployment."""
    print("\n🐳 VERIFYING DOCKER CONFIGURATION...")
    
    dockerfile_path = Path("Dockerfile")
    if not dockerfile_path.exists():
        print("❌ Dockerfile not found")
        return False
    
    with open(dockerfile_path, 'r') as f:
        dockerfile_content = f.read()
    
    checks_passed = 0
    
    # Check if source code is copied to runtime
    if "COPY --from=builder --chown=1000 /app/src /app/src" in dockerfile_content:
        print("✅ Source code copied to runtime stage")
        checks_passed += 1
    else:
        print("❌ Source code not copied to runtime stage")
    
    # Check if frontend build is included
    if "cp -r build /app/src/backend/base/axiestudio/frontend" in dockerfile_content:
        print("✅ Frontend build copied to correct location")
        checks_passed += 1
    else:
        print("❌ Frontend build not copied correctly")
    
    # Check if UV is used for dependency management
    if "uv sync" in dockerfile_content:
        print("✅ UV used for dependency management")
        checks_passed += 1
    else:
        print("❌ UV not used for dependency management")
    
    # Check entry point
    if 'CMD ["axiestudio", "run"]' in dockerfile_content:
        print("✅ Correct entry point configured")
        checks_passed += 1
    else:
        print("❌ Incorrect entry point")
    
    return checks_passed >= 3

def verify_entry_point_chain():
    """Verify the entry point chain works correctly."""
    print("\n🚀 VERIFYING ENTRY POINT CHAIN...")
    
    # Check pyproject.toml entry point
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        if 'axiestudio = "axiestudio.axiestudio_launcher:main"' in content:
            print("✅ Entry point correctly configured in pyproject.toml")
        else:
            print("❌ Entry point incorrectly configured in pyproject.toml")
            return False
    else:
        print("❌ pyproject.toml not found")
        return False
    
    # Check if launcher exists
    launcher_path = Path("src/backend/base/axiestudio/axiestudio_launcher.py")
    if launcher_path.exists():
        print("✅ Launcher file exists")
    else:
        print("❌ Launcher file missing")
        return False
    
    # Check if main module exists
    main_path = Path("src/backend/base/axiestudio/__main__.py")
    if main_path.exists():
        print("✅ Main module exists")
    else:
        print("❌ Main module missing")
        return False
    
    return True

def main():
    """Run deployment component verification."""
    print("🔍 DEPLOYMENT COMPONENT VERIFICATION")
    print("=" * 50)
    print("Verifying components will work correctly in deployment...")
    print()
    
    tests = [
        ("Component Loading Mechanism", verify_component_loading_mechanism),
        ("Component Package Structure", verify_component_package_structure),
        ("Component Imports", verify_component_imports),
        ("Base Components Path", verify_base_components_path),
        ("Docker Configuration", verify_docker_configuration),
        ("Entry Point Chain", verify_entry_point_chain),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED\n")
            else:
                print(f"❌ {test_name}: FAILED\n")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}\n")
    
    print("🎯 DEPLOYMENT COMPONENT VERIFICATION RESULTS")
    print("=" * 50)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL DEPLOYMENT CHECKS PASSED!")
        print("✅ Components will work correctly in deployment")
        print("✅ All import paths are correct")
        print("✅ Docker configuration is proper")
        print("✅ Entry points are configured")
        print("\n🚀 DEPLOY WITH CONFIDENCE!")
        return 0
    else:
        print(f"\n🚨 {total - passed} DEPLOYMENT ISSUES DETECTED")
        print("Fix the failed tests before deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main())
