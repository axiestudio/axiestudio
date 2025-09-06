#!/usr/bin/env python3
"""
Axie Studio Setup and Launch Script
Sets up all required paths and environment variables, then launches Axie Studio
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def setup_environment():
    """Set up all required environment variables and paths"""
    
    print("=" * 80)
    print("🚀 AXIE STUDIO - COMPLETE ENVIRONMENT SETUP AND LAUNCH SCRIPT")
    print("=" * 80)
    
    # Set up paths
    print("🔧 Setting up system paths...")
    
    # Python path
    python_path = r"C:\Program Files\Python313"
    python_scripts = r"C:\Program Files\Python313\Scripts"
    
    # Node.js path
    nodejs_path = r"C:\Program Files\nodejs"
    
    # Rust Cargo path
    cargo_path = os.path.join(os.path.expanduser("~"), ".cargo", "bin")
    
    # Update PATH
    current_path = os.environ.get("PATH", "")
    new_paths = [python_path, python_scripts, nodejs_path, cargo_path]
    
    for path in new_paths:
        if path not in current_path:
            current_path = f"{path};{current_path}"
    
    os.environ["PATH"] = current_path
    print(f"✅ Updated PATH with Python, Node.js, and Cargo")
    
    # Set up all environment variables
    print("🌍 Setting up environment variables...")
    
    env_vars = {
        # Core Application Settings
        "AXIESTUDIO_AUTO_LOGIN": "false",
        "AXIESTUDIO_CACHE_TYPE": "memory",
        "AXIESTUDIO_HOST": "0.0.0.0",
        "AXIESTUDIO_PORT": "7860",
        "AXIESTUDIO_LOG_LEVEL": "DEBUG",
        "AXIESTUDIO_NEW_USER_IS_ACTIVE": "true",
        "AXIESTUDIO_WORKERS": "1",
        "AXIESTUDIO_SECRET_KEY": "your_secret_key_here",
        
        # Database Configuration
        "AXIESTUDIO_DATABASE_URL": "your_database_url_here",

        # Superuser Configuration
        "AXIESTUDIO_SUPERUSER": "your_admin_email_here",
        "AXIESTUDIO_SUPERUSER_PASSWORD": "your_admin_password_here",

        # Email Configuration
        "AXIESTUDIO_EMAIL_FROM_EMAIL": "noreply@yourdomain.com",
        "AXIESTUDIO_EMAIL_FROM_NAME": "Your App Name",
        "AXIESTUDIO_EMAIL_SMTP_HOST": "smtp.resend.com",
        "AXIESTUDIO_EMAIL_SMTP_PASSWORD": "your_smtp_password_here",
        "AXIESTUDIO_EMAIL_SMTP_PORT": "587",
        "AXIESTUDIO_EMAIL_SMTP_USER": "resend",
        "AXIESTUDIO_EMAIL_ENABLED": "true",
        "AXIESTUDIO_EMAIL_USE_TLS": "true",
        "AXIESTUDIO_EMAIL_USE_SSL": "false",
        
        # Stripe Configuration
        "STRIPE_PRICE_ID": "your_stripe_price_id_here",
        "STRIPE_PUBLISHABLE_KEY": "your_stripe_publishable_key_here",
        "STRIPE_SECRET_KEY": "your_stripe_secret_key_here",
        "STRIPE_WEBHOOK_SECRET": "your_stripe_webhook_secret_here",
        
        # Other Configuration
        "DO_NOT_TRACK": "1",
        "FRONTEND_URL": "https://yourdomain.com/",
        "PORT": "7860",
    }
    
    # Set all environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"✅ Set {key}")
    
    print("=" * 80)
    print("✅ ENVIRONMENT SETUP COMPLETE!")
    print("=" * 80)

def setup_visual_studio():
    """Set up Visual Studio build environment on Windows"""
    if platform.system() == "Windows":
        print("🔧 Setting up Visual Studio Build Tools...")
        vs_script = r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
        
        if os.path.exists(vs_script):
            # Create a batch file to set up VS environment and run our command
            batch_content = f'''@echo off
call "{vs_script}"
python -m uv run axiestudio run
'''
            with open("run_with_vs.bat", "w") as f:
                f.write(batch_content)
            print("✅ Visual Studio environment script created")
            return True
        else:
            print("⚠️ Visual Studio Build Tools not found at expected location")
            return False
    return False

def verify_dependencies():
    """Verify that all required dependencies are available"""
    print("🔍 Verifying dependencies...")
    
    # Check Python
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False
    
    # Check UV
    try:
        result = subprocess.run([sys.executable, "-m", "uv", "--version"], capture_output=True, text=True)
        print(f"✅ UV: {result.stdout.strip()}")
    except Exception as e:
        print(f"⚠️ UV not found, installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
            print("✅ UV installed successfully")
        except Exception as install_error:
            print(f"❌ Failed to install UV: {install_error}")
            return False
    
    return True

def launch_axiestudio():
    """Launch Axie Studio with proper environment"""
    print("=" * 80)
    print("🚀 LAUNCHING AXIE STUDIO...")
    print("=" * 80)
    
    try:
        # On Windows, use the VS environment batch file if available
        if platform.system() == "Windows" and os.path.exists("run_with_vs.bat"):
            print("🔧 Using Visual Studio environment...")
            subprocess.run(["run_with_vs.bat"], shell=True)
        else:
            # Direct launch
            subprocess.run([sys.executable, "-m", "uv", "run", "axiestudio", "run"])
            
    except KeyboardInterrupt:
        print("\n🛑 Axie Studio stopped by user")
    except Exception as e:
        print(f"❌ Error launching Axie Studio: {e}")
    finally:
        # Clean up
        if os.path.exists("run_with_vs.bat"):
            os.remove("run_with_vs.bat")

def main():
    """Main function"""
    try:
        # Change to the script directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Set up environment
        setup_environment()
        
        # Set up Visual Studio (Windows only)
        setup_visual_studio()
        
        # Verify dependencies
        if not verify_dependencies():
            print("❌ Dependency verification failed!")
            input("Press Enter to exit...")
            return
        
        # Launch Axie Studio
        launch_axiestudio()
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
