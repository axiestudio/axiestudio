-- 🔧 FINAL DATABASE FIX FOR AXIESTUDIO
-- Copy and paste EACH COMMAND ONE BY ONE into your Neon SQL Editor
-- Do NOT copy the entire file at once - run each command separately!

-- ========================================
-- STEP 1: Fix verification_attempts column (make NOT NULL)
-- ========================================

-- First, ensure all NULL values are set to 0
UPDATE "user" SET verification_attempts = 0 WHERE verification_attempts IS NULL;

-- Then make the column NOT NULL
ALTER TABLE "user" ALTER COLUMN verification_attempts SET NOT NULL;

-- ========================================
-- STEP 2: Remove problematic indexes
-- ========================================

-- Remove the email verification token index
DROP INDEX IF EXISTS ix_user_email_verification_token;

-- Remove the verification code index  
DROP INDEX IF EXISTS ix_user_verification_code;

-- ========================================
-- STEP 3: Verify the fix worked
-- ========================================

-- Check verification_attempts column
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user' AND column_name = 'verification_attempts';

-- Check that indexes are removed
SELECT indexname 
FROM pg_indexes 
WHERE tablename = 'user' 
AND indexname IN ('ix_user_email_verification_token', 'ix_user_verification_code');

-- ========================================
-- STEP 4: Final verification of all columns
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
