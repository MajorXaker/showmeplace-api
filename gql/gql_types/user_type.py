import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN, OP_ILIKE
from alchql.node import AsyncNode
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import User, UserImage
from utils.s3_object_tools import get_presigned_url


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (AsyncNode,)
        filter_fields = {
            User.id: [OP_EQ, OP_IN],
            User.external_id: [OP_EQ],
            User.name: [OP_ILIKE],
            # Place.user_marked: [OP_EQ]
            # M2MUserFollowingUser.lead_id.key: [OP_EQ],
            # M2MUserFollowingUser.follower_id.key: [OP_EQ],
        }
        only_fields = [
            User.id.key,
            User.name.key,
            User.has_onboarded.key,
            User.level.key,
            User.coins.key,
            User.external_id.key,
            User.external_id_type.key,
        ]

        images = graphene.List(of_type=graphene.String)

        async def resolve_images(self, info):
            session: AsyncSession = info.context.session
            images = (
                await session.execute(
                    sa.select(UserImage.id).where(UserImage.place_id == self.id)
                )
            ).fetchall()
            result = [
                await get_presigned_url(
                    session=info.context.session,
                    image_id=image.id,
                    image_class=UserImage,
                )
                for image in images
            ]
            return result

        # TODO namee ilike
        # todo user - marked place
        # todo users - place visited
        # todo user - secret place openeer

    # def resolve_id(self, info):
    #     return encode_gql_id(self.__class__.__name__, self.id)
