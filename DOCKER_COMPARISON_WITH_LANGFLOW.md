# Docker Deployment Comparison: Axie Studio vs Langflow

## 📊 Overview Comparison

| Aspect | Langflow | Axie Studio |
|--------|----------|-------------|
| **Docker Hub** | `langflowai/langflow` | `axiestudio/axiestudio` |
| **Base Image** | Python 3.12 + UV | Python 3.12 + UV |
| **Build System** | UV (modern) | UV (modern) |
| **Frontend** | React + Vite | React + Vite (Enhanced UI) |
| **Multi-platform** | ✅ linux/amd64, linux/arm64 | ✅ linux/amd64, linux/arm64 |
| **Backend-only** | ✅ | ✅ |
| **Size Optimization** | ✅ Multi-stage build | ✅ Multi-stage build |

## 🏗️ Dockerfile Comparison

### Langflow Dockerfile Structure
```dockerfile
# langflow/docker/build_and_push.Dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
# ... build dependencies
# Frontend build: cp -r build /app/src/backend/langflow/frontend
# Runtime: python:3.12.3-slim
ENV LANGFLOW_HOST=0.0.0.0
ENV LANGFLOW_PORT=7860
CMD ["langflow", "run"]
```

### Axie Studio Dockerfile Structure
```dockerfile
# axiestudio/docker/build_and_push.Dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
# ... build dependencies (identical to Langflow)
# Frontend build: cp -r build /app/src/backend/base/axiestudio/frontend
# Runtime: python:3.12.3-slim
ENV AXIESTUDIO_HOST=0.0.0.0
ENV AXIESTUDIO_PORT=7860
CMD ["axiestudio", "run"]
```

**Key Differences:**
- Frontend path: `langflow/frontend` → `axiestudio/frontend`
- Environment variables: `LANGFLOW_*` → `AXIESTUDIO_*`
- Command: `langflow run` → `axiestudio run`
- Labels: Updated for Axie Studio branding

## 📦 Image Variants

### Langflow Images
```bash
langflowai/langflow:latest              # Full application
langflowai/langflow:1.0.0              # Version tagged
langflowai/langflow-backend:latest      # Backend only
```

### Axie Studio Images
```bash
axiestudio/axiestudio:latest            # Full application
axiestudio/axiestudio:1.5.0            # Version tagged
axiestudio/axiestudio-backend:latest    # Backend only
```

## 🐳 Docker Compose Comparison

### Langflow docker-compose.yml
```yaml
services:
  langflow:
    image: langflowai/langflow:latest
    ports:
      - "7860:7860"
    environment:
      - LANGFLOW_DATABASE_URL=postgresql://langflow:langflow@postgres:5432/langflow
      - LANGFLOW_CONFIG_DIR=app/langflow
    volumes:
      - langflow-data:/app/langflow
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: langflow
      POSTGRES_PASSWORD: langflow
      POSTGRES_DB: langflow
```

### Axie Studio docker-compose.yml
```yaml
services:
  axiestudio:
    image: axiestudio/axiestudio:latest
    ports:
      - "7860:7860"
    environment:
      - DATABASE_URL=postgresql://axiestudio:axiestudio_password@postgres:5432/axiestudio
      - AXIESTUDIO_SECRET_KEY=change-this-secret-key-in-production
      - AXIESTUDIO_AUTO_LOGIN=false
    volumes:
      - axiestudio_data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/health_check"]
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: axiestudio
      POSTGRES_PASSWORD: axiestudio_password
      POSTGRES_DB: axiestudio
```

**Axie Studio Enhancements:**
- ✅ Health checks for better reliability
- ✅ Alpine PostgreSQL for smaller size
- ✅ Explicit secret key configuration
- ✅ Auto-login configuration
- ✅ Production-ready defaults

## 🚀 Deployment Scripts Comparison

### Langflow Build Process
```bash
# Manual process, no automated script provided
docker build -f docker/build_and_push.Dockerfile -t langflowai/langflow:latest .
docker push langflowai/langflow:latest
```

### Axie Studio Build Process
```powershell
# Automated PowerShell script
.\scripts\docker-hub-deploy.ps1 -AccessToken "your-token"

# Automated Bash script
./scripts/docker-hub-deploy.sh
```

