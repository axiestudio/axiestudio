-- 🎯 SINGLE NEON-COMPATIBLE SQL COMMAND FOR EMAIL VERIFICATION
-- Copy and paste this ENTIRE command into your Neon SQL Editor as ONE command

DO $$
BEGIN
    -- Add email_verified column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'email_verified') THEN
        ALTER TABLE "user" ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;
        RAISE NOTICE '✅ Added email_verified column';
    ELSE
        RAISE NOTICE '⏭️ email_verified column already exists';
    END IF;

    -- Add email_verification_token column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'email_verification_token') THEN
        ALTER TABLE "user" ADD COLUMN email_verification_token VARCHAR;
        RAISE NOTICE '✅ Added email_verification_token column';
    ELSE
        RAISE NOTICE '⏭️ email_verification_token column already exists';
    END IF;

    -- Add email_verification_expires column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'email_verification_expires') THEN
        ALTER TABLE "user" ADD COLUMN email_verification_expires TIMESTAMP;
        RAISE NOTICE '✅ Added email_verification_expires column';
    ELSE
        RAISE NOTICE '⏭️ email_verification_expires column already exists';
    END IF;

    -- Add verification_code column (6-digit enterprise codes)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'verification_code') THEN
        ALTER TABLE "user" ADD COLUMN verification_code VARCHAR(6);
        RAISE NOTICE '✅ Added verification_code column';
    ELSE
        RAISE NOTICE '⏭️ verification_code column already exists';
    END IF;

    -- Add verification_code_expires column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'verification_code_expires') THEN
        ALTER TABLE "user" ADD COLUMN verification_code_expires TIMESTAMP;
        RAISE NOTICE '✅ Added verification_code_expires column';
    ELSE
        RAISE NOTICE '⏭️ verification_code_expires column already exists';
    END IF;

    -- Add verification_attempts column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'verification_attempts') THEN
        ALTER TABLE "user" ADD COLUMN verification_attempts INTEGER DEFAULT 0;
        RAISE NOTICE '✅ Added verification_attempts column';
    ELSE
        RAISE NOTICE '⏭️ verification_attempts column already exists';
    END IF;

    -- Add login_attempts column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'login_attempts') THEN
        ALTER TABLE "user" ADD COLUMN login_attempts INTEGER DEFAULT 0;
        RAISE NOTICE '✅ Added login_attempts column';
    ELSE
        RAISE NOTICE '⏭️ login_attempts column already exists';
    END IF;

    -- Add locked_until column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'locked_until') THEN
        ALTER TABLE "user" ADD COLUMN locked_until TIMESTAMP;
        RAISE NOTICE '✅ Added locked_until column';
    ELSE
        RAISE NOTICE '⏭️ locked_until column already exists';
    END IF;

    -- Add last_login_ip column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'last_login_ip') THEN
        ALTER TABLE "user" ADD COLUMN last_login_ip VARCHAR;
        RAISE NOTICE '✅ Added last_login_ip column';
    ELSE
        RAISE NOTICE '⏭️ last_login_ip column already exists';
    END IF;

    -- Add password_changed_at column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'password_changed_at') THEN
        ALTER TABLE "user" ADD COLUMN password_changed_at TIMESTAMP;
        RAISE NOTICE '✅ Added password_changed_at column';
    ELSE
        RAISE NOTICE '⏭️ password_changed_at column already exists';
    END IF;

    -- Add failed_login_attempts column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'failed_login_attempts') THEN
        ALTER TABLE "user" ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
        RAISE NOTICE '✅ Added failed_login_attempts column';
    ELSE
        RAISE NOTICE '⏭️ failed_login_attempts column already exists';
    END IF;

    -- Add last_failed_login column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'last_failed_login') THEN
        ALTER TABLE "user" ADD COLUMN last_failed_login TIMESTAMP;
        RAISE NOTICE '✅ Added last_failed_login column';
    ELSE
        RAISE NOTICE '⏭️ last_failed_login column already exists';
    END IF;

    -- Set default values for existing users (non-breaking)
    UPDATE "user" SET 
        email_verified = COALESCE(email_verified, FALSE),
        verification_attempts = COALESCE(verification_attempts, 0),
        login_attempts = COALESCE(login_attempts, 0),
        failed_login_attempts = COALESCE(failed_login_attempts, 0)
    WHERE email_verified IS NULL 
       OR verification_attempts IS NULL 
       OR login_attempts IS NULL 
       OR failed_login_attempts IS NULL;

    -- Create indexes for performance
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE tablename = 'user' AND indexname = 'ix_user_email_verification_token') THEN
        CREATE INDEX ix_user_email_verification_token ON "user" (email_verification_token);
        RAISE NOTICE '✅ Created index on email_verification_token';
    ELSE
        RAISE NOTICE '⏭️ Index on email_verification_token already exists';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE tablename = 'user' AND indexname = 'ix_user_verification_code') THEN
        CREATE INDEX ix_user_verification_code ON "user" (verification_code);
        RAISE NOTICE '✅ Created index on verification_code';
    ELSE
        RAISE NOTICE '⏭️ Index on verification_code already exists';
    END IF;

    RAISE NOTICE '🎉 Email verification migration completed successfully!';
    RAISE NOTICE '✅ All 12 email verification and security columns added';
    RAISE NOTICE '✅ Indexes created for performance';
    RAISE NOTICE '✅ Default values set for existing users';
    RAISE NOTICE '🚀 AxieStudio email verification system is ready!';

END $$;
