"""image relation fixes

Revision ID: 16c000248278
Revises: 0521b017e695
Create Date: 2022-09-17 11:45:57.592940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "16c000248278"
down_revision = "0521b017e695"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "fk_category_image_category_id_place", "category_image", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_category_image_category_id_category"),
        "category_image",
        "category",
        ["category_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.add_column("place", sa.Column("active_due_date", sa.DateTime(), nullable=True))
    op.alter_column("place", "category_id", existing_type=sa.INTEGER(), nullable=False)
    op.create_index(
        op.f("ix_place_category_id"), "place", ["category_id"], unique=False
    )
    op.drop_constraint(
        "fk_place_image_place_id_place", "place_image", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_place_image_place_id_place"),
        "place_image",
        "place",
        ["place_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint("fk_user_image_user_id_place", "user_image", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_user_image_user_id_user"),
        "user_image",
        "user",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_user_image_user_id_user"), "user_image", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_user_image_user_id_place",
        "user_image",
        "place",
        ["user_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.drop_constraint(
        op.f("fk_place_image_place_id_place"), "place_image", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_place_image_place_id_place",
        "place_image",
        "place",
        ["place_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.drop_index(op.f("ix_place_category_id"), table_name="place")
    op.alter_column("place", "category_id", existing_type=sa.INTEGER(), nullable=True)
    op.drop_column("place", "active_due_date")
    op.drop_constraint(
        op.f("fk_category_image_category_id_category"),
        "category_image",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_category_image_category_id_place",
        "category_image",
        "place",
        ["category_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    # ### end Alembic commands ###
