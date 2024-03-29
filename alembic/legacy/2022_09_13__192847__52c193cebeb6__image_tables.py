"""image tables

Revision ID: 52c193cebeb6
Revises: 1742e2f308ad
Create Date: 2022-09-13 19:28:47.587285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52c193cebeb6"
down_revision = "1742e2f308ad"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "category",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "category",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_category_record_modified"),
        "category",
        ["record_modified"],
        unique=False,
    )
    op.add_column(
        "category_image",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "category_image",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column("category_image", sa.Column("s3_path", sa.Text(), nullable=True))
    op.add_column(
        "category_image", sa.Column("presigned_url", sa.Text(), nullable=True)
    )
    op.add_column(
        "category_image", sa.Column("presigned_url_due", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "category_image", sa.Column("category_id", sa.Integer(), nullable=True)
    )
    op.create_index(
        op.f("ix_category_image_record_modified"),
        "category_image",
        ["record_modified"],
        unique=False,
    )
    op.drop_constraint(
        "fk_category_image_user_id_user", "category_image", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_category_image_category_id_place"),
        "category_image",
        "place",
        ["category_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.drop_column("category_image", "user_id")
    op.add_column(
        "m2m_user_opened_secret_place",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "m2m_user_opened_secret_place",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_m2m_user_opened_secret_place_record_modified"),
        "m2m_user_opened_secret_place",
        ["record_modified"],
        unique=False,
    )
    op.add_column(
        "m2m_user_place_favourite",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "m2m_user_place_favourite",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_m2m_user_place_favourite_record_modified"),
        "m2m_user_place_favourite",
        ["record_modified"],
        unique=False,
    )
    op.add_column(
        "m2m_user_place_marked",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "m2m_user_place_marked",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_m2m_user_place_marked_record_modified"),
        "m2m_user_place_marked",
        ["record_modified"],
        unique=False,
    )
    op.add_column(
        "m2m_user_place_visited",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "m2m_user_place_visited",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_m2m_user_place_visited_record_modified"),
        "m2m_user_place_visited",
        ["record_modified"],
        unique=False,
    )
    op.add_column(
        "m2m_user_user_following_user",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "m2m_user_user_following_user",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_m2m_user_user_following_user_record_modified"),
        "m2m_user_user_following_user",
        ["record_modified"],
        unique=False,
    )
    op.add_column(
        "place",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "place",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_place_record_modified"), "place", ["record_modified"], unique=False
    )
    op.add_column(
        "place_image",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "place_image",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column("place_image", sa.Column("s3_path", sa.Text(), nullable=True))
    op.add_column("place_image", sa.Column("presigned_url", sa.Text(), nullable=True))
    op.add_column(
        "place_image", sa.Column("presigned_url_due", sa.DateTime(), nullable=True)
    )
    op.create_index(
        op.f("ix_place_image_record_modified"),
        "place_image",
        ["record_modified"],
        unique=False,
    )
    op.add_column(
        "secret_extras",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "secret_extras",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_secret_extras_record_modified"),
        "secret_extras",
        ["record_modified"],
        unique=False,
    )
    op.add_column(
        "user",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "user",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_user_record_modified"), "user", ["record_modified"], unique=False
    )
    op.add_column(
        "user_image",
        sa.Column(
            "record_created",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column(
        "user_image",
        sa.Column(
            "record_modified",
            sa.DateTime(),
            server_default=sa.text("statement_timestamp()"),
            nullable=False,
        ),
    )
    op.add_column("user_image", sa.Column("s3_path", sa.Text(), nullable=True))
    op.add_column("user_image", sa.Column("presigned_url", sa.Text(), nullable=True))
    op.add_column(
        "user_image", sa.Column("presigned_url_due", sa.DateTime(), nullable=True)
    )
    op.create_index(
        op.f("ix_user_image_record_modified"),
        "user_image",
        ["record_modified"],
        unique=False,
    )
    op.drop_constraint("fk_user_image_user_id_user", "user_image", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_user_image_user_id_place"),
        "user_image",
        "place",
        ["user_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_user_image_user_id_place"), "user_image", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_user_image_user_id_user",
        "user_image",
        "user",
        ["user_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.drop_index(op.f("ix_user_image_record_modified"), table_name="user_image")
    op.drop_column("user_image", "presigned_url_due")
    op.drop_column("user_image", "presigned_url")
    op.drop_column("user_image", "s3_path")
    op.drop_column("user_image", "record_modified")
    op.drop_column("user_image", "record_created")
    op.drop_index(op.f("ix_user_record_modified"), table_name="user")
    op.drop_column("user", "record_modified")
    op.drop_column("user", "record_created")
    op.drop_index(op.f("ix_secret_extras_record_modified"), table_name="secret_extras")
    op.drop_column("secret_extras", "record_modified")
    op.drop_column("secret_extras", "record_created")
    op.drop_index(op.f("ix_place_image_record_modified"), table_name="place_image")
    op.drop_column("place_image", "presigned_url_due")
    op.drop_column("place_image", "presigned_url")
    op.drop_column("place_image", "s3_path")
    op.drop_column("place_image", "record_modified")
    op.drop_column("place_image", "record_created")
    op.drop_index(op.f("ix_place_record_modified"), table_name="place")
    op.drop_column("place", "record_modified")
    op.drop_column("place", "record_created")
    op.drop_index(
        op.f("ix_m2m_user_user_following_user_record_modified"),
        table_name="m2m_user_user_following_user",
    )
    op.drop_column("m2m_user_user_following_user", "record_modified")
    op.drop_column("m2m_user_user_following_user", "record_created")
    op.drop_index(
        op.f("ix_m2m_user_place_visited_record_modified"),
        table_name="m2m_user_place_visited",
    )
    op.drop_column("m2m_user_place_visited", "record_modified")
    op.drop_column("m2m_user_place_visited", "record_created")
    op.drop_index(
        op.f("ix_m2m_user_place_marked_record_modified"),
        table_name="m2m_user_place_marked",
    )
    op.drop_column("m2m_user_place_marked", "record_modified")
    op.drop_column("m2m_user_place_marked", "record_created")
    op.drop_index(
        op.f("ix_m2m_user_place_favourite_record_modified"),
        table_name="m2m_user_place_favourite",
    )
    op.drop_column("m2m_user_place_favourite", "record_modified")
    op.drop_column("m2m_user_place_favourite", "record_created")
    op.drop_index(
        op.f("ix_m2m_user_opened_secret_place_record_modified"),
        table_name="m2m_user_opened_secret_place",
    )
    op.drop_column("m2m_user_opened_secret_place", "record_modified")
    op.drop_column("m2m_user_opened_secret_place", "record_created")
    op.add_column(
        "category_image",
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(
        op.f("fk_category_image_category_id_place"),
        "category_image",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_category_image_user_id_user",
        "category_image",
        "user",
        ["user_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.drop_index(
        op.f("ix_category_image_record_modified"), table_name="category_image"
    )
    op.drop_column("category_image", "category_id")
    op.drop_column("category_image", "presigned_url_due")
    op.drop_column("category_image", "presigned_url")
    op.drop_column("category_image", "s3_path")
    op.drop_column("category_image", "record_modified")
    op.drop_column("category_image", "record_created")
    op.drop_index(op.f("ix_category_record_modified"), table_name="category")
    op.drop_column("category", "record_modified")
    op.drop_column("category", "record_created")
    # ### end Alembic commands ###
