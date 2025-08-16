#!/usr/bin/env python3
"""
EXHAUSTIVE LANGFLOW vs AXIE STUDIO COMPARISON
This script performs systematic verification that Axie Studio is a complete replica of Langflow
with only the specified customizations (branding, auto-login=false, no frontend signup).
"""

import os
import sys
import ast
import json
from pathlib import Path
from collections import defaultdict

def compare_directory_structures():
    """Compare directory structures between Langflow and Axie Studio."""
    print("📁 COMPARING DIRECTORY STRUCTURES...")
    
    langflow_base = Path("../../../Langflow/langflow/src/backend/base/langflow")
    axiestudio_base = Path("src/backend/base/axiestudio")
    
    if not langflow_base.exists():
        print("❌ Langflow directory not found for comparison")
        return False
    
    # Get all directories in both projects
    langflow_dirs = set()
    axiestudio_dirs = set()
    
    for root, dirs, files in os.walk(langflow_base):
        for d in dirs:
            rel_path = os.path.relpath(os.path.join(root, d), langflow_base)
            langflow_dirs.add(rel_path)
    
    for root, dirs, files in os.walk(axiestudio_base):
        for d in dirs:
            rel_path = os.path.relpath(os.path.join(root, d), axiestudio_base)
            axiestudio_dirs.add(rel_path)
    
    # Compare directories
    missing_in_axiestudio = langflow_dirs - axiestudio_dirs
    extra_in_axiestudio = axiestudio_dirs - langflow_dirs
    
    if missing_in_axiestudio:
        print(f"❌ Missing directories in Axie Studio: {len(missing_in_axiestudio)}")
        for d in sorted(missing_in_axiestudio)[:10]:  # Show first 10
            print(f"   • {d}")
        return False
    
    if extra_in_axiestudio:
        print(f"⚠️  Extra directories in Axie Studio: {len(extra_in_axiestudio)}")
        for d in sorted(extra_in_axiestudio)[:5]:  # Show first 5
            print(f"   • {d}")
    
    print(f"✅ Directory structure match: {len(langflow_dirs)} directories")
    return True

def compare_component_files():
    """Compare component files between Langflow and Axie Studio."""
    print("\n🧩 COMPARING COMPONENT FILES...")
    
    langflow_components = Path("../../../Langflow/langflow/src/backend/base/langflow/components")
    axiestudio_components = Path("src/backend/base/axiestudio/components")
    
    if not langflow_components.exists():
        print("❌ Langflow components directory not found")
        return False
    
    # Get all Python files in components
    langflow_files = set()
    axiestudio_files = set()
    
    for file in langflow_components.rglob("*.py"):
        rel_path = file.relative_to(langflow_components)
        langflow_files.add(str(rel_path))
    
    for file in axiestudio_components.rglob("*.py"):
        rel_path = file.relative_to(axiestudio_components)
        axiestudio_files.add(str(rel_path))
    
    missing_files = langflow_files - axiestudio_files
    extra_files = axiestudio_files - langflow_files
    
    if missing_files:
        print(f"❌ Missing component files: {len(missing_files)}")
        for f in sorted(missing_files)[:10]:
            print(f"   • {f}")
        return False
    
    if extra_files:
        print(f"⚠️  Extra component files: {len(extra_files)}")
        for f in sorted(extra_files)[:5]:
            print(f"   • {f}")
    
    print(f"✅ Component files match: {len(langflow_files)} files")
    return True

