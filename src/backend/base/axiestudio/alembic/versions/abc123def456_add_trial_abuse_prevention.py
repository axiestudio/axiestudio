"""Add trial abuse prevention fields (signup_ip, device_fingerprint)

Revision ID: abc123def456
Revises: 3162e83e485f
Create Date: 2024-12-19 12:00:00.000000

Note: Email and subscription fields are handled by separate migrations
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "abc123def456"
down_revision: Union[str, None] = "3162e83e485f"  # Latest revision
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add trial abuse prevention fields (signup_ip, device_fingerprint) to user table.

    Note: Email and subscription fields are handled by separate migration scripts.
    """
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Get existing columns
    existing_columns = [col['name'] for col in inspector.get_columns('user')]
    
    # Add new columns if they don't exist
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Note: Email and subscription fields are handled by separate migration scripts
        print("Email and subscription fields are handled by separate migrations - skipping")

        # Add signup_ip column
        if 'signup_ip' not in existing_columns:
            batch_op.add_column(sa.Column('signup_ip', sa.String(45), nullable=True))
            print("Added signup_ip column")
        else:
            print("signup_ip column already exists - skipping creation")

        # Ensure signup_ip index exists
        try:
            batch_op.create_index('ix_user_signup_ip', ['signup_ip'])
            print("Created signup_ip index")
        except Exception:
            print("signup_ip index may already exist - skipping")

        # Add device_fingerprint column
        if 'device_fingerprint' not in existing_columns:
            batch_op.add_column(sa.Column('device_fingerprint', sa.String(32), nullable=True))
            print("Added device_fingerprint column")
        else:
            print("device_fingerprint column already exists - skipping creation")

        # Ensure device_fingerprint index exists
        try:
            batch_op.create_index('ix_user_device_fingerprint', ['device_fingerprint'])
            print("Created device_fingerprint index")
        except Exception:
            print("device_fingerprint index may already exist - skipping")

        # Note: Subscription fields (stripe_customer_id, subscription_status, etc.)
        # are handled by separate migration scripts and should already exist
        print("Subscription fields are handled by separate migrations - skipping")

        print("Trial abuse prevention migration completed successfully")


def downgrade() -> None:
    """Remove trial abuse prevention fields from user table."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Remove indexes first (only the ones we created)
        indexes_to_remove = ['ix_user_signup_ip', 'ix_user_device_fingerprint']
        for index_name in indexes_to_remove:
            try:
                batch_op.drop_index(index_name)
            except Exception:
                pass

        # Remove only the columns we added (not email or subscription fields)
        columns_to_remove = ['signup_ip', 'device_fingerprint']

        for column_name in columns_to_remove:
            try:
                batch_op.drop_column(column_name)
            except Exception:
                pass

        # Note: We don't remove email or subscription fields as they're managed by other migrations
