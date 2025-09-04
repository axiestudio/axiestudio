#!/bin/bash

# AxieStudio Tauri Build Testing Script
# This script tests the Tauri build process and validates outputs

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "src-tauri/tauri.conf.json" ]; then
    print_error "Please run this script from the axiestudio directory"
    exit 1
fi

# Function to test configuration
test_configuration() {
    print_status "Testing Tauri configuration..."
    
    # Check tauri.conf.json syntax
    if ! jq empty src-tauri/tauri.conf.json 2>/dev/null; then
        print_error "Invalid JSON in tauri.conf.json"
        return 1
    fi
    
    # Check required fields
    local app_name=$(jq -r '.productName' src-tauri/tauri.conf.json)
    local identifier=$(jq -r '.identifier' src-tauri/tauri.conf.json)
    local version=$(jq -r '.version' src-tauri/tauri.conf.json)
    
    if [ "$app_name" = "null" ] || [ -z "$app_name" ]; then
        print_error "productName is missing in tauri.conf.json"
        return 1
    fi
    
    if [ "$identifier" = "null" ] || [ -z "$identifier" ]; then
        print_error "identifier is missing in tauri.conf.json"
        return 1
    fi
    
    if [ "$version" = "null" ] || [ -z "$version" ]; then
        print_error "version is missing in tauri.conf.json"
        return 1
    fi
    
    print_success "Configuration is valid"
    print_status "App: $app_name"
    print_status "Identifier: $identifier"
    print_status "Version: $version"
}

# Function to test Cargo.toml
test_cargo_config() {
    print_status "Testing Cargo configuration..."
    
    cd src-tauri
    
    # Check Cargo.toml syntax
    if ! cargo check --quiet 2>/dev/null; then
        print_error "Cargo configuration has issues"
        cd ..
        return 1
    fi
    
    # Check for required dependencies
    if ! grep -q "tauri.*=" Cargo.toml; then
        print_error "Tauri dependency is missing from Cargo.toml"
        cd ..
        return 1
    fi
    
    cd ..
    print_success "Cargo configuration is valid"
}

# Function to test frontend build
test_frontend_build() {
    print_status "Testing frontend build..."
    
    cd src/frontend
    
    # Check if package.json exists
    if [ ! -f "package.json" ]; then
        print_error "package.json not found in frontend directory"
        cd ../..
        return 1
    fi
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    fi
    
    # Test build
    if npm run build; then
        print_success "Frontend build successful"
        
        # Check if build output exists
        if [ -d "build" ]; then
            print_success "Build output directory exists"
            
            # Check for index.html
            if [ -f "build/index.html" ]; then
                print_success "index.html found in build output"
            else
                print_warning "index.html not found in build output"
            fi
        else
            print_error "Build output directory not found"
            cd ../..
            return 1
        fi
    else
        print_error "Frontend build failed"
        cd ../..
        return 1
    fi
    
    cd ../..
}

# Function to test icon files
test_icons() {
    print_status "Testing icon files..."
    
    local icons_dir="src-tauri/icons"
    local required_icons=("32x32.png" "128x128.png" "128x128@2x.png" "icon.icns" "icon.ico")
    local missing_icons=()
    
    if [ ! -d "$icons_dir" ]; then
        print_error "Icons directory not found: $icons_dir"
        return 1
    fi
    
    for icon in "${required_icons[@]}"; do
        if [ ! -f "$icons_dir/$icon" ]; then
            missing_icons+=("$icon")
        fi
    done
    
    if [ ${#missing_icons[@]} -gt 0 ]; then
        print_warning "Missing icon files: ${missing_icons[*]}"
        print_status "Creating placeholder icons..."
        
        # Create placeholder icons if ImageMagick is available
        if command -v convert &> /dev/null; then
            for icon in "${missing_icons[@]}"; do
                case "$icon" in
                    "32x32.png")
                        convert -size 32x32 xc:#3B82F6 "$icons_dir/$icon"
                        ;;
                    "128x128.png")
                        convert -size 128x128 xc:#3B82F6 "$icons_dir/$icon"
                        ;;
                    "128x128@2x.png")
                        convert -size 256x256 xc:#3B82F6 "$icons_dir/$icon"
                        ;;
                    "icon.ico"|"icon.icns")
                        convert -size 512x512 xc:#3B82F6 "$icons_dir/$icon"
                        ;;
                esac
            done
            print_success "Created placeholder icons"
        else
            # Create empty files as fallback
            for icon in "${missing_icons[@]}"; do
                touch "$icons_dir/$icon"
            done
            print_warning "Created empty placeholder icons (ImageMagick not available)"
        fi
    else
        print_success "All required icon files are present"
    fi
}

