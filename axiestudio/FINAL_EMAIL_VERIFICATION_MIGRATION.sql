-- FINAL EMAIL VERIFICATION MIGRATION FOR AXIE STUDIO
-- Copy and paste EACH COMMAND ONE BY ONE into your Neon SQL Editor
-- Do NOT copy the whole file at once - run each command separately!

-- ========================================
-- STEP 1: Add email verification columns
-- ========================================

ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;

-- ========================================
-- STEP 2: Add verification token column
-- ========================================

ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR;

-- ========================================
-- STEP 3: Add token expiry column
-- ========================================

ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_expires TIMESTAMP;

-- ========================================
-- STEP 4: Mark existing users as verified (NON-BREAKING)
-- ========================================

UPDATE "user" SET email_verified = TRUE WHERE email IS NOT NULL;

-- ========================================
-- STEP 5: Create index for fast token lookups
-- ========================================

CREATE INDEX IF NOT EXISTS ix_user_email_verification_token ON "user" (email_verification_token);

-- ========================================
-- STEP 6: Verify everything worked
-- ========================================

SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user' AND table_schema = 'public'
AND column_name IN ('email_verified', 'email_verification_token', 'email_verification_expires')
ORDER BY ordinal_position;
