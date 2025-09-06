# 🔧 Axie Studio Setup Configuration Guide

## 🚨 IMPORTANT: Security Configuration Required

Before running the setup script, you **MUST** configure your credentials properly to avoid security issues.

## 📋 Configuration Steps

### 1. Environment Variables Setup

Copy the example environment file and configure it:
```bash
cp .env.example .env
```

Edit `.env` file with your actual credentials:

```bash
# Database Configuration
AXIESTUDIO_DATABASE_URL=your_actual_database_url_here

# Superuser Configuration  
AXIESTUDIO_SUPERUSER=your_admin_email@yourdomain.com
AXIESTUDIO_SUPERUSER_PASSWORD=your_secure_admin_password

# Email Configuration
AXIESTUDIO_EMAIL_FROM_EMAIL=noreply@yourdomain.com
AXIESTUDIO_EMAIL_FROM_NAME=Your App Name
AXIESTUDIO_EMAIL_SMTP_HOST=smtp.resend.com
AXIESTUDIO_EMAIL_SMTP_PASSWORD=your_actual_smtp_password

# Stripe Configuration
STRIPE_PRICE_ID=your_actual_stripe_price_id
STRIPE_PUBLISHABLE_KEY=your_actual_stripe_publishable_key
STRIPE_SECRET_KEY=your_actual_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_actual_stripe_webhook_secret

# Application Settings
AXIESTUDIO_SECRET_KEY=your_unique_secret_key_here
FRONTEND_URL=https://yourdomain.com/
```

### 2. Setup Script Configuration

The `setup_and_run.py` script contains placeholder values that need to be replaced with your actual credentials.

**⚠️ DO NOT commit real credentials to git!**

### 3. Security Best Practices

1. **Never commit `.env` files** - They are already in `.gitignore`
2. **Use strong passwords** for superuser accounts
3. **Use environment-specific keys** (test keys for development, live keys for production)
4. **Rotate secrets regularly** especially in production
5. **Use secure secret management** in production environments

### 4. Running the Setup

After configuring your credentials:

```bash
python setup_and_run.py
```

This will:
- ✅ Set up system paths
- ✅ Configure environment variables
- ✅ Initialize Visual Studio Build Tools
- ✅ Launch the Swedish Axie Studio application
- ✅ Start all services with trial protection

### 5. Production Deployment

For production deployment:
1. Use a proper secret management system
2. Set environment variables through your hosting platform
3. Never hardcode credentials in scripts
4. Use SSL/TLS for all connections
5. Enable proper logging and monitoring

## 🛡️ Security Features Included

- ✅ Trial protection middleware
- ✅ Account lockout protection
- ✅ Email verification system
- ✅ Device fingerprinting
- ✅ Abuse prevention
- ✅ Swedish localization
- ✅ Comprehensive logging

## 🇸🇪 Swedish App Features

- Trial expiration handling with HTTP 402 redirects
- Swedish error messages throughout
- Pricing page redirection for expired users
- Email verification in Swedish
- Complete Swedish UI localization

## 📞 Support

If you encounter issues:
1. Check your environment variables are correctly set
2. Verify database connectivity
3. Ensure all required services are running
4. Check logs for detailed error information

---

**Remember: Security is paramount. Never expose credentials in your codebase!**
