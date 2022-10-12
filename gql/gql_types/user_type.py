import graphene
import sqlalchemy as sa
from alchql import SQLAlchemyObjectType
from alchql.consts import OP_EQ, OP_IN, OP_ILIKE
from alchql.node import AsyncNode
from alchql.utils import FilterItem
from sqlalchemy.ext.asyncio import AsyncSession

from gql.gql_id import decode_gql_id, encode_gql_id
from models.db_models import User, UserImage, M2MUserFollowingUser, EmailAddress
from models.enums import EmailStatusEnum
from utils.api_auth import AuthChecker
from utils.logging_tools import debug_log
from utils.s3_object_tools import get_presigned_url
from utils.utils import CountableConnectionCreator


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (AsyncNode,)
        connection_class = CountableConnectionCreator
        filter_fields = {
            User.id: [OP_EQ, OP_IN],
            User.external_id: [OP_EQ],
            User.name: [OP_ILIKE],
            "user_follower_of": FilterItem(
                field_type=graphene.String, filter_func=None
            ),
            "user_followers": FilterItem(field_type=graphene.String, filter_func=None),
        }
        only_fields = [
            User.id.key,
            User.name.key,
            User.description.key,
            User.has_onboarded.key,
            User.level.key,
            User.coins.key,
            User.external_id.key,
            User.external_id_type.key,
        ]

    images = graphene.String()
    followers = graphene.List(of_type=graphene.String)
    following = graphene.List(of_type=graphene.String)
    active_email = graphene.String()

    async def resolve_active_email(self, info):
        session: AsyncSession = info.context.session
        email = (
            await session.execute(
                sa.select(EmailAddress.address).where(
                    sa.and_(
                        EmailAddress.user_id == self.id,
                        EmailAddress.status == EmailStatusEnum.VERIFIED,
                    )
                )
            )
        ).fetchone()
        return email.address if email else None

    async def resolve_followers(self, info):
        session: AsyncSession = info.context.session
        followers = (
            await session.execute(
                sa.select(M2MUserFollowingUser.follower_id).where(
                    M2MUserFollowingUser.lead_id == self.id
                )
            )
        ).fetchall()
        return [encode_gql_id("UserType", usr.follower_id) for usr in followers]

    async def resolve_following(self, info):
        session: AsyncSession = info.context.session
        followers = (
            await session.execute(
                sa.select(M2MUserFollowingUser.lead_id).where(
                    M2MUserFollowingUser.follower_id == self.id
                )
            )
        ).fetchall()
        return [encode_gql_id("UserType", usr.lead_id) for usr in followers]

    async def resolve_images(self, info):
        session: AsyncSession = info.context.session
        image = (
            await session.execute(
                sa.select(UserImage.id).where(UserImage.user_id == self.id)
            )
        ).fetchone()
        if image:
            result = await get_presigned_url(
                session=info.context.session,
                image_id=image.id,
                image_class=UserImage,
            )
            return result
        return ""

        # TODO namee ilike
        # todo user - marked place
        # todo users - place visited
        # todo user - secret place openeer

    # def resolve_id(self, info):
    #     return encode_gql_id(self.__class__.__name__, self.id)

    @classmethod
    async def set_select_from(cls, info, q, query_fields):
        asker_id = AuthChecker.check_auth_request(info)
        await debug_log(cls, info)
        if "userFollowerOf" in info.variable_values:
            user = decode_gql_id(info.variable_values["userVisited"])[1]
            q = q.outerjoin_from(
                User,
                M2MUserFollowingUser,
                onclause=(User.id == M2MUserFollowingUser.lead_id),
            ).where(M2MUserFollowingUser.follower_id == user)
        if "userFollowers" in info.variable_values:
            user = decode_gql_id(info.variable_values["userVisited"])[1]
            q = q.outerjoin_from(
                User,
                M2MUserFollowingUser,
                onclause=(User.id == M2MUserFollowingUser.follower_id),
            ).where(M2MUserFollowingUser.lead_id == user)

        return q
