import pytest

from gql.gql_id import encode_gql_id, assert_gql_id
from models.db_models import Category
from utils.config import settings as s
import sqlalchemy as sa

@pytest.mark.asyncio
async def test_add_place(dbsession, creator, test_client_graph, economy_values):
    user_id = await creator.create_user(coins=50)
    category_name = "Auto"
    category_id = await creator.create_category(category_name)
    category_encoded = encode_gql_id("CategoryType", category_id)
    inserted_data = {
        "name": "Joe's Car Dealership",
        "categoryId": category_encoded,
        "coordinateLongitude": 19.84,
        "coordinateLatitude": 21.42,
        "address": "Groove St 4",
        "description": "Best cars of the LosSantos",
    }

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
                          address
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
            "variables": {"placeData": inserted_data},
        },
        headers={"Authorization": encode_gql_id("UserType", user_id)},
    )
    json_response = response.json()
    assert not json_response.get("errors")
    data = json_response["data"]["addPlace"]
    assert data["coinChange"]["coins"] == economy_values["Create a place"] + 50

    data_from_query = data["newPlace"]
    # category assertion block
    category_from_query = data_from_query["categoryData"]
    assert category_from_query["name"] == category_name
    assert_gql_id(
        coded_id=category_from_query["id"], data_type="CategoryType", id_=category_id
    )
    # place assertion block
    inserted_data_from_query = {
        k: v for k, v in data_from_query.items() if k in inserted_data.keys()
    }
    inserted_data_from_query["categoryId"] = category_from_query["id"]
    assert inserted_data_from_query == inserted_data
    assert data["newPlace"]["isOpenedForUser"]
    assert not data["newPlace"]["hasFavourited"]
    assert not data["newPlace"]["hasVisited"]
    assert_gql_id(
        coded_id=data["newPlace"]["ownerId"], data_type="UserType", id_=user_id
    )


@pytest.mark.asyncio
async def test_place_update(dbsession, creator, test_client_graph):
    user_id = await creator.create_user()
    category_id = await creator.create_category("Auto")
    place_id = await creator.create_place(
        name="Place A",
        category_id=category_id,
        owner_id=user_id,
        description="Place A",
        address="Address A",
    )

    update_data = {"name": "Sample place", "description": "Sample description"}

    response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": """mutation UpdatePlace($updatePlaceId: ID!, $value: InputUpdatePlace!) {
              updatePlace(id: $updatePlaceId, value: $value) {
                id
                name
                description
                address
              }
            }""",
            "variables": {
                "updatePlaceId": encode_gql_id("PlaceType", place_id),
                "value": update_data,
            },
        },
        headers={"Authorization": encode_gql_id("UserType", user_id)},
    )
    data = response.json()
    assert not data.get("errors")
    assert data["data"]["updatePlace"] == {
        "id": encode_gql_id("PlaceType", place_id),
        "address": "Address A",
        **update_data,
    }


@pytest.mark.asyncio
async def test_favour(dbsession, creator, test_client_graph, economy_values):
    place_creator_id = await creator.create_user("Creator")
    place_tester_id = await creator.create_user("Tester")
    category_id = await creator.create_category("Auto")
    place_id = await creator.create_place(
        name="Sample Place",
        category_id=category_id,
        owner_id=place_creator_id,
        description="Sample Description",
        longitude=50,
        latitude=51,
    )
    response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": """mutation AddFavouritePlace($value: MutationAddFavouritePlaceInputType!) {
              addFavouritePlace(value: $value) {
                id
                name
              }
            }""",
            "variables": {"value": {"placeId": encode_gql_id("PlaceType", place_id)}},
        },
        headers={"Authorization": encode_gql_id("UserType", place_tester_id)},
    )
    data = response.json()
    assert not data.get("errors")
    assert data["data"]["addFavouritePlace"] == {
        "name": "Sample Place",
        "id": encode_gql_id("PlaceType", place_id),
    }

    response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": """mutation RemoveFavouritePlace($placeId: String!) {
                  removeFavouritePlace(placeId: $placeId) {
                    isSuccess
                  }
                }""",
            "variables": {"placeId": encode_gql_id("PlaceType", place_id)},
        },
        headers={"Authorization": encode_gql_id("UserType", place_tester_id)},
    )
    data = response.json()
    assert "errors" not in data
    assert data["data"]["removeFavouritePlace"]["isSuccess"]


@pytest.mark.asyncio
async def test_visit(dbsession, creator, test_client_graph, economy_values):
    place_creator_id = await creator.create_user("Creator")
    place_tester_id = await creator.create_user("Tester")
    category_id = await creator.create_category("Auto")
    place_id = await creator.create_place(
        name="Sample Place",
        category_id=category_id,
        owner_id=place_creator_id,
        description="Sample Description",
        longitude=50,
        latitude=51,
    )
    s.CHECK_IN_DISTANCE_METERS = 100000

    response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": """mutation CheckInPlace($checkInPlaceId: String!, $userLatitude: Float!, $userLongitude: Float!) {
              checkInPlace(checkIn_Place_Id: $checkInPlaceId, user_Latitude: $userLatitude, user_Longitude: $userLongitude) {
                isSuccess
                coinChange {
                  changeAmount
                  coins
                }
                distanceToPlace
              }
            }""",
            "variables": {
                "checkInPlaceId": encode_gql_id("PlaceType", place_id),
                "userLatitude": 50.5,
                "userLongitude": 50.5,
            },
        },
        headers={"Authorization": encode_gql_id("UserType", place_tester_id)},
    )
    assert "errors" not in response.json()
    data = response.json()["data"]["checkInPlace"]
    assert data["isSuccess"]
    assert data["coinChange"]["changeAmount"] == economy_values["Visit a place"]
    assert 66100 > data["distanceToPlace"] > 66000
    # For now we cannot unvisit a place
    # Methods for it are temporary and unaccessable to end users
