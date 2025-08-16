# Railway Environment Variables

## Required Environment Variables for Axie Studio

Copy these to your Railway environment variables:

```
# 🗄️ SUPABASE DATABASE (PERSISTENT STORAGE)
AXIESTUDIO_DATABASE_URL=your-supabase-connection-string-here

# 🔐 AUTHENTICATION SETTINGS
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

# 🔧 MISC SETTINGS
DO_NOT_TRACK=1
```

## Railway Setup Steps:

1. **Go to railway.app** and sign up/login
2. **Create new project**
3. **Connect GitHub repository**: `sadfsjg/axiestudio-lang`
4. **Add environment variables** (copy from above)
5. **Deploy!**

## Database Options:

**Option 1: SQLite (Free)**
- Use `DATABASE_URL=sqlite:///./axiestudio.db`
- Data stored locally in the app

**Option 2: Railway PostgreSQL (Recommended)**
- Add PostgreSQL service in Railway
- Railway will provide `DATABASE_URL` automatically
- Better for production use 