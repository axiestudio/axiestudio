-- 🎯 NEON-COMPATIBLE SQL COMMANDS FOR EMAIL VERIFICATION
-- Copy and paste EACH command ONE BY ONE into your Neon SQL Editor
-- Do NOT copy the entire file at once - run each command separately!

-- ========================================
-- STEP 1: Add email verification columns
-- ========================================

-- Add email_verified column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;

-- Add email_verification_token column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR;

-- Add email_verification_expires column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_expires TIMESTAMP;

-- ========================================
-- STEP 2: Add 6-digit verification columns (Enterprise)
-- ========================================

-- Add verification_code column (6-digit codes)
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS verification_code VARCHAR(6);

-- Add verification_code_expires column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS verification_code_expires TIMESTAMP;

-- Add verification_attempts column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS verification_attempts INTEGER DEFAULT 0;

-- ========================================
-- STEP 3: Add security enhancement columns
-- ========================================

-- Add login_attempts column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS login_attempts INTEGER DEFAULT 0;

-- Add locked_until column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP;

-- Add last_login_ip column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS last_login_ip VARCHAR;

-- Add password_changed_at column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS password_changed_at TIMESTAMP;

-- Add failed_login_attempts column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0;

-- Add last_failed_login column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS last_failed_login TIMESTAMP;

-- ========================================
-- STEP 4: Set default values for existing users (NON-BREAKING)
-- ========================================

UPDATE "user" SET
    email_verified = COALESCE(email_verified, FALSE),
    verification_attempts = COALESCE(verification_attempts, 0),
    login_attempts = COALESCE(login_attempts, 0),
    failed_login_attempts = COALESCE(failed_login_attempts, 0)
WHERE email_verified IS NULL
   OR verification_attempts IS NULL
   OR login_attempts IS NULL
   OR failed_login_attempts IS NULL;

-- ========================================
-- STEP 5: Create indexes for performance
-- ========================================

-- Index for email verification token lookups
CREATE INDEX IF NOT EXISTS ix_user_email_verification_token ON "user" (email_verification_token);

-- Index for 6-digit verification code lookups
CREATE INDEX IF NOT EXISTS ix_user_verification_code ON "user" (verification_code);

-- ========================================
-- STEP 6: Verify everything worked
-- ========================================

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
