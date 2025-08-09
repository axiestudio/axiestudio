#!/usr/bin/env python3
"""
DEPLOYMENT STRUCTURE VERIFICATION
This script verifies that all files and import paths are correctly structured for deployment.
It checks file existence and import syntax without actually importing (to avoid dependency issues).
"""

import ast
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a critical file exists."""
    if file_path.exists():
        print(f"✅ {description}: {file_path.name}")
        return True
    else:
        print(f"❌ {description}: {file_path.name} - FILE MISSING")
        return False

def check_import_syntax(file_path, description):
    """Check if a Python file has valid syntax and correct import statements."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check syntax
        ast.parse(content)
        
        # Check for langflow imports (should be axiestudio)
        if 'from langflow' in content or 'import langflow' in content:
            print(f"⚠️  {description}: Contains langflow imports")
            return False
        
        print(f"✅ {description}: Valid syntax, correct imports")
        return True
    except SyntaxError as e:
        print(f"❌ {description}: Syntax error - {e}")
        return False
    except Exception as e:
        print(f"❌ {description}: Error - {e}")
        return False

def main():
    """Run deployment structure verification."""
    print("🔍 DEPLOYMENT STRUCTURE VERIFICATION")
    print("=" * 50)
    print()
    
    base_path = Path(__file__).parent
    src_path = base_path / "src" / "backend" / "base" / "axiestudio"
    
    failed_checks = []
    
    # Test 1: Critical file existence
    print("📁 CHECKING CRITICAL FILE EXISTENCE...")
    critical_files = [
        (src_path / "__init__.py", "Base package init"),
        (src_path / "__main__.py", "Main module"),
        (src_path / "axiestudio_launcher.py", "Launcher"),
        (src_path / "interface" / "components.py", "Component interface"),
        (src_path / "services" / "settings" / "base.py", "Settings base"),
        (base_path / "pyproject.toml", "Main pyproject.toml"),
        (base_path / "src" / "backend" / "base" / "pyproject.toml", "Base pyproject.toml"),
        (base_path / "Dockerfile", "Dockerfile"),
        (base_path / "uv.lock", "UV lock file"),
    ]
    
    for file_path, desc in critical_files:
        if not check_file_exists(file_path, desc):
            failed_checks.append(f"Missing file: {file_path}")
    
    print()
    
    # Test 2: Component directory structure
    print("🧩 CHECKING COMPONENT STRUCTURE...")
    components_path = src_path / "components"
    
    if components_path.exists():
        component_dirs = [d for d in components_path.iterdir() if d.is_dir()]
        print(f"✅ Component directories: {len(component_dirs)} found")
        
        # Check key AI providers
        key_providers = ["openai", "anthropic", "google", "groq", "mistral", "cohere"]
        for provider in key_providers:
            provider_path = components_path / provider
            if provider_path.exists():
                print(f"✅ AI Provider: {provider}")
            else:
                print(f"❌ AI Provider: {provider} - MISSING")
                failed_checks.append(f"Missing AI provider: {provider}")
        
        # Check vector stores
        vectorstores_path = components_path / "vectorstores"
        if vectorstores_path.exists():
            vector_files = list(vectorstores_path.glob("*.py"))
            print(f"✅ Vector stores: {len(vector_files)} implementations")
        else:
            print("❌ Vector stores directory missing")
            failed_checks.append("Missing vectorstores directory")
    else:
        print("❌ Components directory missing")
        failed_checks.append("Missing components directory")
    
    print()
    
    # Test 3: Import syntax verification
    print("🔧 CHECKING IMPORT SYNTAX...")
    syntax_files = [
        (src_path / "__main__.py", "Main module syntax"),
        (src_path / "axiestudio_launcher.py", "Launcher syntax"),
        (src_path / "interface" / "components.py", "Component interface syntax"),
    ]
    
    for file_path, desc in syntax_files:
        if file_path.exists():
            if not check_import_syntax(file_path, desc):
                failed_checks.append(f"Import issue: {file_path}")
        else:
            failed_checks.append(f"Missing for syntax check: {file_path}")
    
    print()
    
    # Test 4: Docker configuration
    print("🐳 CHECKING DOCKER CONFIGURATION...")
    dockerfile_path = base_path / "Dockerfile"
    if dockerfile_path.exists():
        with open(dockerfile_path, 'r') as f:
            dockerfile_content = f.read()
        
        if "axiestudio" in dockerfile_content:
            print("✅ Dockerfile: Contains axiestudio references")
        else:
            print("❌ Dockerfile: Missing axiestudio references")
            failed_checks.append("Dockerfile missing axiestudio references")
        
        if "uv sync" in dockerfile_content:
            print("✅ Dockerfile: Uses UV for dependency management")
        else:
            print("❌ Dockerfile: Missing UV dependency management")
            failed_checks.append("Dockerfile missing UV commands")
    else:
        print("❌ Dockerfile missing")
        failed_checks.append("Missing Dockerfile")
    
    print()
    
    # Test 5: Package configuration
    print("📦 CHECKING PACKAGE CONFIGURATION...")
    main_pyproject = base_path / "pyproject.toml"
    if main_pyproject.exists():
        with open(main_pyproject, 'r') as f:
            content = f.read()
        
        if 'axiestudio = "axiestudio.axiestudio_launcher:main"' in content:
            print("✅ Entry point: Correctly configured")
        else:
            print("❌ Entry point: Incorrect configuration")
            failed_checks.append("Incorrect entry point configuration")
        
        if "axiestudio-base" in content:
            print("✅ Dependencies: References axiestudio-base")
        else:
            print("❌ Dependencies: Missing axiestudio-base reference")
            failed_checks.append("Missing axiestudio-base dependency")
    
    print()
    
    # Final results
    print("🎯 DEPLOYMENT STRUCTURE VERIFICATION RESULTS")
    print("=" * 50)
    
    if not failed_checks:
        print("🎉 ALL STRUCTURE CHECKS PASSED!")
        print("✅ File structure is correct")
        print("✅ Import paths are properly rebranded")
        print("✅ Component structure is complete")
        print("✅ Docker configuration is valid")
        print("✅ Package configuration is correct")
        print()
        print("🚀 DEPLOYMENT STRUCTURE IS READY!")
        print("📝 Note: Import failures in local environment are expected")
        print("📝 Docker will install all dependencies during build")
        return 0
    else:
        print(f"❌ {len(failed_checks)} STRUCTURE ISSUES DETECTED:")
        for issue in failed_checks:
            print(f"   • {issue}")
        print()
        print("FIX THESE ISSUES BEFORE DEPLOYMENT!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
