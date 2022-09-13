import sqlalchemy as sa

from models.base_engine import Model, RecordTimestampFields


class CategoryImage(Model, RecordTimestampFields):
    __tablename__ = "category_image"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("user.id", ondelete="RESTRICT"),
        # index=True,
        # nullable=False,
    )
    s3_filename = sa.Column(sa.Text)
    description = sa.Column(sa.Text)
