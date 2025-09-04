#!/bin/bash

# AxieStudio Tauri Development Script
# This script helps with local Tauri development and testing

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

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    # Check Rust
    if ! command -v rustc &> /dev/null; then
        print_error "Rust is not installed. Please install Rust first."
        print_status "Visit: https://rustup.rs/"
        exit 1
    fi
    
    # Check Tauri CLI
    if ! command -v tauri &> /dev/null; then
        print_warning "Tauri CLI is not installed. Installing..."
        npm install -g @tauri-apps/cli
    fi
    
    print_success "All prerequisites are installed!"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Install frontend dependencies
    print_status "Installing frontend dependencies..."
    cd src/frontend
    if [ -f "package-lock.json" ]; then
        npm ci
    else
        npm install
    fi
    cd ../..
    
    # Install Rust dependencies (this happens automatically with Tauri)
    print_status "Rust dependencies will be installed automatically by Tauri"
    
    print_success "Dependencies installed!"
}

# Function to create placeholder icons
create_placeholder_icons() {
    print_status "Creating placeholder icons..."
    
    mkdir -p src-tauri/icons
    
    # Create simple colored squares as placeholder icons
    # Note: This requires ImageMagick. If not available, create empty files
    if command -v convert &> /dev/null; then
        convert -size 32x32 xc:#3B82F6 src-tauri/icons/32x32.png
        convert -size 128x128 xc:#3B82F6 src-tauri/icons/128x128.png
        convert -size 256x256 xc:#3B82F6 src-tauri/icons/128x128@2x.png
        convert -size 512x512 xc:#3B82F6 src-tauri/icons/icon.ico
        convert -size 512x512 xc:#3B82F6 src-tauri/icons/icon.icns
        print_success "Created placeholder icons with ImageMagick"
    else
        touch src-tauri/icons/32x32.png
        touch src-tauri/icons/128x128.png
        touch src-tauri/icons/128x128@2x.png
        touch src-tauri/icons/icon.ico
        touch src-tauri/icons/icon.icns
        print_warning "Created empty placeholder icons (ImageMagick not found)"
        print_status "Please replace with actual icons before building for production"
    fi
}

# Function to run development server
run_dev() {
    print_status "Starting Tauri development server..."
    print_status "This will start both the frontend dev server and Tauri app"
    
    # Build frontend first
    print_status "Building frontend..."
    cd src/frontend
    npm run build
    cd ../..
    
    # Start Tauri dev
    tauri dev
}

# Function to build the application
build_app() {
    print_status "Building Tauri application..."
    
    # Build frontend
    print_status "Building frontend..."
    cd src/frontend
    npm run build
    cd ../..
    
    # Build Tauri app
    print_status "Building Tauri app (this may take a while)..."
    tauri build
    
    print_success "Build completed! Check src-tauri/target/release/bundle/ for output files"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    
    # Frontend tests
    print_status "Running frontend tests..."
    cd src/frontend
    if npm run test --if-present; then
        print_success "Frontend tests passed!"
    else
        print_warning "Frontend tests failed or not configured"
    fi
    cd ../..
    
    # Rust tests
    print_status "Running Rust tests..."
    cd src-tauri
    if cargo test; then
        print_success "Rust tests passed!"
    else
        print_warning "Rust tests failed"
    fi
    cd ..
}

# Function to clean build artifacts
clean() {
    print_status "Cleaning build artifacts..."
    
    # Clean frontend
    rm -rf src/frontend/build
    rm -rf src/frontend/node_modules/.cache
    
    # Clean Rust
    cd src-tauri
    cargo clean
    cd ..
    
    print_success "Cleaned build artifacts!"
}

# Main script logic
case "${1:-help}" in
    "check")
        check_prerequisites
        ;;
    "install")
        check_prerequisites
        install_dependencies
        create_placeholder_icons
        ;;
    "dev")
        check_prerequisites
        run_dev
        ;;
    "build")
        check_prerequisites
        build_app
        ;;
    "test")
        check_prerequisites
        run_tests
        ;;
    "clean")
        clean
        ;;
    "setup")
        check_prerequisites
        install_dependencies
        create_placeholder_icons
        print_success "Setup complete! Run './scripts/dev-tauri.sh dev' to start development"
        ;;
    "help"|*)
        echo "AxieStudio Tauri Development Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  setup   - Complete setup (check, install, icons)"
        echo "  check   - Check prerequisites"
        echo "  install - Install dependencies"
        echo "  dev     - Start development server"
        echo "  build   - Build the application"
        echo "  test    - Run tests"
        echo "  clean   - Clean build artifacts"
        echo "  help    - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 setup   # First time setup"
        echo "  $0 dev     # Start development"
        echo "  $0 build   # Build for production"
        ;;
esac
