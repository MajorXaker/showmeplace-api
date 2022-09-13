import sqlalchemy as sa

from models.base_engine import Model, RecordTimestampFields


class BaseImage(RecordTimestampFields):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    s3_filename = sa.Column(sa.Text)
    s3_path = sa.Column(sa.Text)
    presigned_url = sa.Column(sa.Text)
    presigned_url_due = sa.Column(sa.DateTime)

    description = sa.Column(sa.Text)


class PlaceImage(Model, BaseImage):
    __tablename__ = "place_image"

    place_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("place.id", ondelete="RESTRICT"),
    )


class CategoryImage(Model, BaseImage):
    __tablename__ = "category_image"

    category_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("place.id", ondelete="RESTRICT"),
    )


class UserImage(Model, BaseImage):
    __tablename__ = "user_image"

    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("place.id", ondelete="RESTRICT"),
    )