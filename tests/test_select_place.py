import random

import pytest

from gql.gql_id import encode_gql_id, decode_gql_id
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
    json_response = [
        x["node"] for x in response.json()["data"]["selectPlaces"]["edges"]
    ]
    assert len(json_response) == 2


@pytest.mark.asyncio
async def test_select_coordinate_box_category(dbsession, creator, test_client_graph):
    user_id = await creator.create_user()
    good_category_id = await creator.create_category("Auto")
    bad_category_id = await creator.create_category("Aero")
    coordinate_box = {
        "neLongitude": 45,
        "neLatitude": 45,
        "swLongitude": 30,
        "swLatitude": 30,
    }

    good_category_good_coordinates_places_ids = [
        await creator.create_place(
            name=f"Place g_cat g_coord #{n}",
            category_id=good_category_id,
            owner_id=user_id,
            latitude=random.randint(
                coordinate_box["swLatitude"], coordinate_box["neLatitude"]
            ),
            longitude=random.randint(
                coordinate_box["swLongitude"], coordinate_box["neLongitude"]
            ),
        )
        for n in range(1, 4)
    ]
    bad_category_good_coordinates_places_ids = [
        await creator.create_place(
            name=f"Place b_cat g_coord #{n}",
            category_id=bad_category_id,
            owner_id=user_id,
            latitude=random.randint(
                coordinate_box["swLatitude"], coordinate_box["neLatitude"]
            ),
            longitude=random.randint(
                coordinate_box["swLongitude"], coordinate_box["neLongitude"]
            ),
        )
        for n in range(1, 4)
    ]
    good_category_bad_coordinates_places_ids = [
        await creator.create_place(
            name=f"Place g_cat b_coord #{n}",
            category_id=good_category_id,
            owner_id=user_id,
            latitude=random.randint(
                -coordinate_box["neLatitude"], -coordinate_box["swLatitude"]
            ),
            longitude=random.randint(
                -coordinate_box["neLongitude"], -coordinate_box["swLongitude"]
            ),
        )
        for n in range(1, 4)
    ]
    bad_category_bad_coordinates_places_ids = [
        await creator.create_place(
            name=f"Place b_cat b_coord #{n}",
            category_id=bad_category_id,
            owner_id=user_id,
            latitude=random.randint(
                -coordinate_box["neLatitude"], -coordinate_box["swLatitude"]
            ),
            longitude=random.randint(
                -coordinate_box["neLongitude"], -coordinate_box["swLongitude"]
            ),
        )
        for n in range(1, 4)
    ]
    query = """query SelectPlaces($categoryIdEq: ID, $coordinateBox:
                CoordinateBox, $includeMyPlaces: Boolean) {
                    selectPlaces(categoryId_Eq: $categoryIdEq, coordinateBox: 
                    $coordinateBox, includeMyPlaces: $includeMyPlaces) {
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
                }"""
    response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": query,
            "variables": {
                "includeMyPlaces": True,
                "coordinateBox": coordinate_box,
                "categoryIdEq": encode_gql_id(
                    "CategoryType", good_category_id
                ),  # TODO implement class passing not a str
            },
        },
        headers={"Authorization": encode_gql_id("UserType", user_id)},
    )
    assert not response.json().get("errors")
    json_response = [
        x["node"] for x in response.json()["data"]["selectPlaces"]["edges"]
    ]
    assert set(good_category_good_coordinates_places_ids) == set(
        (decode_gql_id(x["id"])[1] for x in json_response)
    )

    # just category testing
    query = """query SelectPlaces($categoryIdEq: ID,$includeMyPlaces: Boolean) {
                        selectPlaces(categoryId_Eq: $categoryIdEq, includeMyPlaces: $includeMyPlaces) {
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
                    }"""
    response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": query,
            "variables": {
                "includeMyPlaces": True,
                "categoryIdEq": encode_gql_id("CategoryType", good_category_id),
            },
        },
        headers={"Authorization": encode_gql_id("UserType", user_id)},
    )
    assert not response.json().get("errors")
    json_response = [
        x["node"] for x in response.json()["data"]["selectPlaces"]["edges"]
    ]
    expected_data = {
        *good_category_good_coordinates_places_ids,
        *good_category_bad_coordinates_places_ids,
    }
    assert expected_data == set((decode_gql_id(x["id"])[1] for x in json_response))


@pytest.mark.asyncio
async def test_on_user_selection(dbsession, creator, test_client_graph):
    user_id_alpha = await creator.create_user("AlphaUser")
    user_id_beta = await creator.create_user("BetaUser")
    user_id_gamma = await creator.create_user("GammaUser")
    category_id = await creator.create_category("Auto")

    place_alpha = await creator.create_place(
        name="Place A", category_id=category_id, owner_id=user_id_alpha
    )
    place_beta = await creator.create_place(
        name="Place B", category_id=category_id, owner_id=user_id_beta
    )
    place_gamma = await creator.create_place(
        name="Place C", category_id=category_id, owner_id=user_id_gamma
    )

    query = """query SelectPlaces($userOwner: String) {
                selectPlaces(userOwner: $userOwner) {
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
                    }"""
    response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": query,
            "variables": {
                "includeMyPlaces": False,
                "userOwner": encode_gql_id("UserType", user_id_gamma),
            },
        },
        headers={"Authorization": encode_gql_id("UserType", user_id_beta)},
    )
    assert not response.json().get("errors")
    json_response = [
        x["node"] for x in response.json()["data"]["selectPlaces"]["edges"]
    ]
    assert [encode_gql_id("PlaceType", place_gamma)] == [x["id"] for x in json_response]
