-- 🔍 VERIFICATION COMMAND - Run this to check if all columns were added

SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default,
    CASE 
        WHEN column_name IN (
            'email_verified', 'email_verification_token', 'email_verification_expires',
            'verification_code', 'verification_code_expires', 'verification_attempts',
            'login_attempts', 'locked_until', 'last_login_ip', 
            'password_changed_at', 'failed_login_attempts', 'last_failed_login'
        ) THEN '✅ Email Verification Column'
        ELSE '⚠️ Other Column'
    END as column_type
FROM information_schema.columns
WHERE table_name = 'user' 
AND column_name IN (
    'email_verified', 'email_verification_token', 'email_verification_expires',
    'verification_code', 'verification_code_expires', 'verification_attempts',
    'login_attempts', 'locked_until', 'last_login_ip', 
    'password_changed_at', 'failed_login_attempts', 'last_failed_login'
)
ORDER BY column_name;
