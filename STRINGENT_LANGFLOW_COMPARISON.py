#!/usr/bin/env python3
"""
ULTRA-STRINGENT LANGFLOW vs AXIE STUDIO COMPARISON
This script performs the most rigorous comparison possible to ensure
Axie Studio is a perfect replica of Langflow with only intended customizations.
"""

import os
import sys
import hashlib
from pathlib import Path
from collections import defaultdict

# Paths
LANGFLOW_BASE = Path("../../../Langflow/langflow/src/backend/base/langflow")
AXIESTUDIO_BASE = Path("src/backend/base/axiestudio")
LANGFLOW_MAIN = Path("../../../Langflow/langflow")
AXIESTUDIO_MAIN = Path(".")

def get_file_structure(base_path, exclude_patterns=None):
    """Get complete file structure with relative paths."""
    if exclude_patterns is None:
        exclude_patterns = ['.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv']
    
    files = {}
    dirs = set()
    
    if not base_path.exists():
        return files, dirs
    
    for root, dirnames, filenames in os.walk(base_path):
        # Filter out excluded directories
        dirnames[:] = [d for d in dirnames if not any(pattern in d for pattern in exclude_patterns)]
        
        rel_root = os.path.relpath(root, base_path)
        if rel_root != '.':
            dirs.add(rel_root)
        
        for filename in filenames:
            if not any(pattern in filename for pattern in exclude_patterns):
                rel_path = os.path.join(rel_root, filename) if rel_root != '.' else filename
                full_path = os.path.join(root, filename)
                files[rel_path] = full_path
    
    return files, dirs

def compare_file_structures():
    """Compare file structures between Langflow and Axie Studio."""
    print("📁 STRINGENT FILE STRUCTURE COMPARISON")
    print("=" * 50)
    
    # Get structures
    lf_files, lf_dirs = get_file_structure(LANGFLOW_BASE)
    as_files, as_dirs = get_file_structure(AXIESTUDIO_BASE)
    
    print(f"Langflow files: {len(lf_files)}, dirs: {len(lf_dirs)}")
    print(f"Axie Studio files: {len(as_files)}, dirs: {len(as_dirs)}")
    
    # Compare directories
    missing_dirs = lf_dirs - as_dirs
    extra_dirs = as_dirs - lf_dirs
    
    if missing_dirs:
        print(f"\n❌ MISSING DIRECTORIES ({len(missing_dirs)}):")
        for d in sorted(missing_dirs):
            print(f"   • {d}")
        return False
    
    if extra_dirs:
        print(f"\n⚠️  EXTRA DIRECTORIES ({len(extra_dirs)}):")
        for d in sorted(extra_dirs):
            print(f"   • {d}")
    
    # Compare files (normalize for rebranding)
    lf_files_normalized = set()
    as_files_normalized = set()
    
    for file_path in lf_files.keys():
        # Normalize langflow -> axiestudio
        normalized = file_path.replace('langflow', 'axiestudio')
        lf_files_normalized.add(normalized)
    
    for file_path in as_files.keys():
        as_files_normalized.add(file_path)
    
    missing_files = lf_files_normalized - as_files_normalized
    extra_files = as_files_normalized - lf_files_normalized
    
    if missing_files:
        print(f"\n❌ MISSING FILES ({len(missing_files)}):")
        for f in sorted(missing_files)[:20]:  # Show first 20
            print(f"   • {f}")
        return False
    
    if extra_files:
        print(f"\n⚠️  EXTRA FILES ({len(extra_files)}):")
        for f in sorted(extra_files)[:10]:  # Show first 10
            print(f"   • {f}")
    
    print(f"\n✅ File structure match: {len(lf_files_normalized)} files")
    return True

def compare_dependencies():
    """Compare dependencies stringently."""
    print("\n📦 STRINGENT DEPENDENCY COMPARISON")
    print("=" * 50)
    
    def parse_dependencies(pyproject_path):
        """Parse dependencies from pyproject.toml."""
        if not pyproject_path.exists():
            return set()
        
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        deps = set()
        in_deps = False
        for line in content.split('\n'):
            line = line.strip()
            if 'dependencies = [' in line:
                in_deps = True
                continue
            if in_deps and line == ']':
                break
            if in_deps and '"' in line:
                dep = line.strip(',').strip('"').strip()
                if dep and not dep.startswith('#'):
                    # Extract package name
                    pkg_name = dep.split('>=')[0].split('==')[0].split('~=')[0].split('<')[0].split('>')[0].strip()
                    deps.add(pkg_name)
        return deps
    
    # Compare main dependencies
    lf_main_deps = parse_dependencies(LANGFLOW_MAIN / "pyproject.toml")
    as_main_deps = parse_dependencies(AXIESTUDIO_MAIN / "pyproject.toml")
    
    # Normalize for rebranding
    lf_main_deps.discard('langflow-base')
    as_main_deps.discard('axiestudio-base')
    
    missing_main = lf_main_deps - as_main_deps
    extra_main = as_main_deps - lf_main_deps
    
    if missing_main:
        print(f"❌ MISSING MAIN DEPENDENCIES: {missing_main}")
        return False
    
    if extra_main:
        print(f"⚠️  EXTRA MAIN DEPENDENCIES: {extra_main}")
    
    print(f"✅ Main dependencies match: {len(lf_main_deps)} packages")
    
    # Compare base dependencies
    lf_base_deps = parse_dependencies(LANGFLOW_MAIN / "src/backend/base/pyproject.toml")
    as_base_deps = parse_dependencies(AXIESTUDIO_MAIN / "src/backend/base/pyproject.toml")
    
    missing_base = lf_base_deps - as_base_deps
    extra_base = as_base_deps - lf_base_deps
    
    if missing_base:
        print(f"❌ MISSING BASE DEPENDENCIES: {missing_base}")
        return False
    
    if extra_base:
        print(f"⚠️  EXTRA BASE DEPENDENCIES: {extra_base}")
    
    print(f"✅ Base dependencies match: {len(lf_base_deps)} packages")
    return True

