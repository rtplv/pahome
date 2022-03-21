"""create events event_log table

Revision ID: 41066ee0372a
Revises: badb10cf57e8
Create Date: 2022-03-12 11:02:02.053511

"""
from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision = '41066ee0372a'
down_revision = 'badb10cf57e8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "event_log",
        sa.Column("ieee_address", sa.String(255), nullable=False),
        sa.Column("topic", sa.String(255), nullable=False),
        sa.Column("body", postgresql.JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.current_timestamp())
    )
    op.create_index("event_log_ieee_address_idx", "event_log", ["ieee_address"])
    op.create_index("event_log_topic_idx", "event_log", ["topic"])


def downgrade():
    op.drop_table("event_log")
