# Railway Environment Variables

## Required Environment Variables for Axie Studio

Copy these to your Railway environment variables:

```
DATABASE_URL=sqlite:///./axiestudio.db
AXIESTUDIO_SECRET_KEY=your-secret-key-here-change-this
AXIESTUDIO_SUPERUSER=admin@axiestudio.se
AXIESTUDIO_SUPERUSER_PASSWORD=your-superuser-password
AXIESTUDIO_AUTO_LOGIN=true
AXIESTUDIO_NEW_USER_IS_ACTIVE=true
AXIESTUDIO_WORKERS=1
AXIESTUDIO_CACHE_TYPE=simple
AXIESTUDIO_LOG_LEVEL=info
PORT=7860
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