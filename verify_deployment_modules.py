#!/usr/bin/env python3
"""
Comprehensive module verification script for Axie Studio deployment.
This script verifies that all critical modules are properly installed and accessible.
"""

import sys
import importlib
import traceback
from pathlib import Path

# Add the axiestudio package to Python path
current_dir = Path(__file__).parent
axiestudio_base_path = current_dir / "src" / "backend" / "base"
if axiestudio_base_path.exists():
    sys.path.insert(0, str(axiestudio_base_path))
    print(f"📁 Added to Python path: {axiestudio_base_path}")
else:
    print(f"⚠️  Warning: Axiestudio base path not found: {axiestudio_base_path}")

def test_import(module_name, description=""):
    """Test if a module can be imported successfully."""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} - {description}")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - {description} - ERROR: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name} - {description} - UNEXPECTED ERROR: {e}")
        return False

def main():
    """Main verification function."""
    print("🚀 AXIE STUDIO DEPLOYMENT MODULE VERIFICATION")
    print("=" * 60)
    
    # Track results
    total_tests = 0
    passed_tests = 0
    
    # Core Axie Studio modules
    core_modules = [
        ("axiestudio", "Core Axie Studio package"),
        ("axiestudio.base", "Axie Studio base package"),
        ("axiestudio.base.prompts", "Prompts module"),
        ("axiestudio.base.prompts.api_utils", "Prompt API utilities - CRITICAL"),
        ("axiestudio.inputs", "Input components"),
        ("axiestudio.inputs.inputs", "Input definitions"),
        ("axiestudio.io", "I/O components"),
        ("axiestudio.schema", "Schema definitions"),
        ("axiestudio.schema.message", "Message schema"),
        ("axiestudio.schema.data", "Data schema"),
        ("axiestudio.custom", "Custom components"),
        ("axiestudio.template", "Template system"),
        ("axiestudio.template.utils", "Template utilities"),
        ("axiestudio.interface", "Interface components"),
        ("axiestudio.interface.utils", "Interface utilities"),
        ("axiestudio.services", "Service layer"),
        ("axiestudio.services.database", "Database services"),
        ("axiestudio.services.cache", "Cache services"),
        ("axiestudio.graph", "Graph processing"),
        ("axiestudio.processing", "Processing engine"),
        ("axiestudio.api", "API layer"),
        ("axiestudio.main", "Main application"),
    ]
    
    print("\n📦 TESTING CORE AXIE STUDIO MODULES:")
    print("-" * 40)
    for module, desc in core_modules:
        total_tests += 1
        if test_import(module, desc):
            passed_tests += 1
    
    # Critical dependencies
    dependencies = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("sqlmodel", "SQL model framework"),
        ("pydantic", "Data validation"),
        ("loguru", "Logging framework"),
        ("langchain_core", "LangChain core"),
        ("langchain_core.prompts", "LangChain prompts"),
        ("orjson", "JSON serialization"),
        ("httpx", "HTTP client"),
        ("typer", "CLI framework"),
        ("rich", "Rich text formatting"),
        ("platformdirs", "Platform directories"),
        ("alembic", "Database migrations"),
        ("sqlalchemy", "SQL toolkit"),
        ("asyncio", "Async I/O"),
        ("pathlib", "Path utilities"),
        ("uuid", "UUID generation"),
        ("datetime", "Date/time utilities"),
        ("collections", "Collection utilities"),
        ("typing", "Type hints"),
        ("contextlib", "Context utilities"),
        ("functools", "Function utilities"),
        ("threading", "Threading utilities"),
        ("multiprocessing", "Multiprocessing"),
        ("json", "JSON utilities"),
        ("re", "Regular expressions"),
        ("os", "Operating system interface"),
        ("sys", "System utilities"),
        ("warnings", "Warning control"),
        ("inspect", "Object inspection"),
        ("importlib", "Import utilities"),
        ("ast", "Abstract syntax trees"),
        ("base64", "Base64 encoding"),
        ("hashlib", "Hash algorithms"),
        ("secrets", "Secure random numbers"),
        ("time", "Time utilities"),
        ("enum", "Enumerations"),
        ("dataclasses", "Data classes"),
        ("abc", "Abstract base classes"),
    ]
    
    print("\n🔧 TESTING CRITICAL DEPENDENCIES:")
    print("-" * 40)
    for module, desc in dependencies:
        total_tests += 1
        if test_import(module, desc):
            passed_tests += 1
    
    # Test specific critical functions
    print("\n🎯 TESTING CRITICAL FUNCTIONS:")
    print("-" * 40)
    
    # Test the specific function that was failing
    try:
        from axiestudio.base.prompts.api_utils import process_prompt_template
        print("✅ axiestudio.base.prompts.api_utils.process_prompt_template - CRITICAL FUNCTION")
        passed_tests += 1
    except Exception as e:
        print(f"❌ axiestudio.base.prompts.api_utils.process_prompt_template - CRITICAL FUNCTION - ERROR: {e}")
    total_tests += 1
    
    try:
        from axiestudio.inputs.inputs import DefaultPromptField
        print("✅ axiestudio.inputs.inputs.DefaultPromptField - Prompt field class")
        passed_tests += 1
    except Exception as e:
        print(f"❌ axiestudio.inputs.inputs.DefaultPromptField - ERROR: {e}")
    total_tests += 1
    
    try:
        from axiestudio.interface.utils import extract_input_variables_from_prompt
        print("✅ axiestudio.interface.utils.extract_input_variables_from_prompt - Prompt parsing")
        passed_tests += 1
    except Exception as e:
        print(f"❌ axiestudio.interface.utils.extract_input_variables_from_prompt - ERROR: {e}")
    total_tests += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY:")
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL MODULES VERIFIED SUCCESSFULLY!")
        print("✅ Axie Studio is ready for deployment!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} MODULES FAILED VERIFICATION")
        print("❌ Deployment may have issues!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
