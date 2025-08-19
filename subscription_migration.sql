-- Complete User Migration for Neon PostgreSQL (Subscription + Email Verification)
-- Copy and paste each section separately into Neon SQL Editor

-- SECTION 1: Add subscription columns (safe to run multiple times)
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email VARCHAR;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_status VARCHAR DEFAULT 'trial';
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_id VARCHAR;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS trial_start TIMESTAMP;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS trial_end TIMESTAMP;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_start TIMESTAMP;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_end TIMESTAMP;

-- SECTION 2: Add email verification columns
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR;
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_expires TIMESTAMP;

-- SECTION 3: Create indexes
CREATE INDEX IF NOT EXISTS ix_user_email ON "user" (email);
CREATE INDEX IF NOT EXISTS ix_user_email_verification_token ON "user" (email_verification_token);

-- SECTION 4: Update existing users (mark as verified and set trial status)
UPDATE "user"
SET email_verified = TRUE,
    subscription_status = COALESCE(subscription_status, 'trial'),
    trial_start = COALESCE(trial_start, NOW())
WHERE email IS NOT NULL;

-- SECTION 5: Verify the migration worked
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user' AND table_schema = 'public'
AND column_name IN ('email', 'email_verified', 'email_verification_token', 'subscription_status')
ORDER BY ordinal_position;
