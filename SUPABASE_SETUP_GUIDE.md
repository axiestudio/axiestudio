# 🗄️ Axie Studio + Supabase PostgreSQL Setup Guide

## ✅ **SUPABASE COMPATIBILITY CONFIRMED**

Your Supabase PostgreSQL database is **fully compatible** with Axie Studio:
- ✅ **Standard PostgreSQL** - No compatibility issues
- ✅ **Connection string format** - Standard postgres:// format
- ✅ **All Axie Studio features** - Migrations, users, flows, etc.
- ✅ **Already included** - `supabase==2.6.0` in dependencies

## 🔧 **CONFIGURATION SETUP**

### **1. Environment Variables**

Your Supabase connection string:
```bash
postgresql://postgres:STEfanjohn!12@db.ompjkiiabyuegytncbwq.supabase.co:5432/postgres
```

**Key Components:**
- **Host:** `db.ompjkiiabyuegytncbwq.supabase.co`
- **Port:** `5432` (standard PostgreSQL)
- **Database:** `postgres`
- **Username:** `postgres`
- **Password:** `STEfanjohn!12`
- **Project ID:** `ompjkiiabyuegytncbwq`

### **2. Local Development (.env)**

Use the `.env` file created for local development:
```bash
AXIESTUDIO_DATABASE_URL="postgresql://postgres:STEfanjohn!12@db.ompjkiiabyuegytncbwq.supabase.co:5432/postgres"
AXIESTUDIO_AUTO_LOGIN=false
```

### **3. Docker Deployment**

Use the `docker-compose.supabase.yml` file:
```bash
# Start with Supabase
docker-compose -f docker-compose.supabase.yml up -d

# Or use the deployment script
./deploy-supabase.sh
```

## 🚀 **DEPLOYMENT OPTIONS**

### **Option 1: Docker Compose (Recommended)**
```bash
# Pull latest image
docker pull axiestudio/axiestudio:latest

# Start with Supabase
docker-compose -f docker-compose.supabase.yml up -d

# Check logs
docker-compose -f docker-compose.supabase.yml logs -f
```

### **Option 2: Direct Docker Run**
```bash
docker run -d \
  --name axiestudio \
  -p 7860:7860 \
  -e AXIESTUDIO_DATABASE_URL="postgresql://postgres:STEfanjohn!12@db.ompjkiiabyuegytncbwq.supabase.co:5432/postgres" \
  -e AXIESTUDIO_AUTO_LOGIN=false \
  -e AXIESTUDIO_HOST=0.0.0.0 \
  -e AXIESTUDIO_PORT=7860 \
  axiestudio/axiestudio:latest
```

### **Option 3: VPS Deployment**
```bash
# On your VPS
git pull origin main
docker pull axiestudio/axiestudio:latest
docker-compose -f docker-compose.supabase.yml up -d
```

## 🔐 **SECURITY CONSIDERATIONS**

### **1. Database Security**
- ✅ **SSL Connection** - Supabase enforces SSL by default
- ✅ **Network Security** - Supabase handles network security
- ✅ **Access Control** - Configure in Supabase dashboard

### **2. Environment Variables**
```bash
# Production secrets (change these!)
AXIESTUDIO_SECRET_KEY=your-production-secret-key
AXIESTUDIO_JWT_SECRET=your-production-jwt-secret
```

### **3. Supabase Dashboard Access**
- **URL:** https://supabase.com/dashboard/project/ompjkiiabyuegytncbwq
- **Database:** SQL Editor for direct database access
- **Auth:** User management (if using Supabase Auth)

## 📊 **DATABASE FEATURES**

### **What Axie Studio Will Store:**
- ✅ **User accounts** and authentication
- ✅ **Flow definitions** and configurations
- ✅ **Component settings** and customizations
- ✅ **Chat history** and conversations
- ✅ **API keys** and integrations
- ✅ **File uploads** and metadata

### **Supabase Advantages:**
- 🚀 **Managed service** - No database maintenance
- 📈 **Scalable** - Automatic scaling
- 🔄 **Backups** - Automatic daily backups
- 📊 **Monitoring** - Built-in performance monitoring
- 🌍 **Global** - Edge locations worldwide

## 🧪 **TESTING THE CONNECTION**

### **1. Test Database Connection**
```bash
# Using psql (if available)
psql "postgresql://postgres:STEfanjohn!12@db.ompjkiiabyuegytncbwq.supabase.co:5432/postgres"

# Using Python
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://postgres:STEfanjohn!12@db.ompjkiiabyuegytncbwq.supabase.co:5432/postgres')
print('✅ Connection successful!')
conn.close()
"
```

### **2. Verify Axie Studio Connection**
```bash
# Check logs for successful database connection
docker-compose -f docker-compose.supabase.yml logs | grep -i database
```

## 🎯 **EXPECTED BEHAVIOR**

### **First Startup:**
1. **Database Migration** - Axie Studio will create necessary tables
2. **User Creation** - Admin user will be created
3. **Component Loading** - All 83 AI components will be available
4. **Ready State** - Application accessible at http://localhost:7860

### **Ongoing Operation:**
- ✅ **Persistent Data** - All data stored in Supabase
- ✅ **Multi-Instance** - Can run multiple Axie Studio instances
- ✅ **Backup Safety** - Supabase handles backups automatically

## 🔧 **TROUBLESHOOTING**

### **Connection Issues:**
```bash
# Check if Supabase is accessible
curl -I https://db.ompjkiiabyuegytncbwq.supabase.co

# Verify environment variables
docker-compose -f docker-compose.supabase.yml config
```

### **Migration Issues:**
```bash
# Check migration logs
docker-compose -f docker-compose.supabase.yml logs | grep -i migration
```

## 🎉 **READY TO DEPLOY!**

Your Supabase PostgreSQL configuration is ready! Use any of the deployment methods above to start Axie Studio with your Supabase database.

**Status: 🟢 CONFIGURED AND READY** 🚀
