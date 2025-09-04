# 📥 HOW TO DOWNLOAD YOUR DESKTOP APPS - SUPER SIMPLE!

## 🚀 After You Push to GitHub

1. **Push your code** to GitHub (master/main branch)
2. **Wait 10-15 minutes** for the build to complete
3. **Go to your GitHub repository**
4. **Click "Releases"** (on the right side of your repo page)

## 📦 What You'll Find in Releases

Your GitHub Actions will **automatically create a release** with these files:

### 🪟 **Windows Users Download:**
- **`AxieStudio_1.5.0_x64_en-US.msi`** ← **RECOMMENDED** (Windows Installer)
- **`AxieStudio_1.5.0_x64-setup.exe`** ← Alternative installer

### 🍎 **macOS Users Download:**
- **`AxieStudio_1.5.0_aarch64.dmg`** ← **For Apple Silicon Macs (M1, M2, M3)**
- **`AxieStudio_1.5.0_x64.dmg`** ← **For Intel Macs**
- **`AxieStudio.app.tar.gz`** ← App bundle (advanced users)

### 🐧 **Linux Users Download:**
- **`axiestudio_1.5.0_amd64.AppImage`** ← **RECOMMENDED** (Universal Linux)
- **`axiestudio_1.5.0_amd64.deb`** ← For Ubuntu/Debian
- **`axiestudio-1.5.0-1.x86_64.rpm`** ← For Red Hat/Fedora

## 🎯 SUPER SIMPLE STEPS:

### Step 1: Go to Releases
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases
```

### Step 2: Click "Latest Release"
Look for the newest release (it will be at the top)

### Step 3: Scroll Down to "Assets"
You'll see a list of downloadable files

### Step 4: Download the Right File
- **Windows**: Download the `.msi` file
- **macOS**: Download the `.dmg` file (choose ARM64 for M1+ or x64 for Intel)
- **Linux**: Download the `.AppImage` file

### Step 5: Install & Run!
- **Windows**: Double-click the `.msi` file and follow the installer
- **macOS**: Double-click the `.dmg` file, drag the app to Applications
- **Linux**: Make the `.AppImage` executable and run it

## 🔍 How to Find Your Release URL

Your release URL will be:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases
```

Replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with your repository name

## 📱 Direct Download Links

After the first build, you can share these direct links:

### Latest Release Page:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases/latest
```

### Direct Download Links (replace version number):
```
# Windows MSI
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases/download/v1.5.0/AxieStudio_1.5.0_x64_en-US.msi

# macOS ARM64 (M1+)
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases/download/v1.5.0/AxieStudio_1.5.0_aarch64.dmg

# macOS Intel
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases/download/v1.5.0/AxieStudio_1.5.0_x64.dmg

# Linux AppImage
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases/download/v1.5.0/axiestudio_1.5.0_amd64.AppImage
```

## ⚠️ Security Warnings (NORMAL!)

Since the apps are **unsigned** (for now), users will see:

### Windows:
- "Windows protected your PC" 
- **Click "More info" → "Run anyway"**

### macOS:
- "Cannot be opened because it is from an unidentified developer"
- **Right-click app → "Open" → "Open"**

### Linux:
- No warnings! Linux doesn't require code signing

## 🎉 That's It!

**Your users can now download and install your desktop app on any platform!**

## 🔄 Auto-Updates (Future)

Your apps are already configured for auto-updates! When you release a new version:
1. Users will get a notification
2. They can update with one click
3. No need to download manually again

## 📞 Need Help?

If the build fails or you can't find your releases:
1. Go to your repo → **Actions** tab
2. Check the **"Build and Release AxieStudio Desktop"** workflow
3. Look for any red ❌ errors
4. The logs will tell you exactly what went wrong

**Your desktop apps will be available for download within 15 minutes of pushing to GitHub!** 🚀
