# 🚀 Railway Deployment Guide for Axie Studio with Stripe

This guide will help you deploy Axie Studio with Stripe subscription functionality to Railway.

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Stripe Account**: Get your API keys from [stripe.com](https://stripe.com)
3. **GitHub Repository**: Your code should be in a GitHub repository

## 🔧 Step 1: Prepare Your Stripe Configuration

### 1.1 Get Stripe API Keys
1. Go to your Stripe Dashboard
2. Navigate to **Developers > API Keys**
3. Copy your:
   - **Publishable key** (starts with `pk_`)
   - **Secret key** (starts with `sk_`)

### 1.2 Create Your Product and Price
1. Go to **Products** in Stripe Dashboard
2. Create a new product: "Pro Subscription"
3. Set price: $45.00 USD, recurring monthly
4. Copy the **Price ID** (starts with `price_`)

### 1.3 Set Up Webhook
1. Go to **Developers > Webhooks**
2. Click **Add endpoint**
3. Set endpoint URL: `https://your-app-name.railway.app/api/v1/subscriptions/webhook`
4. Select these events:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
5. Copy the **Webhook Secret** (starts with `whsec_`)

## 🚂 Step 2: Deploy to Railway

### 2.1 Create New Project
1. Go to [railway.app](https://railway.app)
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Choose your repository

### 2.2 Add PostgreSQL Database
1. In your Railway project, click **New**
2. Select **Database > PostgreSQL**
3. Railway will automatically create a database and provide connection details

### 2.3 Configure Environment Variables
In your Railway project settings, add these environment variables:

```env
# Axie Studio Configuration
AXIESTUDIO_AUTO_LOGIN=false
AXIESTUDIO_DEBUG=false
AXIESTUDIO_HOST=0.0.0.0
AXIESTUDIO_PORT=7860
AXIESTUDIO_JWT_SECRET=your-secure-jwt-secret-here
AXIESTUDIO_SECRET_KEY=your-secure-secret-key-here
AXIESTUDIO_NEW_USER_IS_ACTIVE=true
AXIESTUDIO_SUPERUSER=your-admin-email@domain.com
AXIESTUDIO_SUPERUSER_PASSWORD=your-secure-admin-password

# Database (Railway will auto-populate this)
AXIESTUDIO_DATABASE_URL=${{Postgres.DATABASE_URL}}

# Stripe Configuration (Replace with your actual keys)
STRIPE_SECRET_KEY=sk_live_your_actual_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_actual_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_actual_webhook_secret
STRIPE_PRICE_ID=price_your_actual_price_id

# Railway Configuration
FRONTEND_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
RAILWAY_ENVIRONMENT=production

# Optional
DO_NOT_TRACK=1
```

### 2.4 Update Webhook URL
After deployment, update your Stripe webhook URL to use your actual Railway domain:
`https://your-actual-app-name.railway.app/api/v1/subscriptions/webhook`

## 🔄 Step 3: Database Migration

The database migration will run automatically when the app starts, but you can also run it manually:

1. Connect to your Railway project terminal
2. Run: `python src/backend/base/axiestudio/migrations/add_subscription_fields.py`

## ✅ Step 4: Verify Deployment

### 4.1 Check Application Health
Visit: `https://your-app-name.railway.app/health_check`

### 4.2 Test Subscription Flow
1. Go to: `https://your-app-name.railway.app/signup`
2. Create a new account
3. You should be redirected to the pricing page
4. Test the subscription flow

### 4.3 Verify Webhook
1. Create a test subscription
2. Check Railway logs for webhook events
3. Verify user subscription status updates

## 🛠️ Step 5: Production Checklist

- [ ] Use live Stripe keys (not test keys)
- [ ] Set strong JWT and secret keys
- [ ] Configure proper admin credentials
- [ ] Test the complete user flow
- [ ] Monitor Railway logs for errors
- [ ] Set up Stripe webhook monitoring
- [ ] Test trial expiration logic

## 🔍 Troubleshooting

### Common Issues:

1. **Stripe not configured error**
   - Check environment variables are set correctly
   - Verify Stripe keys are valid

2. **Database connection issues**
   - Ensure `AXIESTUDIO_DATABASE_URL` is set to `${{Postgres.DATABASE_URL}}`
   - Check PostgreSQL service is running

3. **Webhook failures**
   - Verify webhook URL is correct
   - Check webhook secret matches
   - Monitor Railway logs for webhook errors

4. **Frontend not loading**
   - Check build logs in Railway
   - Verify static files are being served correctly

### Logs and Monitoring:
- Railway provides real-time logs in the dashboard
- Monitor Stripe webhook delivery in Stripe Dashboard
- Check application health at `/health_check` endpoint

## 🎯 Features Included

✅ **7-day free trial** for all new users  
✅ **Single Pro plan** at $45/month  
✅ **Automatic trial expiration** and account cleanup  
✅ **Stripe Customer Portal** for subscription management  
✅ **Webhook handling** for real-time subscription updates  
✅ **Trial status tracking** with days remaining  
✅ **Clean, responsive UI** for pricing and subscription management  

## 📞 Support

If you encounter issues:
1. Check Railway deployment logs
2. Verify Stripe webhook delivery
3. Test with Stripe test mode first
4. Monitor application health endpoint

Your Axie Studio with Stripe subscriptions is now ready for production! 🎉
