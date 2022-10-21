import pytest

from gql.gql_id import encode_gql_id
from models.db_models import Place
import sqlalchemy as sa


@pytest.mark.asyncio
async def test_add_place(dbsession, creator, test_client_graph):
    user_id = await creator.create_user()
    category_id = await creator.create_category("Auto")
    response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": """
                    mutation AddPlace($placeData: PlaceDataInput) {
                      addPlace(placeData: $placeData) {
                        coinChange {
                          changeAmount
                          coins
                        }
                        newPlace {
                          id
                          name
                          description
                          coordinateLatitude
                          coordinateLongitude
                          activeDueDate
                          ownerId
                          categoryData {
                            id
                            mark
                            name
                          }
                          hasVisited
                          hasFavourited
                          isOpenedForUser
                        }
                      }
                    }
                """,
            "variables": {
                "placeData": {
                    "name": "Joe's Car Dealership",
                    "categoryId": encode_gql_id("CategoryType", category_id),
                    "coordinateLongitude": 19.84,
                    "coordinateLatitude": 21.42,
                    "address": "Groove St 4",
                    "description": "Best cars of the LosSantos",
                }
            },
        },
        headers={"Authorization": encode_gql_id("UserType", user_id)},
    )
    json_response = response.json()
    assert not json_response["error"]