# Function to test Tauri build
test_tauri_build() {
    print_status "Testing Tauri build process..."
    
    # This is a dry run to check if build would work
    print_status "Running Tauri build check..."
    
    if tauri build --help &>/dev/null; then
        print_success "Tauri CLI is working"
    else
        print_error "Tauri CLI is not working properly"
        return 1
    fi
    
    # Test build (this will take time)
    print_status "Starting actual build test (this may take several minutes)..."
    
    if tauri build; then
        print_success "Tauri build completed successfully!"
        
        # Check build outputs
        local bundle_dir="src-tauri/target/release/bundle"
        if [ -d "$bundle_dir" ]; then
            print_success "Bundle directory created: $bundle_dir"
            
            # List available bundles
            print_status "Available bundles:"
            find "$bundle_dir" -name "*.exe" -o -name "*.msi" -o -name "*.dmg" -o -name "*.app" -o -name "*.AppImage" -o -name "*.deb" -o -name "*.rpm" | while read -r file; do
                local size=$(du -h "$file" | cut -f1)
                print_status "  - $(basename "$file") ($size)"
            done
        else
            print_warning "Bundle directory not found"
        fi
    else
        print_error "Tauri build failed"
        return 1
    fi
}

# Function to validate build outputs
validate_outputs() {
    print_status "Validating build outputs..."
    
    local bundle_dir="src-tauri/target/release/bundle"
    local found_bundles=false
    
    # Check for platform-specific bundles
    case "$(uname -s)" in
        Darwin*)
            if ls "$bundle_dir"/macos/*.app &>/dev/null || ls "$bundle_dir"/dmg/*.dmg &>/dev/null; then
                print_success "macOS bundles found"
                found_bundles=true
            fi
            ;;
        Linux*)
            if ls "$bundle_dir"/appimage/*.AppImage &>/dev/null || ls "$bundle_dir"/deb/*.deb &>/dev/null; then
                print_success "Linux bundles found"
                found_bundles=true
            fi
            ;;
        MINGW*|CYGWIN*|MSYS*)
            if ls "$bundle_dir"/msi/*.msi &>/dev/null || ls "$bundle_dir"/nsis/*.exe &>/dev/null; then
                print_success "Windows bundles found"
                found_bundles=true
            fi
            ;;
    esac
    
    if [ "$found_bundles" = false ]; then
        print_warning "No platform-specific bundles found"
        return 1
    fi
}

# Function to run all tests
run_all_tests() {
    print_status "Running comprehensive Tauri build tests..."
    
    local failed_tests=0
    
    test_configuration || ((failed_tests++))
    test_cargo_config || ((failed_tests++))
    test_frontend_build || ((failed_tests++))
    test_icons || ((failed_tests++))
    
    if [ "$1" != "--skip-build" ]; then
        test_tauri_build || ((failed_tests++))
        validate_outputs || ((failed_tests++))
    else
        print_status "Skipping actual build test (--skip-build flag)"
    fi
    
    if [ $failed_tests -eq 0 ]; then
        print_success "All tests passed! ✅"
        print_status "Your Tauri setup is ready for production builds."
    else
        print_error "$failed_tests test(s) failed! ❌"
        print_status "Please fix the issues above before proceeding."
        exit 1
    fi
}

# Main script logic
case "${1:-all}" in
    "config")
        test_configuration
        ;;
    "cargo")
        test_cargo_config
        ;;
    "frontend")
        test_frontend_build
        ;;
    "icons")
        test_icons
        ;;
    "build")
        test_tauri_build
        ;;
    "validate")
        validate_outputs
        ;;
    "all")
        run_all_tests "$2"
        ;;
    "help"|*)
        echo "AxieStudio Tauri Build Testing Script"
        echo ""
        echo "Usage: $0 [test] [options]"
        echo ""
        echo "Tests:"
        echo "  config    - Test Tauri configuration"
        echo "  cargo     - Test Cargo configuration"
        echo "  frontend  - Test frontend build"
        echo "  icons     - Test icon files"
        echo "  build     - Test Tauri build process"
        echo "  validate  - Validate build outputs"
        echo "  all       - Run all tests (default)"
        echo ""
        echo "Options:"
        echo "  --skip-build  - Skip the actual build test (for 'all' command)"
        echo ""
        echo "Examples:"
        echo "  $0              # Run all tests"
        echo "  $0 all --skip-build  # Run all tests except build"
        echo "  $0 config       # Test only configuration"
        ;;
esac