**Axie Studio Advantages:**
- ✅ Automated build scripts for Windows & Linux
- ✅ Multi-platform builds (AMD64 + ARM64)
- ✅ Frontend build integration
- ✅ Error handling and validation
- ✅ Comprehensive logging

## 🔧 Configuration Comparison

### Environment Variables

| Variable | Langflow | Axie Studio |
|----------|----------|-------------|
| Host | `LANGFLOW_HOST` | `AXIESTUDIO_HOST` |
| Port | `LANGFLOW_PORT` | `AXIESTUDIO_PORT` |
| Database | `LANGFLOW_DATABASE_URL` | `DATABASE_URL` |
| Config Dir | `LANGFLOW_CONFIG_DIR` | `AXIESTUDIO_CONFIG_DIR` |
| Secret Key | `LANGFLOW_SECRET_KEY` | `AXIESTUDIO_SECRET_KEY` |
| Auto Login | `LANGFLOW_AUTO_LOGIN` | `AXIESTUDIO_AUTO_LOGIN` |
| Log Level | `LANGFLOW_LOG_LEVEL` | `AXIESTUDIO_LOG_LEVEL` |

### Database Support

| Database | Langflow | Axie Studio |
|----------|----------|-------------|
| SQLite | ✅ Default | ✅ Default |
| PostgreSQL | ✅ | ✅ |
| MySQL | ❌ | ✅ |

## 📈 Performance & Size

### Image Sizes (Estimated)
- **Langflow**: ~2.5GB (full), ~2.2GB (backend)
- **Axie Studio**: ~2.5GB (full), ~2.2GB (backend)

### Build Time
- **Langflow**: ~15-20 minutes (multi-platform)
- **Axie Studio**: ~15-20 minutes (multi-platform)

### Startup Time
- **Langflow**: ~30-45 seconds
- **Axie Studio**: ~30-45 seconds

## 🔐 Security Comparison

### Langflow Security
- Basic user authentication
- Default secret keys
- Standard Docker security

### Axie Studio Security Enhancements
- ✅ Configurable auto-login (disabled by default)
- ✅ Explicit secret key management
- ✅ Health check endpoints
- ✅ Production-ready defaults
- ✅ Enhanced error handling

## 🎯 Key Improvements in Axie Studio

### 1. **Enhanced UI/UX**
- Modern, clean design
- Removed GitHub/Discord references
- Professional branding
- Better error handling

### 2. **Better DevOps**
- Automated deployment scripts
- Comprehensive testing
- Multi-platform support
- Production-ready configurations

### 3. **Improved Documentation**
- Step-by-step deployment guides
- Troubleshooting sections
- Environment configuration examples
- Security best practices

### 4. **Enhanced Reliability**
- Health checks
- Better error handling
- Graceful degradation
- Monitoring capabilities

## 🚀 Migration from Langflow

### For Users
```bash
# Replace Langflow
docker stop langflow_container
docker run -p 7860:7860 axiestudio/axiestudio:latest

# Migrate data (if needed)
docker cp langflow_container:/app/langflow/data ./axiestudio_data
docker run -v ./axiestudio_data:/app/data axiestudio/axiestudio:latest
```

### For Developers
```bash
# Update docker-compose.yml
sed 's/langflowai\/langflow/axiestudio\/axiestudio/g' docker-compose.yml
sed 's/LANGFLOW_/AXIESTUDIO_/g' docker-compose.yml

# Update environment variables
AXIESTUDIO_HOST=0.0.0.0
AXIESTUDIO_PORT=7860
DATABASE_URL=postgresql://user:pass@host:5432/db
```

## 📋 Deployment Checklist

### Pre-deployment
- [ ] Docker Desktop installed and running
- [ ] Access to Docker Hub repository
- [ ] Frontend built and tested
- [ ] Environment variables configured
- [ ] Database setup (if using PostgreSQL)

### Deployment
- [ ] Run build tests: `.\scripts\test-docker-build.ps1`
- [ ] Deploy to Docker Hub: `.\scripts\docker-hub-deploy.ps1`
- [ ] Verify images on Docker Hub
- [ ] Test production deployment
- [ ] Monitor health checks

### Post-deployment
- [ ] Verify application functionality
- [ ] Check logs for errors
- [ ] Test user authentication
- [ ] Validate database connectivity
- [ ] Monitor performance metrics
