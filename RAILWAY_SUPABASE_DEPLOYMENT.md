# 🚀 Railway + Supabase Deployment Guide

## 🎯 **PROBLEM SOLVED: PERSISTENT DATA STORAGE**

This guide fixes the issue where **data gets deleted on every Railway redeployment** by configuring persistent Supabase PostgreSQL storage.

## ❌ **PREVIOUS ISSUE:**
- Railway was using SQLite (`sqlite:///./axiestudio.db`)
- SQLite file stored in container (ephemeral storage)
- **Data lost on every redeploy** ❌

## ✅ **NEW SOLUTION:**
- Railway uses Supabase PostgreSQL (persistent storage)
- Data survives all redeployments ✅
- Professional production setup ✅

---

## 🔧 **RAILWAY CONFIGURATION**

### **Step 1: Update Environment Variables**

In your Railway project, **replace ALL environment variables** with these:

```bash
# 🗄️ PRIMARY SUPABASE DATABASE (PERSISTENT STORAGE)
AXIESTUDIO_DATABASE_URL=your-supabase-connection-string-here

# 🔄 BACKUP DATABASE OPTIONS (OPTIONAL)
# DATABASE_URL=postgresql://backup-connection-string-here
# SUPABASE_DATABASE_URL=postgresql://alternative-supabase-connection

# 🔐 AUTHENTICATION SETTINGS (SECURE)
AXIESTUDIO_AUTO_LOGIN=false
AXIESTUDIO_NEW_USER_IS_ACTIVE=false

# 🔒 SECURITY SETTINGS (CHANGE THESE!)
AXIESTUDIO_SECRET_KEY=your-production-secret-key-here
AXIESTUDIO_JWT_SECRET=your-production-jwt-secret-here

# 👤 ADMIN USER SETTINGS
AXIESTUDIO_SUPERUSER=your-admin-email-here
AXIESTUDIO_SUPERUSER_PASSWORD=your-admin-password-here

# 🌐 SERVER CONFIGURATION
AXIESTUDIO_HOST=0.0.0.0
AXIESTUDIO_PORT=7860
PORT=7860

# 📊 PERFORMANCE & LOGGING
AXIESTUDIO_WORKERS=1
AXIESTUDIO_CACHE_TYPE=simple
AXIESTUDIO_LOG_LEVEL=info
AXIESTUDIO_DEBUG=false

# 🔧 DATABASE HEALTH & MONITORING
AXIESTUDIO_DATABASE_HEALTH_CHECK=true
AXIESTUDIO_DATABASE_RETRY_ATTEMPTS=3
AXIESTUDIO_DATABASE_RETRY_DELAY=5

# 🔧 MISC SETTINGS
DO_NOT_TRACK=1
```

### **Step 2: Deploy**

1. **Commit and push** the updated code to GitHub
2. **Railway will auto-deploy** with the new environment variables
3. **Your data will now persist** across all future deployments! ✅

---

## 🗄️ **SUPABASE CONNECTION DETAILS**

**Your Supabase Database:**
- **Host**: `aws-1-eu-north-1.pooler.supabase.com`
- **Port**: `6543` (Transaction Pooler)
- **Database**: `postgres`
- **Username**: `postgres.rsjmtwsvcfvabvqfcgeg`
- **Password**: `STEfanjohn!12`

**Connection String:**
```
postgresql://postgres.rsjmtwsvcfvabvqfcgeg:STEfanjohn!12@aws-1-eu-north-1.pooler.supabase.com:6543/postgres
```

---

## ✅ **VERIFICATION**

After deployment, verify persistent storage:

1. **Login to your Railway app**
2. **Create some flows/data**
3. **Redeploy the app** (trigger a new deployment)
4. **Check if your data is still there** ✅

**Result**: Your data should persist across all redeployments!

---

## 🔒 **SECURITY NOTES**

**⚠️ IMPORTANT**: Change these in production:
- `AXIESTUDIO_SECRET_KEY` - Use a random 32+ character string
- `AXIESTUDIO_JWT_SECRET` - Use a different random 32+ character string
- Consider changing the admin password

**Generate secure keys:**
```bash
# Generate random secret keys
openssl rand -hex 32
```

---

## 🎉 **BENEFITS OF THIS SETUP**

✅ **Persistent Data** - Survives all redeployments  
✅ **Professional Database** - PostgreSQL instead of SQLite  
✅ **Scalable** - Supabase handles database scaling  
✅ **Reliable** - Supabase provides backups and monitoring  
✅ **Secure** - Enhanced authentication settings  

Your Axie Studio is now production-ready with persistent data storage! 🚀
