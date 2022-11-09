import pytest

from gql.gql_id import encode_gql_id, assert_gql_id
from models.db_models import Category
from tests.creator import SecretExtraData
from utils.config import settings as s
import sqlalchemy as sa


@pytest.mark.asyncio
async def test_select_w_secret_place(
    dbsession, creator, test_client_graph, economy_values
):
    place_creator_id = await creator.create_user("Creator")
    place_tester_id = await creator.create_user("Tester")
    secret_id = (
        (
            await dbsession.execute(
                sa.select(Category.id).where(Category.mark == "secret")
            )
        )
        .fetchone()
        .id
    )

    extra_data = SecretExtraData(
        time_suggestion="Sunset",
        company_suggestion="Girlfriend",
        food_suggestion="Croissant$Wine",
        music_suggestion="Ed Sheeran",
        extra_suggestion="",
    )

    secret_place_id = await creator.create_place(
        name="Long Beach",
        category_id=secret_id,
        owner_id=place_creator_id,
        description="A romantic place",
        longitude=20,
        latitude=20,
        secret_extra_data=extra_data,
    )
    other_category_id = await creator.create_category("Auto")
