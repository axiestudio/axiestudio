# 📋 Complete SQL Commands Reference for AxieStudio

## 🎯 **Overview**

This document contains **ALL SQL commands** used by AxieStudio's automatic database creation system. These commands are executed automatically during application startup, but can also be run manually if needed.

---

## 🔧 **Email Verification System Commands**

### **Basic Email Verification Columns**
```sql
-- Add email verification status
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;

-- Add email verification token (for email links)
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR;

-- Add token expiration
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_expires TIMESTAMP;
```

### **6-Digit Verification Code System (Enterprise)**
```sql
-- Add 6-digit verification code
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS verification_code VARCHAR(6);

-- Add code expiration
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS verification_code_expires TIMESTAMP;

-- Add verification attempts counter (with NOT NULL constraint)
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS verification_attempts INTEGER DEFAULT 0 NOT NULL;
```

---

## 🔒 **Security Enhancement Commands**

### **Login Security Tracking**
```sql
-- Track login attempts
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS login_attempts INTEGER DEFAULT 0;

-- Account lockout timestamp
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP;

-- Track last login IP
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS last_login_ip VARCHAR;

-- Password change tracking
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS password_changed_at TIMESTAMP;

-- Failed login attempts
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0;

-- Last failed login timestamp
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS last_failed_login TIMESTAMP;
```

---

## 💳 **Subscription Management Commands**

### **Stripe Integration**
```sql
-- Stripe customer ID
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR;

-- Subscription status (trial, active, cancelled, etc.)
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_status VARCHAR DEFAULT 'trial';

-- Stripe subscription ID
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_id VARCHAR;
```

### **Trial and Subscription Tracking**
```sql
-- Trial period tracking
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS trial_start TIMESTAMP;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS trial_end TIMESTAMP;

-- Subscription period tracking
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_start TIMESTAMP;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_end TIMESTAMP;
```

---

## 🔧 **Schema Fix Commands**

### **Fix verification_attempts Column**
```sql
-- Update NULL values to 0
UPDATE "user" SET verification_attempts = 0 WHERE verification_attempts IS NULL;

-- Make column NOT NULL
ALTER TABLE "user" ALTER COLUMN verification_attempts SET NOT NULL;
```

### **Remove Problematic Indexes**
```sql
-- Remove email verification token index
DROP INDEX IF EXISTS ix_user_email_verification_token;

-- Remove verification code index
DROP INDEX IF EXISTS ix_user_verification_code;
```

### **Set Default Values for Existing Users**
```sql
-- Ensure all users have proper default values
UPDATE "user" SET
    email_verified = COALESCE(email_verified, FALSE),
    verification_attempts = COALESCE(verification_attempts, 0),
    login_attempts = COALESCE(login_attempts, 0),
    failed_login_attempts = COALESCE(failed_login_attempts, 0),
    subscription_status = COALESCE(subscription_status, 'trial')
WHERE email_verified IS NULL
   OR verification_attempts IS NULL
   OR login_attempts IS NULL
   OR failed_login_attempts IS NULL
   OR subscription_status IS NULL;
```

---

## 📊 **Verification and Status Commands**

### **Check Email Verification Columns**
```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user'
AND column_name IN (
    'email_verified', 'email_verification_token', 'email_verification_expires',
    'verification_code', 'verification_code_expires', 'verification_attempts',
    'login_attempts', 'locked_until', 'last_login_ip',
    'password_changed_at', 'failed_login_attempts', 'last_failed_login'
)
ORDER BY column_name;
```

### **Check All User Table Columns**
```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user'
ORDER BY ordinal_position;
```

### **Check Table Indexes**
```sql
SELECT indexname, indexdef
FROM pg_indexes 
WHERE tablename = 'user'
ORDER BY indexname;
```

### **Check User Data**
```sql
-- Check user verification status
SELECT 
    username,
    email,
    is_active,
    email_verified,
    verification_attempts,
    login_attempts,
    subscription_status,
    created_at
FROM "user"
ORDER BY created_at DESC
LIMIT 10;
```

---

## 🗄️ **Complete Table Creation Commands**

### **User Table (Complete)**
```sql
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR,
    password VARCHAR NOT NULL,
    profile_image VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    signup_ip VARCHAR,
    device_fingerprint VARCHAR,
    
    -- Email Verification
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR,
    email_verification_expires TIMESTAMP,
    
    -- 6-Digit Verification (Enterprise)
    verification_code VARCHAR(6),
    verification_code_expires TIMESTAMP,
    verification_attempts INTEGER DEFAULT 0 NOT NULL,
    
    -- Security Tracking
    login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    last_login_ip VARCHAR,
    password_changed_at TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    last_failed_login TIMESTAMP,
    
    -- Subscription Management
    stripe_customer_id VARCHAR,
    subscription_status VARCHAR DEFAULT 'trial',
    subscription_id VARCHAR,
    trial_start TIMESTAMP,
    trial_end TIMESTAMP,
    subscription_start TIMESTAMP,
    subscription_end TIMESTAMP,
    
    -- Additional Fields
    store_api_key VARCHAR,
    optins JSONB
);
```

---

## 🔍 **Database Health Check Commands**

### **Check Database Connection**
```sql
SELECT 1;
```

### **Check All Tables Exist**
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

### **Check Database Size**
```sql
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE tablename = 'user';
```

---

## 🚀 **Emergency Fix Commands**

### **Complete Emergency Fix (Run in Order)**
```sql
-- 1. Fix verification_attempts column
UPDATE "user" SET verification_attempts = 0 WHERE verification_attempts IS NULL;
ALTER TABLE "user" ALTER COLUMN verification_attempts SET NOT NULL;

-- 2. Remove problematic indexes
DROP INDEX IF EXISTS ix_user_email_verification_token;
DROP INDEX IF EXISTS ix_user_verification_code;

-- 3. Verify the fix
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user' AND column_name = 'verification_attempts';

-- 4. Check that indexes are removed
SELECT indexname 
FROM pg_indexes 
WHERE tablename = 'user' 
AND indexname IN ('ix_user_email_verification_token', 'ix_user_verification_code');
```

---

## 📝 **Notes**

- **All commands use `IF NOT EXISTS`** to prevent errors if columns already exist
- **Commands are idempotent** - safe to run multiple times
- **PostgreSQL syntax** - adjust for other databases if needed
- **Automatic execution** - These commands run automatically during app startup
- **Manual execution** - Can be run manually in database console if needed

**The automatic database system handles all of these commands during application startup!** 🎉
