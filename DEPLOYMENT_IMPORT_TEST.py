#!/usr/bin/env python3
"""
COMPREHENSIVE IMPORT VERIFICATION FOR DEPLOYMENT
This script tests ALL critical imports that could cause deployment failures.
"""

import sys
import traceback
from pathlib import Path

# Add the source directory to Python path
src_path = Path(__file__).parent / "src" / "backend" / "base"
sys.path.insert(0, str(src_path))

def test_import(module_name, description):
    """Test importing a module and report results."""
    try:
        __import__(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except Exception as e:
        print(f"❌ {description}: {module_name}")
        print(f"   Error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run comprehensive import tests."""
    print("🔍 COMPREHENSIVE DEPLOYMENT IMPORT VERIFICATION")
    print("=" * 60)
    print()
    
    failed_imports = []
    
    # Test 1: Core package imports
    print("📦 TESTING CORE PACKAGE IMPORTS...")
    tests = [
        ("axiestudio", "Base package"),
        ("axiestudio.__main__", "Main module"),
        ("axiestudio.axiestudio_launcher", "Launcher module"),
    ]
    
    for module, desc in tests:
        if not test_import(module, desc):
            failed_imports.append(module)
    
    print()
    
    # Test 2: Critical service imports
    print("⚙️ TESTING CRITICAL SERVICE IMPORTS...")
    tests = [
        ("axiestudio.services.settings.base", "Settings base"),
        ("axiestudio.services.database", "Database service"),
        ("axiestudio.services.auth", "Authentication service"),
        ("axiestudio.logging.logger", "Logging service"),
    ]
    
    for module, desc in tests:
        if not test_import(module, desc):
            failed_imports.append(module)
    
    print()
    
    # Test 3: Component system imports
    print("🧩 TESTING COMPONENT SYSTEM IMPORTS...")
    tests = [
        ("axiestudio.interface.components", "Component interface"),
        ("axiestudio.custom.utils", "Custom component utils"),
        ("axiestudio.components", "Components package"),
    ]
    
    for module, desc in tests:
        if not test_import(module, desc):
            failed_imports.append(module)
    
    print()
    
    # Test 4: Critical AI provider imports
    print("🤖 TESTING AI PROVIDER IMPORTS...")
    tests = [
        ("axiestudio.components.openai", "OpenAI components"),
        ("axiestudio.components.anthropic", "Anthropic components"),
        ("axiestudio.components.google", "Google AI components"),
        ("axiestudio.components.groq", "Groq components"),
        ("axiestudio.components.mistral", "Mistral components"),
    ]
    
    for module, desc in tests:
        if not test_import(module, desc):
            failed_imports.append(module)
    
    print()
    
    # Test 5: Vector store imports
    print("🗄️ TESTING VECTOR STORE IMPORTS...")
    tests = [
        ("axiestudio.components.vectorstores", "Vector stores package"),
        ("axiestudio.components.vectorstores.pinecone", "Pinecone"),
        ("axiestudio.components.vectorstores.chroma", "Chroma"),
        ("axiestudio.components.vectorstores.qdrant", "Qdrant"),
    ]
    
    for module, desc in tests:
        if not test_import(module, desc):
            failed_imports.append(module)
    
    print()
    
    # Test 6: API and server imports
    print("🌐 TESTING API AND SERVER IMPORTS...")
    tests = [
        ("axiestudio.api", "API package"),
        ("axiestudio.server", "Server module"),
        ("axiestudio.main", "Main server"),
    ]
    
    for module, desc in tests:
        if not test_import(module, desc):
            failed_imports.append(module)
    
    print()
    
    # Test 7: Component loading function
    print("🔧 TESTING COMPONENT LOADING FUNCTION...")
    try:
        from axiestudio.interface.components import import_axiestudio_components
        print("✅ Component loading function: import_axiestudio_components")
    except Exception as e:
        print(f"❌ Component loading function: import_axiestudio_components")
        print(f"   Error: {e}")
        failed_imports.append("import_axiestudio_components")
    
    print()
    
    # Final results
    print("🎯 IMPORT VERIFICATION RESULTS")
    print("=" * 60)
    
    if not failed_imports:
        print("🎉 ALL IMPORTS SUCCESSFUL!")
        print("✅ Your Axie Studio is ready for deployment")
        print("✅ Zero import errors detected")
        print("✅ All critical systems verified")
        return 0
    else:
        print(f"❌ {len(failed_imports)} IMPORT FAILURES DETECTED:")
        for module in failed_imports:
            print(f"   • {module}")
        print()
        print("🚨 DEPLOYMENT WILL FAIL!")
        print("🔧 Fix these imports before deploying")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
