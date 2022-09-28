"""email subsystem

Revision ID: f2795db71ef8
Revises: dd3647d3a599
Create Date: 2022-09-27 22:29:34.050719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f2795db71ef8"
down_revision = "dd3647d3a599"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "email_address",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("status", sa.String(), server_default="PENDING", nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_email_address_user_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_email_address")),
    )
    op.create_index(
        op.f("ix_email_address_record_modified"),
        "email_address",
        ["record_modified"],
        unique=False,
    )
    op.create_index(
        op.f("ix_email_address_status"), "email_address", ["status"], unique=False
    )
    op.create_index(
        op.f("ix_email_address_user_id"), "email_address", ["user_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_email_address_user_id"), table_name="email_address")
    op.drop_index(op.f("ix_email_address_status"), table_name="email_address")
    op.drop_index(op.f("ix_email_address_record_modified"), table_name="email_address")
    op.drop_table("email_address")
    # ### end Alembic commands ###
