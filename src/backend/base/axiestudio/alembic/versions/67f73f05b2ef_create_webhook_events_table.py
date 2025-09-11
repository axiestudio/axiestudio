"""Create webhook_events table for Stripe webhook idempotency

Revision ID: 67f73f05b2ef
Revises: 66f72f04a1de
Create Date: 2025-01-11 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from axiestudio.utils import migration

# revision identifiers, used by Alembic.
revision: str = '67f73f05b2ef'
down_revision: Union[str, None] = '66f72f04a1de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create webhook_events table for Stripe webhook processing idempotency."""
    conn = op.get_bind()
    
    # Create webhook_events table if it doesn't exist
    if not migration.table_exists("webhook_events", conn):
        op.create_table(
            "webhook_events",
            sa.Column("id", sqlmodel.sql.sqltypes.types.Uuid(), nullable=False),
            sa.Column("stripe_event_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("event_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("stripe_event_id"),
        )
        
        # Create indexes for performance
        op.create_index("ix_webhook_events_stripe_event_id", "webhook_events", ["stripe_event_id"])
        op.create_index("ix_webhook_events_status", "webhook_events", ["status"])
        op.create_index("ix_webhook_events_created_at", "webhook_events", ["created_at"])


def downgrade() -> None:
    """Drop webhook_events table."""
    conn = op.get_bind()
    
    if migration.table_exists("webhook_events", conn):
        # Drop indexes first
        op.drop_index("ix_webhook_events_created_at", "webhook_events")
        op.drop_index("ix_webhook_events_status", "webhook_events")
        op.drop_index("ix_webhook_events_stripe_event_id", "webhook_events")
        
        # Drop table
        op.drop_table("webhook_events")
