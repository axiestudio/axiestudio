#!/usr/bin/env python3
"""
COMPREHENSIVE SCRIPT TO FIX ALL LANGFLOW IMPORTS TO AXIESTUDIO
This script will fix ALL remaining langflow references in test files and other Python files.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix all langflow imports to axiestudio in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix import statements
        import_patterns = [
            (r'from langflow\.', r'from axiestudio.'),
            (r'import langflow\.', r'import axiestudio.'),
            (r'from langflow import', r'from axiestudio import'),
            (r'import langflow', r'import axiestudio'),
        ]
        
        for pattern, replacement in import_patterns:
            content = re.sub(pattern, replacement, content)
        
        # Fix patch decorators and function calls
        patch_patterns = [
            (r'"langflow\.', r'"axiestudio.'),
            (r"'langflow\.", r"'axiestudio."),
            (r'langflow\.', r'axiestudio.'),
        ]
        
        for pattern, replacement in patch_patterns:
            content = re.sub(pattern, replacement, content)
        
        # Fix specific function calls
        function_patterns = [
            (r'import_langflow_components', r'import_axiestudio_components'),
            (r'get_langflow_components', r'get_axiestudio_components'),
        ]
        
        for pattern, replacement in function_patterns:
            content = re.sub(pattern, replacement, content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def fix_all_python_files():
    """Fix all Python files in the src directory."""
    src_dir = Path("src")
    if not src_dir.exists():
        print("❌ src directory not found!")
        return
    
    fixed_count = 0
    total_count = 0
    
    # Find all Python files
    for py_file in src_dir.rglob("*.py"):
        total_count += 1
        if fix_imports_in_file(py_file):
            fixed_count += 1
    
    print(f"\n🎯 SUMMARY:")
    print(f"📁 Total Python files: {total_count}")
    print(f"🔧 Files fixed: {fixed_count}")
    print(f"✅ Files unchanged: {total_count - fixed_count}")

if __name__ == "__main__":
    print("🚀 STARTING COMPREHENSIVE LANGFLOW → AXIESTUDIO IMPORT FIX")
    print("=" * 60)
    fix_all_python_files()
    print("=" * 60)
    print("🎉 IMPORT FIX COMPLETE!")
