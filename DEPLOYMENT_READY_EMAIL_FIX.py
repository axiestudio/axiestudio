#!/usr/bin/env python3
"""
DEPLOYMENT-READY EMAIL VERIFICATION FIX
This script automatically patches the installed AxieStudio package to fix the email verification issue.

LOGICAL APPROACH:
1. Find the actual installed package location
2. Patch the real email service file that the application uses
3. Fix the missing html_body parameter issue
4. Make it work without admin access
"""

import os
import sys
import shutil
from pathlib import Path
import importlib.util


def find_axiestudio_package_path():
    """Find the actual installed AxieStudio package path."""
    try:
        # Method 1: Try to import and get the path
        import axiestudio
        package_path = Path(axiestudio.__file__).parent
        print(f"✅ Found AxieStudio package at: {package_path}")
        return package_path
    except ImportError:
        print("❌ AxieStudio package not found via import")
    
    # Method 2: Check common installation paths
    possible_paths = [
        Path("/app/.venv/lib/python3.12/site-packages/axiestudio"),
        Path(sys.prefix) / "lib" / "python3.12" / "site-packages" / "axiestudio",
        Path.home() / ".local" / "lib" / "python3.12" / "site-packages" / "axiestudio",
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"✅ Found AxieStudio package at: {path}")
            return path
    
    print("❌ Could not find AxieStudio package installation")
    return None


def backup_original_file(email_service_path):
    """Create a backup of the original email service file."""
    backup_path = email_service_path.with_suffix('.py.backup')
    if not backup_path.exists():
        shutil.copy2(email_service_path, backup_path)
        print(f"✅ Created backup: {backup_path}")
    else:
        print(f"✅ Backup already exists: {backup_path}")
    return backup_path


def fix_email_service_file(email_service_path):
    """Fix the email service file by adding the missing text_body parameter."""
    try:
        print(f"🔧 Fixing email service file: {email_service_path}")
        
        # Read the current file
        with open(email_service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file already has the fix
        if 'text_body' in content and 'await self._send_email(email, subject, text_body, html_body)' in content:
            print("✅ Email service file already appears to be fixed!")
            return True
        
        # Find the problematic line and fix it
        lines = content.split('\n')
        fixed_lines = []
        fix_applied = False
        
        for i, line in enumerate(lines):
            # Look for the problematic _send_email call with only 3 parameters
            if 'await self._send_email(email, subject, html_body)' in line:
                print(f"🔧 Found problematic line {i+1}: {line.strip()}")
                
                # Add text_body creation before the _send_email call
                indent = len(line) - len(line.lstrip())
                text_body_code = f"""
{' ' * indent}# Create text version for email clients that don't support HTML
{' ' * indent}text_body = f\"\"\"
{' ' * indent}AxieStudio - Email Verification

{' ' * indent}Hello {{username}}!

{' ' * indent}Your verification code is: {{verification_code}}

{' ' * indent}⏰ This code expires in 10 minutes

{' ' * indent}How to use this code:
{' ' * indent}1. Return to the AxieStudio verification page
{' ' * indent}2. Enter the 6-digit code above
{' ' * indent}3. Click "Verify Account" to complete setup
{' ' * indent}4. Start building amazing AI workflows!

{' ' * indent}🔒 Security Notice: Never share this code with anyone.

{' ' * indent}---
{' ' * indent}AxieStudio - Building the future of AI workflows
{' ' * indent}Visit us at: https://axiestudio.se
{' ' * indent}Need help? Contact our support team - we're here to help!
{' ' * indent}\"\"\"

{' ' * indent}# Send email with BOTH text and HTML versions (Enterprise standard)"""
                
                # Add the text_body creation code
                fixed_lines.extend(text_body_code.split('\n')[1:])  # Skip first empty line
                
                # Fix the _send_email call
                fixed_line = line.replace(
                    'await self._send_email(email, subject, html_body)',
                    'await self._send_email(email, subject, text_body, html_body)'
                )
                fixed_lines.append(fixed_line)
                fix_applied = True
                print(f"✅ Fixed line {i+1}: {fixed_line.strip()}")
                
            else:
                fixed_lines.append(line)
        
        if not fix_applied:
            print("❌ Could not find the problematic _send_email call to fix")
            return False
        
        # Write the fixed content back
        fixed_content = '\n'.join(fixed_lines)
        with open(email_service_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print("✅ Email service file has been fixed!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing email service file: {e}")
        return False


def verify_fix(email_service_path):
    """Verify that the fix was applied correctly."""
    try:
        with open(email_service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for the fix
        if 'text_body' in content and 'await self._send_email(email, subject, text_body, html_body)' in content:
            print("✅ Fix verification: Email service file contains the correct _send_email call")
            return True
        else:
            print("❌ Fix verification: Email service file still has the issue")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying fix: {e}")
        return False


def main():
    """Main function to apply the email verification fix."""
    print("🚀 DEPLOYMENT-READY EMAIL VERIFICATION FIX")
    print("=" * 60)
    print("This script fixes the 'missing html_body' error in AxieStudio email verification")
    print()
    
    # Step 1: Find the AxieStudio package
    print("📍 Step 1: Locating AxieStudio package...")
    package_path = find_axiestudio_package_path()
    if not package_path:
        print("❌ Cannot proceed without finding the AxieStudio package")
        return 1
    
    # Step 2: Locate the email service file
    print("\n📧 Step 2: Locating email service file...")
    email_service_path = package_path / "services" / "email" / "service.py"
    
    if not email_service_path.exists():
        print(f"❌ Email service file not found at: {email_service_path}")
        return 1
    
    print(f"✅ Found email service file: {email_service_path}")
    
    # Step 3: Create backup
    print("\n💾 Step 3: Creating backup...")
    backup_path = backup_original_file(email_service_path)
    
    # Step 4: Apply the fix
    print("\n🔧 Step 4: Applying email verification fix...")
    if not fix_email_service_file(email_service_path):
        print("❌ Failed to apply fix")
        return 1
    
    # Step 5: Verify the fix
    print("\n✅ Step 5: Verifying fix...")
    if not verify_fix(email_service_path):
        print("❌ Fix verification failed")
        return 1
    
    print("\n🎉 EMAIL VERIFICATION FIX APPLIED SUCCESSFULLY!")
    print("=" * 60)
    print("✅ The 'missing html_body' error should now be resolved")
    print("✅ Email verification codes will now be sent successfully")
    print("✅ Users can complete account verification")
    print()
    print("🚀 NEXT STEPS:")
    print("1. Restart your AxieStudio application")
    print("2. Test email verification with a new user account")
    print("3. Check that verification emails are received")
    print()
    print(f"📁 Backup created at: {backup_path}")
    print("   (You can restore from backup if needed)")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
