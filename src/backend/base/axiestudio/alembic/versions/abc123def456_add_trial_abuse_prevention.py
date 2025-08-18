"""Add trial abuse prevention fields

Revision ID: abc123def456
Revises: 3162e83e485f
Create Date: 2024-12-19 12:00:00.000000

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
    """Add trial abuse prevention fields to user table."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Get existing columns
    existing_columns = [col['name'] for col in inspector.get_columns('user')]
    
    # Add new columns if they don't exist
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Add signup_ip column
        if 'signup_ip' not in existing_columns:
            batch_op.add_column(sa.Column('signup_ip', sa.String(45), nullable=True))
            batch_op.create_index('ix_user_signup_ip', ['signup_ip'])
        
        # Add device_fingerprint column
        if 'device_fingerprint' not in existing_columns:
            batch_op.add_column(sa.Column('device_fingerprint', sa.String(32), nullable=True))
            batch_op.create_index('ix_user_device_fingerprint', ['device_fingerprint'])
        
        # Make email unique if not already (but keep nullable for existing users)
        # Note: We'll handle the NOT NULL constraint separately for existing data
        try:
            # Check if unique constraint already exists
            constraints = inspector.get_unique_constraints('user')
            email_unique_exists = any('email' in constraint['column_names'] for constraint in constraints)
            
            if not email_unique_exists:
                batch_op.create_unique_constraint('uq_user_email', ['email'])
        except Exception as e:
            # If constraint creation fails, log but continue
            print(f"Warning: Could not create email unique constraint: {e}")


def downgrade() -> None:
    """Remove trial abuse prevention fields from user table."""
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Remove indexes first
        try:
            batch_op.drop_index('ix_user_signup_ip')
        except Exception:
            pass
        
        try:
            batch_op.drop_index('ix_user_device_fingerprint')
        except Exception:
            pass
        
        # Remove unique constraint
        try:
            batch_op.drop_constraint('uq_user_email', type_='unique')
        except Exception:
            pass
        
        # Remove columns
        try:
            batch_op.drop_column('signup_ip')
        except Exception:
            pass
        
        try:
            batch_op.drop_column('device_fingerprint')
        except Exception:
            pass
