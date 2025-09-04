#!/bin/bash

# 🚀 Axie Studio Supabase Deployment Script
# ==========================================

echo "🚀 Starting Axie Studio deployment with Supabase PostgreSQL..."

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

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running ✅"

# Pull the latest Axie Studio image
print_status "Pulling latest Axie Studio image from Docker Hub..."
if docker pull axiestudio/axiestudio:latest; then
    print_success "Successfully pulled axiestudio/axiestudio:latest"
else
    print_error "Failed to pull Docker image. Check your internet connection."
    exit 1
fi

# Stop existing containers
print_status "Stopping existing Axie Studio containers..."
docker-compose -f docker-compose.supabase.yml down 2>/dev/null || true

# Test Supabase connection
print_status "Testing Supabase PostgreSQL connection..."
if docker run --rm axiestudio/axiestudio:latest python -c "
import psycopg2
try:
    conn = psycopg2.connect('postgresql://postgres:STEfanjohn!12@db.ompjkiiabyuegytncbwq.supabase.co:5432/postgres')
    conn.close()
    print('✅ Supabase connection successful')
except Exception as e:
    print(f'❌ Supabase connection failed: {e}')
    exit(1)
" 2>/dev/null; then
    print_success "Supabase PostgreSQL connection verified"
else
    print_warning "Could not verify Supabase connection (this might be normal if psycopg2 is not available in the image)"
fi

# Start Axie Studio with Supabase
print_status "Starting Axie Studio with Supabase PostgreSQL..."
if docker-compose -f docker-compose.supabase.yml up -d; then
    print_success "Axie Studio started successfully!"
else
    print_error "Failed to start Axie Studio"
    exit 1
fi

# Wait for service to be ready
print_status "Waiting for Axie Studio to be ready..."
sleep 10

# Check if service is healthy
for i in {1..12}; do
    if curl -f http://localhost:7860/health_check > /dev/null 2>&1; then
        print_success "Axie Studio is ready and healthy!"
        break
    else
        if [ $i -eq 12 ]; then
            print_error "Axie Studio failed to start properly"
            print_status "Checking logs..."
            docker-compose -f docker-compose.supabase.yml logs --tail=50
            exit 1
        fi
        print_status "Waiting for Axie Studio to start... ($i/12)"
        sleep 10
    fi
done

# Display deployment information
echo ""
echo "🎉 Axie Studio Deployment Complete!"
echo "=================================="
echo "🌐 Application URL: http://localhost:7860"
echo "🗄️ Database: Supabase PostgreSQL"
echo "🔐 Login Required: Yes (AUTO_LOGIN=false)"
echo "📊 Project: ompjkiiabyuegytncbwq.supabase.co"
echo ""
echo "📋 Useful Commands:"
echo "  View logs:    docker-compose -f docker-compose.supabase.yml logs -f"
echo "  Stop service: docker-compose -f docker-compose.supabase.yml down"
echo "  Restart:      docker-compose -f docker-compose.supabase.yml restart"
echo ""
print_success "Deployment completed successfully! 🚀"
