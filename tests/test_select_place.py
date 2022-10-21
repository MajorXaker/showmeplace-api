import pytest

from gql.gql_id import encode_gql_id
from models.db_models import Place
import sqlalchemy as sa





@pytest.mark.asyncio
async def test_select_places(dbsession, creator, test_client_graph):
    user_id = await creator.create_user()
    category_id = await creator.create_category("Auto")
    place_a = await creator.create_place(
        name="Place A", category_id=category_id, owner_id=user_id
    )
    place_b = await creator.create_place(
        name="Place b", category_id=category_id, owner_id=user_id
    )

    aaa = (await dbsession.execute(
        sa.select(Place)
    )).fetchall()

    response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": """query Edges($includeMyPlaces: Boolean) {
              selectPlaces(includeMyPlaces: $includeMyPlaces) {
                edges {
                  node {
                    id
                    coordinateLongitude
                    description
                    name
                    coordinateLatitude
                    activeDueDate
                    ownerId
                  }
                }
              }
            }""",
            "variables": {"includeMyPlaces": True},
        },
        headers={"Authorization": encode_gql_id("UserType", user_id)},
    )
    json_response = [x["node"] for x in response.json()["data"]['selectPlaces']["edges"]]
    assert len(json_response) == 2
