#!/bin/bash

# AxieStudio Docker Build Test Script
# This script tests all three Docker builds locally

set -e

echo "🐳 AxieStudio Docker Build Test Script"
echo "======================================"

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

# Function to test Docker build
test_build() {
    local dockerfile=$1
    local tag=$2
    local description=$3
    
    print_status "Testing $description..."
    print_status "Dockerfile: $dockerfile"
    print_status "Tag: $tag"
    
    if docker build -f "$dockerfile" -t "$tag" . --no-cache; then
        print_success "$description build completed successfully!"
        
        # Test if image was created
        if docker images | grep -q "$tag"; then
            print_success "Image $tag created successfully"
            
            # Get image size
            size=$(docker images --format "table {{.Size}}" "$tag" | tail -n 1)
            print_status "Image size: $size"
        else
            print_error "Image $tag not found after build"
            return 1
        fi
    else
        print_error "$description build failed!"
        return 1
    fi
    
    echo ""
}

# Function to test container startup
test_container() {
    local image=$1
    local container_name=$2
    local port=$3
    local description=$4
    
    print_status "Testing $description container startup..."
    
    # Remove existing container if it exists
    docker rm -f "$container_name" 2>/dev/null || true
    
    # Start container in detached mode
    if docker run -d --name "$container_name" -p "$port" "$image"; then
        print_success "Container $container_name started successfully"
        
        # Wait a bit for startup
        sleep 10
        
        # Check if container is still running
        if docker ps | grep -q "$container_name"; then
            print_success "Container $container_name is running"
            
            # Show container logs (last 10 lines)
            print_status "Container logs (last 10 lines):"
            docker logs --tail 10 "$container_name"
        else
            print_error "Container $container_name stopped unexpectedly"
            print_status "Container logs:"
            docker logs "$container_name"
            return 1
        fi
        
        # Clean up
        docker stop "$container_name" >/dev/null 2>&1
        docker rm "$container_name" >/dev/null 2>&1
        print_status "Container $container_name cleaned up"
    else
        print_error "Failed to start container $container_name"
        return 1
    fi
    
    echo ""
}

# Main test execution
main() {
    print_status "Starting Docker build tests..."
    echo ""
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    # Test 1: Backend-only build
    print_status "=== Test 1: Backend-Only Build ==="
    if test_build "docker/backend-only.Dockerfile" "axiestudio-backend-test" "Backend-Only"; then
        test_container "axiestudio-backend-test" "test-backend" "7860:7860" "Backend-Only"
    fi
    
    # Test 2: Frontend-only build
    print_status "=== Test 2: Frontend-Only Build ==="
    if test_build "docker/frontend-only.Dockerfile" "axiestudio-frontend-test" "Frontend-Only"; then
        test_container "axiestudio-frontend-test" "test-frontend" "8080:80" "Frontend-Only"
    fi
    
    # Test 3: Fullstack build
    print_status "=== Test 3: Fullstack Build ==="
    if test_build "docker/fullstack.Dockerfile" "axiestudio-fullstack-test" "Fullstack"; then
        test_container "axiestudio-fullstack-test" "test-fullstack" "7861:7860" "Fullstack"
    fi
    
    # Summary
    echo ""
    print_success "=== Build Test Summary ==="
    print_status "All Docker builds completed!"
    print_status "Images created:"
    docker images | grep "axiestudio.*test"
    
    # Cleanup test images
    print_status "Cleaning up test images..."
    docker rmi axiestudio-backend-test axiestudio-frontend-test axiestudio-fullstack-test 2>/dev/null || true
    
    print_success "🎉 All tests completed successfully!"
}

# Run main function
main "$@"
