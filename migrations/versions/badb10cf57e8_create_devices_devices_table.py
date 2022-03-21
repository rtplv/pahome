"""create [devices] devices table

Revision ID: badb10cf57e8
Revises: 
Create Date: 2022-03-11 22:04:24.986416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'badb10cf57e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "devices",
        sa.Column("ieee_address", sa.String(255), unique=True, primary_key=True),
        sa.Column("friendly_name", sa.String(255)),
        sa.Column("removed", sa.Boolean, nullable=False, default=False),
        sa.Column("created_at", sa.DateTime, default=sa.func.current_timestamp()),
        sa.Column("updated_at", sa.DateTime, default=sa.func.current_timestamp()),
    )


def downgrade():
    op.drop_table("devices")
