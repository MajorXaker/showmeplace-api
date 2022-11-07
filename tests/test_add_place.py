import pytest

from gql.gql_id import encode_gql_id, assert_gql_id


@pytest.mark.asyncio
async def test_add_place(dbsession, creator, test_client_graph):
    user_id = await creator.create_user()
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
    assert (
        data["coinChange"]["coins"] == "25"
    )  # TODO this will break down when we change the economy

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
