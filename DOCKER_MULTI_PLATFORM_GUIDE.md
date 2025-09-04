# 🐳 AxieStudio Multi-Platform Docker Guide

## 🚀 Overview

AxieStudio now supports **three different Docker deployment strategies** to meet various use cases:

1. **🏠 Fullstack** - Complete application in a single container
2. **🎯 Frontend-Only** - Standalone React frontend with nginx
3. **⚙️ Backend-Only** - API server for microservices architecture

## 📦 Available Docker Images

All images are built for **multi-platform support** (AMD64 + ARM64):

| Image | Description | Size | Use Case |
|-------|-------------|------|----------|
| `axiestudio/axiestudio-fullstack:latest` | Complete app with frontend + backend | ~2GB | Single-container deployment |
| `axiestudio/axiestudio-frontend:latest` | React frontend with nginx | ~100MB | Microservices, CDN deployment |
| `axiestudio/axiestudio-backend:latest` | Python API server only | ~1.5GB | Microservices, API-only deployment |

## 🎯 Deployment Scenarios

### 1. 🏠 Full-Stack Deployment (Recommended for beginners)

**Single container with everything included:**

```bash
# Quick start
docker run -p 7860:7860 axiestudio/axiestudio-fullstack:latest

# With persistent data
docker run -d \
  --name axiestudio \
  -p 7860:7860 \
  -v axiestudio_data:/app/data \
  axiestudio/axiestudio-fullstack:latest
```

**Access:** http://localhost:7860

### 2. 🎯 Microservices Deployment (Recommended for production)

**Separate frontend and backend containers:**

```bash
# Start backend
docker run -d \
  --name axiestudio-backend \
  -p 7860:7860 \
  axiestudio/axiestudio-backend:latest

# Start frontend
docker run -d \
  --name axiestudio-frontend \
  -p 80:80 \
  -e BACKEND_URL=http://localhost:7860 \
  axiestudio/axiestudio-frontend:latest
```

**Access:** 
- Frontend: http://localhost:80
- Backend API: http://localhost:7860

### 3. 🔧 Development Setup

**Using Docker Compose for complex setups:**

```bash
# Full-stack mode
docker-compose --profile fullstack up -d

# Microservices mode
docker-compose --profile microservices up -d

# Development mode with PostgreSQL
docker-compose --profile development up -d
```

## ⚙️ Configuration Options

### Frontend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | - | Backend API URL (required for frontend-only) |
| `FRONTEND_PORT` | `80` | Port for nginx to listen on |
| `AXIEFLOW_MAX_FILE_SIZE_UPLOAD` | `100` | Max file upload size in MB |

### Backend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AXIESTUDIO_HOST` | `0.0.0.0` | Host to bind the server |
| `AXIESTUDIO_PORT` | `7860` | Port for the API server |
| `AXIESTUDIO_DATABASE_URL` | `sqlite:///./axiestudio.db` | Database connection string |
| `AXIESTUDIO_CORS_ALLOW_ORIGINS` | `["*"]` | CORS allowed origins |

## 🔄 GitHub Actions Integration

The new **Multi-Platform Docker Build** workflow automatically builds all three image types when you push to the `master` branch.

### Workflow Features:
- ✅ **Multi-platform builds** (AMD64 + ARM64)
- ✅ **Automatic version tagging** from pyproject.toml
- ✅ **Selective builds** via manual trigger
- ✅ **Optimized caching** for faster builds
- ✅ **Health checks** and validation

### Manual Trigger Options:
```yaml
# Build all images
build_type: "all"

# Build specific image type
build_type: "fullstack" | "frontend" | "backend"
```

## 🏗️ Build Process

### Automated Builds (GitHub Actions)
- **Trigger:** Push to `master` branch
- **Platforms:** linux/amd64, linux/arm64
- **Registry:** Docker Hub
- **Workflow:** `.github/workflows/docker-swedish-backend.yml`

### Local Development Builds
```bash
# Build fullstack image
docker build -f docker/fullstack.Dockerfile -t axiestudio-fullstack .

# Build frontend-only image
docker build -f docker/frontend-only.Dockerfile -t axiestudio-frontend .

# Build backend-only image
docker build -f docker/backend-only.Dockerfile -t axiestudio-backend .
```

## 🔍 Health Checks

All images include built-in health checks:

```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"

# View health check logs
docker inspect --format='{{json .State.Health}}' axiestudio
```

## 📊 Performance Optimization

### Image Size Optimization:
- **Multi-stage builds** to reduce final image size
- **Layer caching** for faster rebuilds
- **Minimal base images** (Alpine/Slim variants)
- **Dependency optimization** with UV package manager

### Runtime Optimization:
- **Health checks** for container orchestration
- **Graceful shutdown** handling
- **Resource limits** configuration
- **Logging** to stdout/stderr for container logs

## 🚨 Troubleshooting

### Common Issues:

1. **Frontend can't connect to backend:**
   ```bash
   # Check BACKEND_URL environment variable
   docker logs axiestudio-frontend
   ```

2. **Database connection issues:**
   ```bash
   # Check database URL and connectivity
   docker logs axiestudio-backend
   ```

3. **Port conflicts:**
   ```bash
   # Use different ports
   docker run -p 8080:7860 axiestudio/axiestudio-fullstack:latest
   ```

### Debug Mode:
```bash
# Run with debug logging
docker run -e AXIESTUDIO_LOG_LEVEL=debug axiestudio/axiestudio-backend:latest
```

## 📚 Next Steps

1. **Choose your deployment strategy** based on your needs
2. **Configure environment variables** for your setup
3. **Set up monitoring** and logging
4. **Configure reverse proxy** (nginx/traefik) for production
5. **Set up SSL/TLS** certificates
6. **Configure backup strategy** for persistent data

## 🤝 Contributing

To contribute to the Docker setup:

1. **Test locally** with different configurations
2. **Update documentation** for new features
3. **Optimize Dockerfiles** for better performance
4. **Add new deployment scenarios** as needed

---

**🎉 Happy Deploying with AxieStudio!**
