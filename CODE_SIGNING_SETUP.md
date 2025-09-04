# Code Signing Setup for AxieStudio Desktop

## Overview
Code signing is essential for distributing desktop applications without security warnings. This guide covers setting up code signing for Windows and macOS builds.

## Windows Code Signing

### Requirements
- Code signing certificate from a trusted CA (DigiCert, Sectigo, etc.)
- Certificate in PFX format with private key

### Setup Steps

1. **Obtain Certificate**
   - Purchase from a Certificate Authority
   - Or use self-signed for testing (not recommended for distribution)

2. **Convert Certificate to Base64**
   ```bash
   # Convert PFX to base64 for GitHub Secrets
   base64 -i your-certificate.pfx -o certificate-base64.txt
   ```

3. **Add GitHub Secrets**
   Go to your repository Settings → Secrets and variables → Actions:
   - `TAURI_SIGNING_PRIVATE_KEY`: Base64 encoded PFX certificate
   - `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`: Certificate password

### Tauri Configuration
Update `tauri.conf.json`:
```json
{
  "bundle": {
    "windows": {
      "certificateThumbprint": null,
      "digestAlgorithm": "sha256",
      "timestampUrl": "http://timestamp.digicert.com",
      "wix": {
        "license": "../LICENSE"
      },
      "nsis": {
        "license": "../LICENSE",
        "installerIcon": "icons/icon.ico"
      }
    }
  }
}
```

## macOS Code Signing

### Requirements
- Apple Developer Account ($99/year)
- Developer ID Application certificate
- Developer ID Installer certificate (for PKG)

### Setup Steps

1. **Create Certificates in Apple Developer Portal**
   - Log into developer.apple.com
   - Go to Certificates, Identifiers & Profiles
   - Create "Developer ID Application" certificate
   - Create "Developer ID Installer" certificate

2. **Export Certificates**
   ```bash
   # Export from Keychain Access as .p12 files
   # Convert to base64 for GitHub Secrets
   base64 -i DeveloperIDApplication.p12 -o dev-id-app-base64.txt
   ```

3. **Add GitHub Secrets**
   - `APPLE_CERTIFICATE`: Base64 encoded Developer ID Application certificate
   - `APPLE_CERTIFICATE_PASSWORD`: Certificate password
   - `APPLE_SIGNING_IDENTITY`: Certificate name (e.g., "Developer ID Application: Your Name")
   - `APPLE_ID`: Your Apple ID email
   - `APPLE_PASSWORD`: App-specific password (not your Apple ID password)
   - `APPLE_TEAM_ID`: Your team ID from Apple Developer portal

4. **Create App-Specific Password**
   - Go to appleid.apple.com
   - Sign in → App-Specific Passwords
   - Generate password for "Tauri Notarization"

### Tauri Configuration
Update `tauri.conf.json`:
```json
{
  "bundle": {
    "macOS": {
      "minimumSystemVersion": "10.15",
      "hardenedRuntime": true,
      "entitlements": "entitlements.plist",
      "signingIdentity": null,
      "providerShortName": null
    }
  }
}
```

### Create Entitlements File
Create `src-tauri/entitlements.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.network.server</key>
    <true/>
</dict>
</plist>
```

## Linux Code Signing

Linux doesn't require code signing like Windows/macOS, but you can:
- Sign packages with GPG keys
- Distribute through official repositories
- Use AppImage signing (optional)

## Testing Code Signing

### Local Testing
```bash
# Install Tauri CLI
npm install -g @tauri-apps/cli

# Build with signing (requires certificates)
cd axiestudio
tauri build

# Check Windows signature
signtool verify /pa /v "target/release/bundle/msi/AxieStudio_1.5.0_x64_en-US.msi"

# Check macOS signature  
codesign -dv --verbose=4 "target/release/bundle/macos/AxieStudio.app"
spctl -a -t exec -vv "target/release/bundle/macos/AxieStudio.app"
```

### GitHub Actions Testing
The workflow includes code signing automatically when secrets are configured.

## Troubleshooting

### Windows Issues
- **"Certificate not found"**: Check certificate format and password
- **"Timestamp server unavailable"**: Try different timestamp URLs
- **"Invalid certificate"**: Ensure certificate is for code signing

### macOS Issues  
- **"No signing identity found"**: Check certificate installation
- **"Notarization failed"**: Verify Apple ID credentials and app-specific password
- **"Invalid entitlements"**: Check entitlements.plist syntax

### Common Solutions
1. **Verify certificate validity**: Check expiration dates
2. **Test locally first**: Don't rely only on CI/CD
3. **Check logs**: GitHub Actions provides detailed signing logs
4. **Use staging environment**: Test with development certificates first

## Security Best Practices

1. **Protect Private Keys**
   - Never commit certificates to version control
   - Use GitHub Secrets for sensitive data
   - Rotate certificates before expiration

2. **Validate Signatures**
   - Test signed applications on clean systems
   - Verify signatures after build
   - Monitor certificate expiration

3. **Backup Certificates**
   - Keep secure backups of certificates
   - Document renewal procedures
   - Have contingency plans for certificate issues

## Cost Considerations

- **Windows**: $200-500/year for code signing certificate
- **macOS**: $99/year for Apple Developer Program
- **Total**: ~$300-600/year for professional code signing

## Alternative Solutions

### For Testing/Development
- Self-signed certificates (users will see warnings)
- Skip code signing (more security warnings)
- Use development builds only

### For Open Source Projects
- Some CAs offer discounted certificates for OSS
- Community signing services (limited availability)
- User education about security warnings
