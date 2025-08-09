# Axie Studio Deployment Guide

## 🚀 **Production Deployment**

### **DigitalOcean App Platform Deployment**

1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/axiestudio-deployment.git
   cd axiestudio-deployment
   ```

2. **Environment Variables (Required)**
   Set these in your DigitalOcean App Platform:
   ```
   DATABASE_URL=sqlite:///./axiestudio.db
   AXIESTUDIO_SECRET_KEY=your-secret-key-here-change-this
   AXIESTUDIO_SUPERUSER=admin@axiestudio.se
   AXIESTUDIO_SUPERUSER_PASSWORD=your-superuser-password
   AXIESTUDIO_AUTO_LOGIN=false
   AXIESTUDIO_NEW_USER_IS_ACTIVE=true
   AXIESTUDIO_WORKERS=1
   AXIESTUDIO_CACHE_TYPE=simple
   AXIESTUDIO_LOG_LEVEL=info
   PORT=7860
   DO_NOT_TRACK=1
   ```

3. **Deploy to DigitalOcean App Platform**
   - Connect your GitHub repository
   - Select the `main` branch
   - Choose "Dockerfile" as build method
   - Set port to `7860`
   - Deploy!

### **Docker Deployment**

1. **Build Image**
   ```bash
   docker build -t axiestudio .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     --name axiestudio \
     -p 7860:7860 \
     -e DATABASE_URL=sqlite:///./axiestudio.db \
     -e AXIESTUDIO_SECRET_KEY=your-secret-key \
     -e AXIESTUDIO_SUPERUSER=admin@axiestudio.se \
     -e AXIESTUDIO_SUPERUSER_PASSWORD=your-password \
     axiestudio
   ```

### **Local Development**

1. **Backend Setup**
   ```bash
   cd src/backend/base
   uv sync
   axiestudio run
   ```

2. **Frontend Setup**
   ```bash
   cd src/frontend
   npm install
   npm run dev
   ```

## 🔧 **Configuration**

### **Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./axiestudio.db` |
| `AXIESTUDIO_SECRET_KEY` | Secret key for JWT tokens | Required |
| `AXIESTUDIO_SUPERUSER` | Admin email | Required |
| `AXIESTUDIO_SUPERUSER_PASSWORD` | Admin password | Required |
| `AXIESTUDIO_AUTO_LOGIN` | Enable auto-login | `false` |
| `AXIESTUDIO_NEW_USER_IS_ACTIVE` | Auto-activate new users | `true` |
| `AXIESTUDIO_WORKERS` | Number of workers | `1` |
| `AXIESTUDIO_CACHE_TYPE` | Cache type (simple/redis) | `simple` |
| `AXIESTUDIO_LOG_LEVEL` | Logging level | `info` |
| `PORT` | Server port | `7860` |

### **Database Options**

- **SQLite** (Default): `sqlite:///./axiestudio.db`
- **PostgreSQL**: `postgresql://user:password@localhost:5432/axiestudio`
- **MySQL**: `mysql://user:password@localhost:3306/axiestudio`

### **Caching Options**

- **Simple** (Default): In-memory caching
- **Redis**: `redis://localhost:6379/0`

## 🎯 **Features**

### **✅ Complete Langflow Functionality**
- **80+ Components**: All major AI/ML components
- **Flow Builder**: Visual workflow creation
- **API Integration**: RESTful API endpoints
- **User Management**: Authentication & authorization
- **Real-time Execution**: Live flow monitoring
- **Component Library**: Extensible component system

### **🔧 Custom Components**
- **OpenAI Integration**: GPT models, embeddings
- **Vector Stores**: Chroma, Pinecone, Weaviate
- **Document Loaders**: PDF, DOCX, CSV, JSON
- **Text Splitters**: Recursive, character-based
- **Tools**: Web search, file operations
- **Chains**: LLM chains, conversation chains

## **Troubleshooting**

### **Common Issues**

1. **Build Fails**
   - Check Node.js memory: Set `NODE_OPTIONS="--max-old-space-size=8192"`
   - Verify all dependencies are installed

2. **Frontend-Backend Communication**
   - Ensure `BACKEND_URL` is set correctly
   - Check proxy configuration in `vite.config.mts`

3. **Database Issues**
   - Verify `DATABASE_URL` format
   - Check database permissions

4. **Missing Dependencies**
   - Run `uv sync` in backend directory
   - Run `npm install` in frontend directory

### **Health Checks**
- **Backend**: `http://localhost:7860/health_check`
- **Frontend**: `http://localhost:3000`

## 📞 **Support**

For issues and questions:
- Check the logs: `docker logs axiestudio`
- Verify environment variables
- Test health endpoints
- Review deployment configuration

---

**Axie Studio** - Complete Langflow Alternative with Full AI/ML Workflow Capabilities 