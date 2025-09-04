#!/bin/bash

# Axie Studio Docker Hub Deployment Script
# This script builds and pushes Axie Studio Docker images to Docker Hub

set -e

# Configuration
DOCKER_HUB_USERNAME="${DOCKER_HUB_USERNAME:-axiestudio}"
IMAGE_NAME="axiestudio"
VERSION=$(grep "^version" pyproject.toml | sed 's/.*"\(.*\)"$/\1/')
PLATFORMS="linux/amd64,linux/arm64"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AXIE STUDIO DOCKER HUB DEPLOYMENT${NC}"
echo -e "${BLUE}====================================${NC}"
echo -e "${YELLOW}Version: ${VERSION}${NC}"
echo -e "${YELLOW}Platforms: ${PLATFORMS}${NC}"
echo -e "${YELLOW}Docker Hub: ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if logged into Docker Hub
if ! docker info | grep -q "Username"; then
    echo -e "${YELLOW}⚠️  Not logged into Docker Hub. Please run: docker login${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build frontend first
echo -e "${BLUE}📦 Building frontend...${NC}"
cd src/frontend
npm ci
npm run build
cd ../..

# Copy frontend to backend
echo -e "${BLUE}📋 Copying frontend to backend...${NC}"
rm -rf src/backend/base/axiestudio/frontend
cp -r src/frontend/build src/backend/base/axiestudio/frontend

# Build multi-platform images
echo -e "${BLUE}🏗️  Building multi-platform Docker images...${NC}"

# Create and use buildx builder if it doesn't exist
if ! docker buildx ls | grep -q "axiestudio-builder"; then
    echo -e "${YELLOW}Creating buildx builder...${NC}"
    docker buildx create --name axiestudio-builder --use
    docker buildx inspect --bootstrap
fi

# Build and push main image
echo -e "${BLUE}🐳 Building and pushing main image...${NC}"
docker buildx build \
    --platform ${PLATFORMS} \
    --file docker/build_and_push.Dockerfile \
    --tag ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION} \
    --tag ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest \
    --push \
    .

# Build and push backend-only image
echo -e "${BLUE}🔧 Building and pushing backend-only image...${NC}"
docker buildx build \
    --platform ${PLATFORMS} \
    --file docker/build_and_push_backend.Dockerfile \
    --build-arg AXIESTUDIO_IMAGE=${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION} \
    --tag ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}-backend:${VERSION} \
    --tag ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}-backend:latest \
    --push \
    .

echo -e "${GREEN}✅ Successfully deployed to Docker Hub!${NC}"
echo -e "${GREEN}📦 Images available:${NC}"
echo -e "   • ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}"
echo -e "   • ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest"
echo -e "   • ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}-backend:${VERSION}"
echo -e "   • ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}-backend:latest"
echo ""
echo -e "${BLUE}🚀 To run the image:${NC}"
echo -e "   docker run -p 7860:7860 ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest"
echo ""
echo -e "${BLUE}📖 To use with docker-compose:${NC}"
echo -e "   Update docker-compose.yml to use: ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest"
