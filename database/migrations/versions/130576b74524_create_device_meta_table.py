"""create device meta table

Revision ID: 130576b74524
Revises: 41066ee0372a
Create Date: 2022-03-12 21:54:05.344540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '130576b74524'
down_revision = '41066ee0372a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "device_meta",
        sa.Column("ieee_address", sa.String(255), sa.ForeignKey("devices.ieee_address"), unique=True, primary_key=True),
        sa.Column("model", sa.String(255), nullable=False),
        sa.Column("vendor", sa.String(255)),
        sa.Column("description", sa.Text),
        sa.Column("options", sa.JSON),
        sa.Column("exposes", sa.JSON),
    )


def downgrade():
    op.drop_table("device_meta")