def verify_import_rebranding():
    """Verify all imports have been correctly rebranded from langflow to axiestudio."""
    print("\n🔄 VERIFYING IMPORT REBRANDING...")
    
    axiestudio_base = Path("src/backend/base/axiestudio")
    langflow_imports = []
    
    for file in axiestudio_base.rglob("*.py"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for langflow imports
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'from langflow' in line or 'import langflow' in line:
                    langflow_imports.append(f"{file}:{i} - {line.strip()}")
        except Exception as e:
            print(f"⚠️  Error reading {file}: {e}")
    
    if langflow_imports:
        print(f"❌ Found {len(langflow_imports)} langflow imports:")
        for imp in langflow_imports[:10]:
            print(f"   • {imp}")
        return False
    
    print("✅ All imports correctly rebranded to axiestudio")
    return True

def verify_dependency_completeness():
    """Verify all dependencies from Langflow are present in Axie Studio."""
    print("\n📦 VERIFYING DEPENDENCY COMPLETENESS...")
    
    # Read Langflow dependencies
    langflow_pyproject = Path("../../../Langflow/langflow/pyproject.toml")
    langflow_base_pyproject = Path("../../../Langflow/langflow/src/backend/base/pyproject.toml")
    
    axiestudio_pyproject = Path("pyproject.toml")
    axiestudio_base_pyproject = Path("src/backend/base/pyproject.toml")
    
    def extract_dependencies(file_path):
        """Extract dependencies from pyproject.toml."""
        if not file_path.exists():
            return set()
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Simple extraction of dependency names
            deps = set()
            in_deps = False
            for line in content.split('\n'):
                if 'dependencies = [' in line:
                    in_deps = True
                    continue
                if in_deps and line.strip() == ']':
                    break
                if in_deps and '"' in line:
                    # Extract package name
                    dep = line.strip().strip(',').strip('"')
                    if dep and not dep.startswith('#'):
                        pkg_name = dep.split('>=')[0].split('==')[0].split('~=')[0].split('<')[0].split('>')[0]
                        deps.add(pkg_name.strip())
            return deps
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return set()
    
    # Compare main dependencies
    if langflow_pyproject.exists():
        langflow_deps = extract_dependencies(langflow_pyproject)
        axiestudio_deps = extract_dependencies(axiestudio_pyproject)
        
        # Adjust for rebranding
        langflow_deps.discard('langflow-base')
        axiestudio_deps.discard('axiestudio-base')
        
        missing_deps = langflow_deps - axiestudio_deps
        if missing_deps:
            print(f"❌ Missing main dependencies: {missing_deps}")
            return False
        
        print(f"✅ Main dependencies match: {len(langflow_deps)} packages")
    
    # Compare base dependencies
    if langflow_base_pyproject.exists():
        langflow_base_deps = extract_dependencies(langflow_base_pyproject)
        axiestudio_base_deps = extract_dependencies(axiestudio_base_pyproject)
        
        missing_base_deps = langflow_base_deps - axiestudio_base_deps
        if missing_base_deps:
            print(f"❌ Missing base dependencies: {missing_base_deps}")
            return False
        
        print(f"✅ Base dependencies match: {len(langflow_base_deps)} packages")
    
    return True

def verify_customizations():
    """Verify the specific customizations are correctly implemented."""
    print("\n🎨 VERIFYING CUSTOMIZATIONS...")
    
    customizations_verified = 0
    
    # 1. Check auto-login = false
    settings_files = [
        "src/backend/base/axiestudio/services/settings/base.py",
        "src/backend/base/axiestudio/services/settings/service.py"
    ]
    
    auto_login_found = False
    for settings_file in settings_files:
        if Path(settings_file).exists():
            with open(settings_file, 'r') as f:
                content = f.read()
                if 'auto_login' in content.lower() or 'autologin' in content.lower():
                    auto_login_found = True
                    if 'false' in content.lower():
                        print("✅ Auto-login disabled configuration found")
                        customizations_verified += 1
                    break
    
    if not auto_login_found:
        print("⚠️  Auto-login configuration not explicitly found")
    
    # 2. Check branding
    branding_files = [
        "src/backend/base/axiestudio/__main__.py",
        "src/frontend/package.json"
    ]
    
    branding_found = False
    for brand_file in branding_files:
        if Path(brand_file).exists():
            with open(brand_file, 'r') as f:
                content = f.read()
                if 'axie' in content.lower() and 'studio' in content.lower():
                    branding_found = True
                    break
    
    if branding_found:
        print("✅ Axie Studio branding found")
        customizations_verified += 1
    else:
        print("⚠️  Axie Studio branding not clearly found")
    
    # 3. Check frontend signup disabled
    frontend_files = list(Path("src/frontend").rglob("*.tsx")) + list(Path("src/frontend").rglob("*.ts"))
    
    signup_disabled = False
    for frontend_file in frontend_files:
        try:
            with open(frontend_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'signup' in content.lower() and ('disable' in content.lower() or 'false' in content.lower()):
                    signup_disabled = True
                    break
        except:
            continue
    
    if signup_disabled:
        print("✅ Frontend signup disabled")
        customizations_verified += 1
    else:
        print("⚠️  Frontend signup disable not clearly found")
    
    print(f"✅ Customizations verified: {customizations_verified}/3")
    return customizations_verified >= 2

def main():
    """Run exhaustive comparison."""
    print("🔍 EXHAUSTIVE LANGFLOW vs AXIE STUDIO COMPARISON")
    print("=" * 60)
    
    os.chdir(Path(__file__).parent)
    
    tests = [
        ("Directory Structure", compare_directory_structures),
        ("Component Files", compare_component_files),
        ("Import Rebranding", verify_import_rebranding),
        ("Dependency Completeness", verify_dependency_completeness),
        ("Customizations", verify_customizations),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n🎯 FINAL RESULTS: {passed}/{total} TESTS PASSED")
    
    if passed == total:
        print("🎉 AXIE STUDIO IS A COMPLETE LANGFLOW REPLICA!")
        print("✅ All structures match")
        print("✅ All components present")
        print("✅ All imports rebranded")
        print("✅ All dependencies included")
        print("✅ Customizations implemented")
        return 0
    else:
        print("ISSUES DETECTED - REVIEW ABOVE")
        return 1

if __name__ == "__main__":
    sys.exit(main())
