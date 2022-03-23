"""create device state table

Revision ID: a91fd8fa7dd8
Revises: 130576b74524
Create Date: 2022-03-19 14:04:27.119421

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'a91fd8fa7dd8'
down_revision = '130576b74524'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "device_state",
        sa.Column("ieee_address", sa.String(255), sa.ForeignKey("devices.ieee_address"), unique=True, primary_key=True),
        sa.Column("state", postgresql.JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()),
    )


def downgrade():
    op.drop_table("device_state")

