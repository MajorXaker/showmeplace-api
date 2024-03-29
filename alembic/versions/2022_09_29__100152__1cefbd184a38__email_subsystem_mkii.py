"""email subsystem mkII

Revision ID: 1cefbd184a38
Revises: f2795db71ef8
Create Date: 2022-09-29 10:01:52.033519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1cefbd184a38"
down_revision = "f2795db71ef8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "email_address", "address", existing_type=sa.VARCHAR(), nullable=False
    )
    op.drop_index("ix_email_address_status", table_name="email_address")
    op.create_index(
        op.f("ix_email_address_address"), "email_address", ["address"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_email_address_address"), table_name="email_address")
    op.create_index(
        "ix_email_address_status", "email_address", ["status"], unique=False
    )
    op.alter_column(
        "email_address", "address", existing_type=sa.VARCHAR(), nullable=True
    )
    # ### end Alembic commands ###
