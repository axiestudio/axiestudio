#!/bin/bash
# Axie Studio VPS Deployment Script
# Server: srv932265.hstgr.cloud (168.231.104.42)

set -e

DEPLOY_PATH="/opt/axiestudio"
SERVER_IP="168.231.104.42"

echo "🚀 Starting Axie Studio deployment..."
echo "📡 Server: $SERVER_IP"
echo "📁 Deploy Path: $DEPLOY_PATH"

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
    rm get-docker.sh
else
    echo "✅ Docker already installed"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "🔧 Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose already installed"
fi

# Install Git if not present
if ! command -v git &> /dev/null; then
    echo "📥 Installing Git..."
    apt install -y git
else
    echo "✅ Git already installed"
fi

# Create deployment directory
echo "📁 Setting up deployment directory..."
mkdir -p $DEPLOY_PATH
cd $DEPLOY_PATH

# Clone or update repository
if [ -d ".git" ]; then
    echo "📥 Updating existing repository..."
    git fetch origin
    git checkout main
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone https://github.com/axiestudio/axiestudio.git .
    git checkout main
fi

# Create production environment file
echo "⚙️ Creating production environment..."
cat > .env << 'EOF'
AXIESTUDIO_SECRET_KEY=production-secret-key-axiestudio-$(date +%s)
AXIESTUDIO_AUTO_LOGIN=false
AXIESTUDIO_NEW_USER_IS_ACTIVE=false
AXIESTUDIO_SUPERUSER=admin@axiestudio.se
AXIESTUDIO_SUPERUSER_PASSWORD=STEfanjohn-12
DATABASE_URL=sqlite:///./axiestudio.db
AXIESTUDIO_HOST=0.0.0.0
AXIESTUDIO_PORT=7860
AXIESTUDIO_LOG_LEVEL=INFO
AXIESTUDIO_WORKERS=1
AXIESTUDIO_CACHE_TYPE=simple
DO_NOT_TRACK=1
EOF

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Clean up old images (optional)
echo "🧹 Cleaning up old Docker images..."
docker system prune -f || true

# Build and start services
echo "🐳 Building and starting Axie Studio..."
docker-compose up -d --build

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Test if the application is responding
echo "🧪 Testing application health..."
if curl -f http://localhost:7860/health_check > /dev/null 2>&1; then
    echo "✅ Application is healthy!"
else
    echo "⚠️ Application may still be starting..."
fi

# Setup firewall (if ufw is available)
if command -v ufw &> /dev/null; then
    echo "🔥 Configuring firewall..."
    ufw allow 22/tcp
    ufw allow 7860/tcp
    ufw --force enable
fi

# Show final status
echo ""
echo "🎉 Deployment Complete!"
echo "================================"
echo "🌐 Access URL: http://$SERVER_IP:7860"
echo "👤 Username: admin@axiestudio.se"
echo "🔑 Password: STEfanjohn-12"
echo "📁 Deploy Path: $DEPLOY_PATH"
echo "================================"
echo ""
echo "📊 Container Status:"
docker-compose ps
echo ""
echo "📝 To view logs: docker-compose logs -f"
echo "🔄 To restart: docker-compose restart"
echo "🛑 To stop: docker-compose down"
echo ""
echo "✅ Axie Studio is now running!"
