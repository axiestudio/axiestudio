# 🔒 Axie Studio Deployment & Credentials Guide

## 🎯 **CREDENTIALS SECURITY**

### ✅ **What's Safe in GitHub:**
- ✅ `.env.example` - Template with placeholders
- ✅ `RAILWAY_SUPABASE_DEPLOYMENT.md` - Instructions with placeholders
- ✅ Configuration files with `your-value-here` placeholders

### ❌ **What's NOT in GitHub:**
- ❌ `.env` - Your actual environment variables
- ❌ `.env.production` - Production credentials
- ❌ Any files with real passwords/API keys

---

## 🚀 **DEPLOYMENT STEPS**

### **Step 1: Set Up Local Environment**

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Fill in your credentials in `.env`:**
   ```bash
   # Your Supabase connection
   AXIESTUDIO_DATABASE_URL=postgresql://postgres.rsjmtwsvcfvabvqfcgeg:STEfanjohn!12@aws-1-eu-north-1.pooler.supabase.com:6543/postgres
   
   # Your admin credentials
   AXIESTUDIO_SUPERUSER=stefan@axiestudio.se
   AXIESTUDIO_SUPERUSER_PASSWORD=STEfanjohn!12
   
   # Generate secure keys (run: openssl rand -hex 32)
   AXIESTUDIO_SECRET_KEY=your-generated-secret-key
   AXIESTUDIO_JWT_SECRET=your-generated-jwt-secret
   ```

### **Step 2: Railway Deployment**

1. **Go to Railway Dashboard**
2. **Add these environment variables:**

```bash
AXIESTUDIO_DATABASE_URL=postgresql://postgres.rsjmtwsvcfvabvqfcgeg:STEfanjohn!12@aws-1-eu-north-1.pooler.supabase.com:6543/postgres
AXIESTUDIO_AUTO_LOGIN=false
AXIESTUDIO_NEW_USER_IS_ACTIVE=false
AXIESTUDIO_SECRET_KEY=your-generated-secret-key
AXIESTUDIO_JWT_SECRET=your-generated-jwt-secret
AXIESTUDIO_SUPERUSER=stefan@axiestudio.se
AXIESTUDIO_SUPERUSER_PASSWORD=STEfanjohn!12
AXIESTUDIO_HOST=0.0.0.0
AXIESTUDIO_PORT=7860
PORT=7860
AXIESTUDIO_WORKERS=1
AXIESTUDIO_CACHE_TYPE=simple
AXIESTUDIO_LOG_LEVEL=info
AXIESTUDIO_DEBUG=false
DO_NOT_TRACK=1
```

3. **Deploy** - Railway will automatically build and deploy

---

## 🔐 **SECURITY RECOMMENDATIONS**

### **1. Generate Secure Keys**
```bash
# Generate 32-character random keys
openssl rand -hex 32
```

### **2. Change Default Passwords**
- Change `STEfanjohn!12` to a stronger password
- Use a password manager to generate secure passwords

### **3. Environment-Specific Configs**
- **Development**: Use `.env` file
- **Production**: Use Railway environment variables
- **Never commit** real credentials to Git

---

## 🗄️ **DATABASE PERSISTENCE VERIFICATION**

After deployment, verify your data persists:

1. **Login to your Railway app**
2. **Create some test data** (flows, users, etc.)
3. **Trigger a redeploy** (push new code to GitHub)
4. **Check if data is still there** ✅

**Expected Result**: All data should persist across redeployments!

---

## 🔧 **TROUBLESHOOTING**

### **Database Connection Issues:**
```bash
# Check if your Supabase URL is correct
# Verify the password doesn't contain special characters that need encoding
# Ensure the pooler port (6543) is used for Railway
```

### **Authentication Issues:**
```bash
# Verify AXIESTUDIO_AUTO_LOGIN=false
# Check admin credentials are correct
# Ensure secret keys are set
```

### **Data Not Persisting:**
```bash
# Verify AXIESTUDIO_DATABASE_URL points to Supabase
# Check Railway environment variables are set
# Confirm not using SQLite in production
```

---

## 🎉 **SUCCESS INDICATORS**

✅ **Railway deployment successful**  
✅ **Login works with your admin credentials**  
✅ **Data persists across redeployments**  
✅ **Supabase dashboard shows your data**  
✅ **No credentials exposed in GitHub**  

Your Axie Studio is now production-ready with secure, persistent data storage! 🚀
