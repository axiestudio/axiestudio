-- Email Verification Migration for Axie Studio
-- Copy and paste EACH COMMAND ONE BY ONE into Neon SQL Editor

-- Command 1: Add email_verified column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;

-- Command 2: Add email_verification_token column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR;

-- Command 3: Add email_verification_expires column
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verification_expires TIMESTAMP;

-- Command 4: Mark existing users as verified (non-breaking change)
UPDATE "user" SET email_verified = TRUE WHERE email IS NOT NULL;

-- Command 5: Create index for verification token lookups
CREATE INDEX IF NOT EXISTS ix_user_email_verification_token ON "user" (email_verification_token);

-- Command 6: Verify the migration worked
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user' AND table_schema = 'public'
AND column_name IN ('email_verified', 'email_verification_token', 'email_verification_expires')
ORDER BY ordinal_position;
