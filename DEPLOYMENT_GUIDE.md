# Axie Studio Deployment Guide

This guide covers deploying Axie Studio to various cloud platforms using our optimized Docker configuration.

## 🚀 Quick Deploy Options

### Railway (Recommended)
```bash
# 1. Fork this repository
# 2. Connect to Railway
# 3. Deploy automatically
```

### DigitalOcean App Platform
```bash
# 1. Connect your GitHub repository
# 2. Select Docker as build method
# 3. Set environment variables
```

### Render
```bash
# 1. Connect your GitHub repository
# 2. Select Docker as build method
# 3. Configure environment variables
```

## 🔧 Environment Variables

### Required Variables
```bash
AXIESTUDIO_SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
```

### Optional Variables
```bash
AXIESTUDIO_HOST=0.0.0.0
AXIESTUDIO_PORT=7860
AXIESTUDIO_LOG_LEVEL=INFO
AXIESTUDIO_AUTO_LOGIN=false
AXIESTUDIO_SUPERUSER=admin@example.com
AXIESTUDIO_SUPERUSER_PASSWORD=your-password
```

## 🐳 Docker Deployment

### Local Docker Build
```bash
# Build the image
docker build -t axiestudio .

# Run the container
docker run -p 7860:7860 \
  -e AXIESTUDIO_SECRET_KEY=your-secret-key \
  -e DATABASE_URL=sqlite:////app/data/axiestudio.db \
  axiestudio
```

### Docker Compose
```yaml
version: '3.8'
services:
  axiestudio:
    build: .
    ports:
      - "7860:7860"
    environment:
      - AXIESTUDIO_SECRET_KEY=your-secret-key
      - DATABASE_URL=sqlite:////app/data/axiestudio.db
    volumes:
      - axiestudio_data:/app/data
    restart: unless-stopped

volumes:
  axiestudio_data:
```

## 🌐 Platform-Specific Configurations

### Railway
- **Build Command**: Automatic (Docker)
- **Start Command**: `axiestudio run`
- **Health Check**: `/health_check`
- **Port**: `$PORT` (Railway sets this automatically)

### DigitalOcean App Platform
- **Build Command**: Automatic (Docker)
- **Run Command**: `axiestudio run`
- **HTTP Port**: `7860`
- **Health Check**: `/health_check`

### Render
- **Build Command**: Automatic (Docker)
- **Start Command**: `axiestudio run`
- **Health Check**: `/health_check`

### AWS ECS
- **Task Definition**: Use the Docker image
- **Port Mappings**: `7860:7860`
- **Environment Variables**: Set required variables
- **Health Check**: `/health_check`

### Google Cloud Run
- **Container**: Use the Docker image
- **Port**: `7860`
- **Environment Variables**: Set required variables
- **Health Check**: `/health_check`

## 🔒 Security Considerations

### Production Security
1. **Use Strong Secret Keys**: Generate a strong `AXIESTUDIO_SECRET_KEY`
2. **Database Security**: Use managed databases with SSL
3. **Network Security**: Use HTTPS in production
4. **Access Control**: Set up proper user authentication

### Environment Variables Security
```bash
# Generate a strong secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Use environment-specific configurations
AXIESTUDIO_ENVIRONMENT=production
AXIESTUDIO_LOG_LEVEL=WARNING
```

## 📊 Monitoring & Health Checks

### Health Check Endpoint
- **URL**: `/health_check`
- **Method**: `GET`
- **Expected Response**: `200 OK`

### Monitoring Setup
```bash
# Health check command
curl -f http://localhost:7860/health_check

# Log monitoring
docker logs axiestudio-container

# Resource monitoring
docker stats axiestudio-container
```

## 🗄️ Database Configuration

### SQLite (Default)
```bash
DATABASE_URL=sqlite:////app/data/axiestudio.db
```

### PostgreSQL
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

### MySQL
```bash
DATABASE_URL=mysql://user:password@host:port/database
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :7860
   
   # Kill the process or change port
   AXIESTUDIO_PORT=7861
   ```

2. **Database Connection Issues**
   ```bash
   # Check database URL format
   # Ensure database is accessible
   # Verify credentials
   ```

3. **Memory Issues**
   ```bash
   # Increase memory limits
   # Monitor resource usage
   # Optimize component usage
   ```

### Logs and Debugging
```bash
# View application logs
docker logs axiestudio-container

# Debug mode
AXIESTUDIO_LOG_LEVEL=DEBUG

# Access container shell
docker exec -it axiestudio-container /bin/bash
```

## 📈 Performance Optimization

### Resource Requirements
- **CPU**: Minimum 1 vCPU, Recommended 2+ vCPU
- **Memory**: Minimum 2GB RAM, Recommended 4GB+ RAM
- **Storage**: Minimum 10GB, Recommended 20GB+ for data

### Scaling Considerations
- **Horizontal Scaling**: Use load balancers
- **Vertical Scaling**: Increase resource allocation
- **Database Scaling**: Use managed databases
- **Caching**: Implement Redis for caching

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild Docker image
docker build -t axiestudio:latest .

# Update running container
docker-compose up -d --build
```

### Backup Strategy
```bash
# Database backup
docker exec axiestudio-container sqlite3 /app/data/axiestudio.db .dump > backup.sql

# Volume backup
docker run --rm -v axiestudio_data:/data -v $(pwd):/backup alpine tar czf /backup/axiestudio-backup.tar.gz /data
```

## 📞 Support

For deployment issues:
1. Check the logs: `docker logs axiestudio-container`
2. Verify environment variables
3. Test health check endpoint
4. Review this deployment guide
5. Check Axie Studio documentation

## 🎯 Best Practices

1. **Always use HTTPS in production**
2. **Set up proper monitoring and alerting**
3. **Regular backups of your data**
4. **Keep your deployment updated**
5. **Monitor resource usage**
6. **Use environment-specific configurations**
7. **Implement proper logging**
8. **Set up health checks**
9. **Use managed services when possible**
10. **Follow security best practices** 