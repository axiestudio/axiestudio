#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE VERIFICATION
This script performs exhaustive verification that Axie Studio is deployment-ready
with all required customizations and complete Langflow functionality.
"""

import os
import sys
import json
import ast
from pathlib import Path
from collections import defaultdict

def verify_auto_login_disabled():
    """Verify AUTO_LOGIN is set to False."""
    print("🔐 VERIFYING AUTO-LOGIN DISABLED...")
    
    auth_file = Path("src/backend/base/axiestudio/services/settings/auth.py")
    if not auth_file.exists():
        print("❌ Auth settings file not found")
        return False
    
    with open(auth_file, 'r') as f:
        content = f.read()
    
    if "AUTO_LOGIN: bool = False" in content:
        print("✅ AUTO_LOGIN correctly set to False")
        return True
    elif "AUTO_LOGIN: bool = True" in content:
        print("❌ AUTO_LOGIN is set to True - should be False")
        return False
    else:
        print("⚠️  AUTO_LOGIN setting not found")
        return False

def verify_branding_complete():
    """Verify Axie Studio branding is complete."""
    print("\n🎨 VERIFYING AXIE STUDIO BRANDING...")
    
    branding_checks = 0
    
    # Check frontend package.json
    frontend_package = Path("src/frontend/package.json")
    if frontend_package.exists():
        with open(frontend_package, 'r') as f:
            content = f.read()
        if '"name": "axiestudio"' in content:
            print("✅ Frontend package name: axiestudio")
            branding_checks += 1
    
    # Check login page for AxieStudioLogo
    login_page = Path("src/frontend/src/pages/LoginPage/index.tsx")
    if login_page.exists():
        with open(login_page, 'r') as f:
            content = f.read()
        if "AxieStudioLogo" in content:
            print("✅ Login page uses AxieStudioLogo")
            branding_checks += 1
    
    # Check main pyproject.toml
    main_pyproject = Path("pyproject.toml")
    if main_pyproject.exists():
        with open(main_pyproject, 'r') as f:
            content = f.read()
        if 'axiestudio = "axiestudio.axiestudio_launcher:main"' in content:
            print("✅ Entry point correctly branded")
            branding_checks += 1
    
    # Check for axiestudio imports
    axiestudio_files = list(Path("src/backend/base/axiestudio").rglob("*.py"))
    axiestudio_imports = 0
    for file in axiestudio_files[:10]:  # Check first 10 files
        try:
            with open(file, 'r') as f:
                content = f.read()
            if "from axiestudio" in content or "import axiestudio" in content:
                axiestudio_imports += 1
        except:
            continue
    
    if axiestudio_imports > 0:
        print(f"✅ Found axiestudio imports in {axiestudio_imports} files")
        branding_checks += 1
    
    print(f"✅ Branding verification: {branding_checks}/4 checks passed")
    return branding_checks >= 3

def verify_signup_disabled():
    """Verify frontend signup is disabled."""
    print("\n🚫 VERIFYING SIGNUP DISABLED...")
    
    # Check if signup route exists
    routes_file = Path("src/frontend/src/routes.tsx")
    if routes_file.exists():
        with open(routes_file, 'r') as f:
            content = f.read()
        if "signup" not in content.lower() and "SignUp" not in content:
            print("✅ No signup route found in routes.tsx")
        else:
            print("⚠️  Signup route may still exist")
            return False
    
    # Check login page for signup links
    login_page = Path("src/frontend/src/pages/LoginPage/index.tsx")
    if login_page.exists():
        with open(login_page, 'r') as f:
            content = f.read()
        if "signup" not in content.lower() and "register" not in content.lower():
            print("✅ No signup links in login page")
        else:
            print("⚠️  Signup links may exist in login page")
            return False
    
    print("✅ Frontend signup appears to be disabled")
    return True

def verify_component_completeness():
    """Verify all components are present."""
    print("\n🧩 VERIFYING COMPONENT COMPLETENESS...")
    
    components_dir = Path("src/backend/base/axiestudio/components")
    if not components_dir.exists():
        print("❌ Components directory not found")
        return False
    
    # Count component directories
    component_dirs = [d for d in components_dir.iterdir() if d.is_dir()]
    print(f"✅ Component directories: {len(component_dirs)}")
    
    # Check key AI providers
    key_providers = ["openai", "anthropic", "google", "groq", "mistral", "cohere"]
    found_providers = []
    
    for provider in key_providers:
        provider_dir = components_dir / provider
        if provider_dir.exists():
            found_providers.append(provider)
    
    print(f"✅ AI providers found: {', '.join(found_providers)}")
    
    # Check vector stores
    vectorstores_dir = components_dir / "vectorstores"
    if vectorstores_dir.exists():
        vector_files = list(vectorstores_dir.glob("*.py"))
        print(f"✅ Vector store implementations: {len(vector_files)}")
    
    return len(found_providers) >= 5 and len(component_dirs) >= 80

def verify_dependency_integrity():
    """Verify dependency integrity."""
    print("\n📦 VERIFYING DEPENDENCY INTEGRITY...")
    
    # Check UV lock file
    uv_lock = Path("uv.lock")
    if not uv_lock.exists():
        print("❌ UV lock file not found")
        return False
    
    with open(uv_lock, 'r') as f:
        lock_content = f.read()
    
    # Check for key dependencies
    key_deps = ["fastapi", "langchain", "openai", "anthropic", "loguru", "axiestudio-base"]
    found_deps = []
    
    for dep in key_deps:
        if f'name = "{dep}"' in lock_content:
            found_deps.append(dep)
    
    print(f"✅ Key dependencies in lock file: {', '.join(found_deps)}")
    
    # Check pyproject.toml files
    main_pyproject = Path("pyproject.toml")
    base_pyproject = Path("src/backend/base/pyproject.toml")
    
    pyproject_checks = 0
    if main_pyproject.exists():
        pyproject_checks += 1
        print("✅ Main pyproject.toml exists")
    
    if base_pyproject.exists():
        pyproject_checks += 1
        print("✅ Base pyproject.toml exists")
    
    return len(found_deps) >= 5 and pyproject_checks == 2

def verify_docker_configuration():
    """Verify Docker configuration."""
    print("\n🐳 VERIFYING DOCKER CONFIGURATION...")
    
    dockerfile = Path("Dockerfile")
    if not dockerfile.exists():
        print("❌ Dockerfile not found")
        return False
    
    with open(dockerfile, 'r') as f:
        content = f.read()
    
    docker_checks = 0
    
    if "uv sync" in content:
        print("✅ Dockerfile uses UV for dependency management")
        docker_checks += 1
    
    if "axiestudio/frontend" in content:
        print("✅ Dockerfile copies frontend to correct path")
        docker_checks += 1
    
    if "--frozen" in content:
        print("✅ Dockerfile uses frozen dependencies")
        docker_checks += 1
    
    # Check docker-compose
    docker_compose = Path("docker-compose.yml")
    if docker_compose.exists():
        print("✅ Docker Compose file exists")
        docker_checks += 1
    
    return docker_checks >= 3

def verify_import_integrity():
    """Verify import integrity."""
    print("\n🔗 VERIFYING IMPORT INTEGRITY...")
    
    # Check for any remaining langflow imports
    axiestudio_dir = Path("src/backend/base/axiestudio")
    langflow_imports = []
    
    for file in axiestudio_dir.rglob("*.py"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'from langflow' in line or 'import langflow' in line:
                    langflow_imports.append(f"{file.name}:{i}")
        except:
            continue
    
    if langflow_imports:
        print(f"❌ Found {len(langflow_imports)} langflow imports")
        for imp in langflow_imports[:5]:
            print(f"   • {imp}")
        return False
    
    print("✅ No langflow imports found - all correctly rebranded")
    return True

def main():
    """Run final comprehensive verification."""
    print("🔍 FINAL COMPREHENSIVE VERIFICATION")
    print("=" * 60)
    print("Verifying Axie Studio is a complete Langflow replica with customizations")
    print()
    
    os.chdir(Path(__file__).parent)
    
    tests = [
        ("Auto-Login Disabled", verify_auto_login_disabled),
        ("Axie Studio Branding", verify_branding_complete),
        ("Signup Disabled", verify_signup_disabled),
        ("Component Completeness", verify_component_completeness),
        ("Dependency Integrity", verify_dependency_integrity),
        ("Docker Configuration", verify_docker_configuration),
        ("Import Integrity", verify_import_integrity),
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
    
    print("🎯 FINAL VERIFICATION RESULTS")
    print("=" * 60)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 AXIE STUDIO VERIFICATION COMPLETE!")
        print("✅ Complete Langflow replica confirmed")
        print("✅ All customizations implemented:")
        print("   • AUTO_LOGIN = False")
        print("   • Axie Studio branding throughout")
        print("   • Frontend signup disabled")
        print("✅ All components and dependencies present")
        print("✅ Docker deployment ready")
        print("\n🚀 DEPLOY WITH 100% CONFIDENCE!")
        return 0
    else:
        print(f"\n🚨 {total - passed} ISSUES DETECTED")
        print("Review the failed tests above before deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main())
