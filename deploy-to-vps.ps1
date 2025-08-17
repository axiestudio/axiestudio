# Axie Studio VPS Deployment Instructions
# Server: srv932265.hstgr.cloud (168.231.104.42)

Write-Host "🚀 Axie Studio VPS Deployment Guide" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "📡 Server IP: 168.231.104.42" -ForegroundColor Yellow
Write-Host "🌐 Server Name: srv932265.hstgr.cloud" -ForegroundColor Yellow
Write-Host "👤 Username: root" -ForegroundColor Yellow
Write-Host "🔑 Password: STEfanjohn-12" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔧 Deployment Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Copy deployment script to VPS:" -ForegroundColor White
Write-Host "   scp deploy-axiestudio.sh root@168.231.104.42:/tmp/" -ForegroundColor Gray
Write-Host ""
Write-Host "2. SSH to your VPS:" -ForegroundColor White
Write-Host "   ssh root@168.231.104.42" -ForegroundColor Gray
Write-Host "   # Enter password: STEfanjohn-12" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Run deployment script:" -ForegroundColor White
Write-Host "   chmod +x /tmp/deploy-axiestudio.sh" -ForegroundColor Gray
Write-Host "   /tmp/deploy-axiestudio.sh" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Access Axie Studio:" -ForegroundColor White
Write-Host "   http://168.231.104.42:7860" -ForegroundColor Gray
Write-Host "   Login: admin@axiestudio.se" -ForegroundColor Gray
Write-Host "   Password: STEfanjohn-12" -ForegroundColor Gray
Write-Host ""

Write-Host "Alternative - Direct Commands:" -ForegroundColor Cyan
Write-Host "If you prefer to run commands directly on the VPS:" -ForegroundColor White
Write-Host ""
Write-Host "# Update system and install Docker" -ForegroundColor Gray
Write-Host "apt update" -ForegroundColor Gray
Write-Host "apt upgrade -y" -ForegroundColor Gray
Write-Host "curl -fsSL https://get.docker.com -o get-docker.sh" -ForegroundColor Gray
Write-Host "sh get-docker.sh" -ForegroundColor Gray
Write-Host ""
Write-Host "# Clone repository" -ForegroundColor Gray
Write-Host "mkdir -p /opt/axiestudio" -ForegroundColor Gray
Write-Host "cd /opt/axiestudio" -ForegroundColor Gray
Write-Host "git clone https://github.com/axiestudio/axiestudio.git ." -ForegroundColor Gray
Write-Host ""
Write-Host "# Deploy with Docker" -ForegroundColor Gray
Write-Host "docker-compose up -d --build" -ForegroundColor Gray
Write-Host ""

Write-Host "Files ready for deployment!" -ForegroundColor Green
Write-Host "Deployment script: deploy-axiestudio.sh" -ForegroundColor Green
Write-Host "SSH config: .ssh/config" -ForegroundColor Green
