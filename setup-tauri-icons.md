# Tauri Icon Setup Guide

## Quick Icon Generation

To generate the required icons for your Tauri application, you have several options:

### Option 1: Using Tauri CLI (Recommended)
```bash
# Install Tauri CLI if not already installed
npm install -g @tauri-apps/cli

# Generate icons from a single source image (1024x1024 recommended)
cd axiestudio
tauri icon path/to/your/source-icon.png
```

### Option 2: Online Icon Generator
1. Visit [Tauri Icon Generator](https://tauri.app/guides/features/icons/)
2. Upload a high-resolution source image (1024x1024 PNG recommended)
3. Download the generated icon pack
4. Extract to `src-tauri/icons/` directory

### Option 3: Manual Creation
Create the following files in `src-tauri/icons/`:

#### Required Files:
- `32x32.png` - 32×32 pixels
- `128x128.png` - 128×128 pixels
- `128x128@2x.png` - 256×256 pixels (high DPI)
- `icon.icns` - macOS icon bundle
- `icon.ico` - Windows icon file

#### Tools for Manual Creation:
- **Windows**: Use GIMP, Paint.NET, or online converters
- **macOS**: Use Icon Composer, Preview, or online converters  
- **Linux**: Use GIMP, ImageMagick, or online converters

### Option 4: ImageMagick Command Line
If you have ImageMagick installed:

```bash
# Convert source image to required PNG sizes
convert source-icon.png -resize 32x32 src-tauri/icons/32x32.png
convert source-icon.png -resize 128x128 src-tauri/icons/128x128.png
convert source-icon.png -resize 256x256 src-tauri/icons/128x128@2x.png

# For ICO file (Windows)
convert source-icon.png -resize 256x256 src-tauri/icons/icon.ico

# For ICNS file (macOS) - requires additional tools
# Use online converter or macOS-specific tools
```

## Icon Requirements

### Source Image Guidelines:
- **Format**: PNG with transparency
- **Size**: 1024×1024 pixels minimum
- **Design**: Simple, clear design that scales well
- **Background**: Transparent or solid color
- **Content**: Avoid fine details that disappear at small sizes

### Platform-Specific Notes:
- **Windows**: ICO file supports multiple sizes in one file
- **macOS**: ICNS file is a bundle format with multiple resolutions
- **Linux**: PNG files are used directly

## Verification

After adding icons, verify they're correctly referenced in `tauri.conf.json`:

```json
{
  "bundle": {
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png", 
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

## Testing Icons

Test your icons by building the application:

```bash
cd axiestudio
npm install -g @tauri-apps/cli  # if not installed
tauri build
```

The built application will use your custom icons on each platform.