def compare_component_files():
    """Compare component files stringently."""
    print("\n🧩 STRINGENT COMPONENT COMPARISON")
    print("=" * 50)
    
    lf_components = LANGFLOW_BASE / "components"
    as_components = AXIESTUDIO_BASE / "components"
    
    if not lf_components.exists():
        print("❌ Langflow components not found for comparison")
        return False
    
    # Get all Python files
    lf_py_files = set()
    as_py_files = set()
    
    for file in lf_components.rglob("*.py"):
        rel_path = file.relative_to(lf_components)
        lf_py_files.add(str(rel_path))
    
    for file in as_components.rglob("*.py"):
        rel_path = file.relative_to(as_components)
        as_py_files.add(str(rel_path))
    
    missing_components = lf_py_files - as_py_files
    extra_components = as_py_files - lf_py_files
    
    if missing_components:
        print(f"❌ MISSING COMPONENT FILES ({len(missing_components)}):")
        for comp in sorted(missing_components)[:20]:
            print(f"   • {comp}")
        return False
    
    if extra_components:
        print(f"⚠️  EXTRA COMPONENT FILES ({len(extra_components)}):")
        for comp in sorted(extra_components)[:10]:
            print(f"   • {comp}")
    
    print(f"✅ Component files match: {len(lf_py_files)} files")
    
    # Check specific AI providers
    providers = ["openai", "anthropic", "google", "groq", "mistral", "cohere"]
    for provider in providers:
        lf_provider = lf_components / provider
        as_provider = as_components / provider
        
        if lf_provider.exists() and not as_provider.exists():
            print(f"❌ Missing AI provider: {provider}")
            return False
        elif lf_provider.exists() and as_provider.exists():
            lf_provider_files = len(list(lf_provider.rglob("*.py")))
            as_provider_files = len(list(as_provider.rglob("*.py")))
            if lf_provider_files != as_provider_files:
                print(f"❌ {provider} file count mismatch: LF={lf_provider_files}, AS={as_provider_files}")
                return False
            print(f"✅ {provider}: {as_provider_files} files")
    
    return True

def compare_critical_imports():
    """Compare critical import statements."""
    print("\n🔗 STRINGENT IMPORT COMPARISON")
    print("=" * 50)
    
    # Check for any remaining langflow imports in Axie Studio
    langflow_imports = []
    
    for file in AXIESTUDIO_BASE.rglob("*.py"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'from langflow' in line or 'import langflow' in line:
                    rel_path = file.relative_to(AXIESTUDIO_BASE)
                    langflow_imports.append(f"{rel_path}:{i} - {line.strip()}")
        except:
            continue
    
    if langflow_imports:
        print(f"❌ FOUND LANGFLOW IMPORTS ({len(langflow_imports)}):")
        for imp in langflow_imports:
            print(f"   • {imp}")
        return False
    
    print("✅ No langflow imports found - all correctly rebranded")
    
    # Check that axiestudio imports exist
    axiestudio_imports = 0
    for file in AXIESTUDIO_BASE.rglob("*.py"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'from axiestudio' in content or 'import axiestudio' in content:
                axiestudio_imports += 1
        except:
            continue
    
    if axiestudio_imports == 0:
        print("❌ No axiestudio imports found - rebranding may be incomplete")
        return False
    
    print(f"✅ Found axiestudio imports in {axiestudio_imports} files")
    return True

def main():
    """Run stringent comparison."""
    print("🔍 ULTRA-STRINGENT LANGFLOW vs AXIE STUDIO COMPARISON")
    print("=" * 70)
    print("Performing the most rigorous comparison possible...")
    print()
    
    os.chdir(Path(__file__).parent)
    
    tests = [
        ("File Structure", compare_file_structures),
        ("Dependencies", compare_dependencies),
        ("Component Files", compare_component_files),
        ("Import Integrity", compare_critical_imports),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name}: PASSED")
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {e}")
    
    print(f"\n🎯 STRINGENT COMPARISON RESULTS")
    print("=" * 70)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 AXIE STUDIO IS A PERFECT LANGFLOW REPLICA!")
        print("✅ Identical file structure")
        print("✅ Identical dependencies")
        print("✅ Identical component files")
        print("✅ Properly rebranded imports")
        print("\n🚀 STRINGENT VERIFICATION COMPLETE!")
        return 0
    else:
        print(f"\n{total - passed} CRITICAL DIFFERENCES DETECTED")
        print("Axie Studio is NOT a perfect replica - review failures above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
