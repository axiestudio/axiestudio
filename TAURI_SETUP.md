# Tauri Desktop App Setup for Axie Studio

This document explains the Tauri desktop application setup for Axie Studio.

## 🚀 What's Included

### ✅ **Tauri Configuration**
- `src-tauri/tauri.conf.json` - Main Tauri configuration
- `src-tauri/Cargo.toml` - Rust dependencies and build settings
- `src-tauri/src/main.rs` - Main Rust application code
- `src-tauri/build.rs` - Build script

### ✅ **GitHub Actions Workflow**
- `.github/workflows/tauri-build.yml` - Cross-platform build workflow
- Builds for Windows, macOS, and Linux
- Triggers on `tauri-sv` branch
- Uploads artifacts for each platform

### ✅ **Features Implemented**
- **System Tray** - App runs in system tray
- **Window Management** - Hide/show, minimize/maximize
- **External URLs** - Open links in default browser
- **Cross-Platform** - Windows, macOS, Linux support
- **Auto-updater Ready** - Configuration for future updates

## 🛠️ Development Setup

### Prerequisites
1. **Rust** - Install from [rustup.rs](https://rustup.rs/)
2. **Node.js 20+** - For frontend development
3. **Platform-specific dependencies**:
   - **Windows**: Microsoft C++ Build Tools
   - **macOS**: Xcode Command Line Tools
   - **Linux**: See GitHub Actions workflow for required packages

### Local Development
```bash
# Install Tauri CLI
cargo install tauri-cli

# Install frontend dependencies
cd src/frontend
npm install

# Run in development mode
cargo tauri dev
```

### Building for Production
```bash
# Build for current platform
cargo tauri build

# Build with specific target (macOS universal)
cargo tauri build --target universal-apple-darwin
```

## 🔧 Configuration

### Frontend Integration
- **Dev Server**: `http://localhost:3000` (Vite dev server)
- **Build Output**: `src/frontend/build` (Vite build output)
- **Build Command**: `npm run build` in `src/frontend`

### App Settings
- **App Name**: Axie Studio
- **Bundle ID**: `com.axiestudio.app`
- **Category**: Developer Tool
- **Window Size**: 1200x800 (min: 800x600)

### Permissions
The app has permissions for:
- File system operations (read/write)
- HTTP requests
- Shell operations (open URLs)
- Notifications
- OS information
- Dialog boxes

## 🚀 GitHub Actions Deployment

### Trigger Workflow
1. **Push to `tauri-sv` branch**:
   ```bash
   git checkout -b tauri-sv
   git push origin tauri-sv
   ```

2. **Manual trigger** with release option:
   - Go to GitHub Actions
   - Select "Tauri Build - Axie Studio"
   - Click "Run workflow"
   - Check "Create GitHub Release" if needed

### Build Artifacts
The workflow creates:
- **Windows**: `.msi` installer
- **macOS**: `.dmg` disk image and `.app` bundle
- **Linux**: `.deb`, `.rpm`, and `.AppImage` packages

### Secrets Required (Optional)
For code signing and auto-updates:
- `TAURI_SIGNING_PRIVATE_KEY` - Code signing key
- `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` - Key password

## 📱 App Features

### System Tray
- Left-click to show/hide main window
- Right-click for context menu:
  - Show Axie Studio
  - Hide Axie Studio
  - Quit

### Window Behavior
- Closing window hides to system tray (doesn't quit)
- Minimizes to system tray
- Remembers window size and position

### Integration with Web App
- Uses the same frontend build as the web version
- Can connect to local backend or remote API
- Maintains PWA functionality within desktop app

## 🔄 Next Steps

1. **Test the build** by pushing to `tauri-sv` branch
2. **Customize icons** - Replace placeholder icons with branded ones
3. **Add auto-updater** - Configure update server and signing
4. **Add native features** - File system integration, native notifications
5. **Code signing** - Set up certificates for distribution

## 🐛 Troubleshooting

### Common Issues
1. **Build fails on dependencies**: Check platform-specific requirements
2. **Frontend not found**: Ensure `npm run build` completes successfully
3. **Icons missing**: Verify icon files exist in `src-tauri/icons/`
4. **Permission errors**: Check Tauri allowlist configuration

### Debug Mode
```bash
# Run with debug output
RUST_LOG=debug cargo tauri dev
```

---

Your **Axie Studio** is now ready to be built as a native desktop application! 🎉
