# 🔐 Enable Code Signing Later - Simple Guide

## 📋 Current Status
✅ **Your apps will build UNSIGNED** - Perfect for testing!  
✅ **No secrets needed right now** - Keep it simple  
✅ **All platforms supported** - Windows, macOS, Linux  

## ⚠️ What This Means
- **Windows**: Users will see "Unknown publisher" warning (they can still install)
- **macOS**: Users will see "Unidentified developer" warning (they can bypass it)
- **Linux**: No warnings (Linux doesn't require code signing)

## 🚀 When You're Ready to Enable Signing (Later)

### Step 1: On Your Mac - Create Certificates

1. **Open Keychain Access** on your Mac
2. **Go to Apple Developer Portal**: https://developer.apple.com/account/resources/certificates/list
3. **Create these certificates**:
   - "Developer ID Application" (for app signing)
   - "Developer ID Installer" (for PKG installer)

### Step 2: Export Certificates from Mac

```bash
# In Keychain Access, export as .p12 files
# Then convert to base64:
base64 -i DeveloperIDApplication.p12 -o dev-id-app-base64.txt
```

### Step 3: Create App-Specific Password

1. Go to https://appleid.apple.com
2. Sign in → App-Specific Passwords
3. Generate password for "Tauri Notarization"

### Step 4: Add GitHub Secrets

Go to your GitHub repo → Settings → Secrets and variables → Actions:

**Required Secrets:**
- `APPLE_CERTIFICATE`: Content of `dev-id-app-base64.txt`
- `APPLE_CERTIFICATE_PASSWORD`: Password you used when exporting .p12
- `APPLE_SIGNING_IDENTITY`: "Developer ID Application: Your Name (TEAM_ID)"
- `APPLE_ID`: Your Apple ID email
- `APPLE_PASSWORD`: App-specific password from Step 3
- `APPLE_TEAM_ID`: Your team ID (found in Apple Developer portal)

### Step 5: Enable Signing in Code

**In `.github/workflows/tauri-build.yml`:**
```yaml
# Uncomment these lines:
env:
  APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
  APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
  # ... etc
```

**In `src-tauri/tauri.conf.json`:**
```json
{
  "bundle": {
    "macOS": {
      "hardenedRuntime": true,
      "entitlements": "entitlements.plist"
    }
  }
}
```

## 🎯 For Now - Just Build and Test!

**Your current setup will:**
- ✅ Build for Windows, macOS, Linux
- ✅ Create installers (MSI, DMG, AppImage, etc.)
- ✅ Work perfectly for development and testing
- ✅ Be ready for signing when you add certificates later

## 🚀 Next Steps (Right Now)

1. **Add icons**: `tauri icon your-icon.png`
2. **Push to GitHub** to trigger first build
3. **Download and test** the unsigned apps
4. **Add signing later** when you have your Mac ready

**The apps will work perfectly - they'll just show security warnings that users can bypass!** 🎉
