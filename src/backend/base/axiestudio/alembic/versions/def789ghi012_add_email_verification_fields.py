"""Add 6-digit email verification fields and enhanced security columns

Revision ID: def789ghi012
Revises: abc123def456
Create Date: 2024-12-19 15:00:00.000000

This migration adds the new 6-digit email verification system fields
and enhanced security columns to support enterprise-grade authentication.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "def789ghi012"
down_revision: Union[str, None] = "abc123def456"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add 6-digit email verification fields and enhanced security columns.

    This migration adds:
    1. 6-digit verification code fields (verification_code, verification_code_expires, verification_attempts)
    2. Enhanced security fields (login_attempts, locked_until, last_login_ip, etc.)
    3. Email verification fields (email_verified, email_verification_token, email_verification_expires)
    """
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Get existing columns
    existing_columns = [col['name'] for col in inspector.get_columns('user')]
    
    # Define all email verification and security fields
    fields_to_add = {
        # Email verification fields (legacy token-based)
        'email_verified': {'type': sa.Boolean(), 'nullable': False, 'default': False},
        'email_verification_token': {'type': sa.String(), 'nullable': True},
        'email_verification_expires': {'type': sa.DateTime(), 'nullable': True},
        
        # 🎯 NEW: 6-digit code verification fields (enterprise-grade)
        'verification_code': {'type': sa.String(6), 'nullable': True},
        'verification_code_expires': {'type': sa.DateTime(), 'nullable': True},
        'verification_attempts': {'type': sa.Integer(), 'nullable': False, 'default': 0},
        
        # Enhanced security fields for enterprise auth
        'login_attempts': {'type': sa.Integer(), 'nullable': False, 'default': 0},
        'locked_until': {'type': sa.DateTime(), 'nullable': True},
        'last_login_ip': {'type': sa.String(), 'nullable': True},
        'password_changed_at': {'type': sa.DateTime(), 'nullable': True},
        'failed_login_attempts': {'type': sa.Integer(), 'nullable': False, 'default': 0},
        'last_failed_login': {'type': sa.DateTime(), 'nullable': True},
    }

    # Add columns using batch operations for better compatibility
    with op.batch_alter_table('user', schema=None) as batch_op:
        print("Starting email verification and security fields migration...")
        
        added_count = 0
        for field_name, field_config in fields_to_add.items():
            if field_name not in existing_columns:
                try:
                    # Create column with proper configuration
                    column = sa.Column(
                        field_name,
                        field_config['type'],
                        nullable=field_config['nullable'],
                        default=field_config.get('default')
                    )
                    
                    batch_op.add_column(column)
                    print(f"✅ Added {field_name} column")
                    added_count += 1
                    
                except Exception as e:
                    print(f"❌ Failed to add {field_name} column: {e}")
            else:
                print(f"⏭️ {field_name} column already exists - skipping")
        
        # Set default values for existing users
        if added_count > 0:
            print("Setting default values for existing users...")
            
            # Set email_verified to False for existing users if the column was just added
            if 'email_verified' not in existing_columns:
                try:
                    conn.execute(sa.text("UPDATE \"user\" SET email_verified = FALSE WHERE email_verified IS NULL"))
                    print("✅ Set email_verified = FALSE for existing users")
                except Exception as e:
                    print(f"❌ Failed to set email_verified defaults: {e}")
            
            # Set verification_attempts to 0 for existing users if the column was just added
            if 'verification_attempts' not in existing_columns:
                try:
                    conn.execute(sa.text("UPDATE \"user\" SET verification_attempts = 0 WHERE verification_attempts IS NULL"))
                    print("✅ Set verification_attempts = 0 for existing users")
                except Exception as e:
                    print(f"❌ Failed to set verification_attempts defaults: {e}")
            
            # Set login_attempts to 0 for existing users if the column was just added
            if 'login_attempts' not in existing_columns:
                try:
                    conn.execute(sa.text("UPDATE \"user\" SET login_attempts = 0 WHERE login_attempts IS NULL"))
                    print("✅ Set login_attempts = 0 for existing users")
                except Exception as e:
                    print(f"❌ Failed to set login_attempts defaults: {e}")
            
            # Set failed_login_attempts to 0 for existing users if the column was just added
            if 'failed_login_attempts' not in existing_columns:
                try:
                    conn.execute(sa.text("UPDATE \"user\" SET failed_login_attempts = 0 WHERE failed_login_attempts IS NULL"))
                    print("✅ Set failed_login_attempts = 0 for existing users")
                except Exception as e:
                    print(f"❌ Failed to set failed_login_attempts defaults: {e}")

        print(f"Email verification and security fields migration completed! Added {added_count} new columns.")


def downgrade() -> None:
    """Remove 6-digit email verification fields and enhanced security columns."""
    
    # Define fields to remove (only the ones we added in this migration)
    fields_to_remove = [
        'verification_code',
        'verification_code_expires', 
        'verification_attempts',
        'login_attempts',
        'locked_until',
        'last_login_ip',
        'password_changed_at',
        'failed_login_attempts',
        'last_failed_login'
    ]
    
    # Note: We keep email_verified, email_verification_token, email_verification_expires
    # as they might be used by other parts of the system
    
    with op.batch_alter_table('user', schema=None) as batch_op:
        print("Removing email verification and security fields...")
        
        for field_name in fields_to_remove:
            try:
                batch_op.drop_column(field_name)
                print(f"✅ Removed {field_name} column")
            except Exception as e:
                print(f"❌ Failed to remove {field_name} column: {e}")
        
        print("Email verification and security fields removal completed!")
