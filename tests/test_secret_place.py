import pytest

from gql.gql_id import encode_gql_id, assert_gql_id
from models.db_models import Category
from tests.creator import SecretExtraData
from utils.config import settings as s
import sqlalchemy as sa


@pytest.mark.asyncio
async def test_select_secret_vs_regular(
    dbsession, creator, test_client_graph, economy_values
):
    user_creator_id = await creator.create_user("Creator")
    user_tester_id = await creator.create_user("Tester")
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
        owner_id=user_creator_id,
        description="A romantic place",
        longitude=20,
        latitude=20,
        secret_extra_data=extra_data,
    )
    other_category_id = await creator.create_category("Auto")
    other_place_id = await creator.create_place(
        name="Bently car shop",
        category_id=other_category_id,
        owner_id=user_creator_id,
        description="Extremely pricey!",
        longitude=21,
        latitude=42,
    )
    coded_secret_id = encode_gql_id("PlaceType", secret_place_id)
    coded_regular_id = encode_gql_id("PlaceType", other_place_id)
    query = """query SecretsTest($secretsFilter: SecretPlacesFilterEnum, $openedSecretPlaces: Boolean) {
                  selectPlaces(secretsFilter: $secretsFilter, openedSecretPlaces: $openedSecretPlaces) {
                    edges {
                      node {
                        id
                        name
                        ownerId
                        categoryData {
                          name
                          mark
                          id
                        }
                        secretExtraField {
                          id
                          foodSuggestion
                          timeSuggestion
                          companySuggestion
                          musicSuggestion
                          extraSuggestion
                        }
                        coordinateLatitude
                        coordinateLongitude
                        isOpenedForUser
                      }
                    }
                  }
                }"""
    regulars_response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": query,
            "variables": {
                "secretsFilter": "REGULAR",
                "openedSecretPlaces": None,
            },
        },
        headers={"Authorization": encode_gql_id("UserType", user_tester_id)},
    )
    secrets_response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": query,
            "variables": {
                "secretsFilter": "SECRET",
                "openedSecretPlaces": None,
            },
        },
        headers={"Authorization": encode_gql_id("UserType", user_tester_id)},
    )
    all_response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": query,
            "variables": {
                "secretsFilter": "ALL",
                "openedSecretPlaces": None,
            },
        },
        headers={"Authorization": encode_gql_id("UserType", user_tester_id)},
    )
    no_filter_response = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": query,
            "variables": {
                "secretsFilter": None,
                "openedSecretPlaces": None,
            },
        },
        headers={"Authorization": encode_gql_id("UserType", user_tester_id)},
    )
    assert "errors" not in all_response.json()
    data = all_response.json()["data"]["selectPlaces"]["edges"]
    data = {
        "no_filter_response": no_filter_response,
        "all_response": all_response,
        "secrets_response": secrets_response,
        "regulars_response": regulars_response,
    }
    data = {k: v.json()["data"]["selectPlaces"]["edges"] for k, v in data.items()}
    selected_attributes = {
        key: [
            {
                "id": x["node"]["id"],
                "category": x["node"]["categoryData"]["name"],
                "opened": x["node"]["isOpenedForUser"],
            }
            for x in results
        ]
        for key, results in data.items()
    }
    assert len(selected_attributes["no_filter_response"]) == 2
    assert len(selected_attributes["all_response"]) == 2
    assert (
        selected_attributes["all_response"] == selected_attributes["no_filter_response"]
    )
    assert set([res["id"] for res in selected_attributes["all_response"]]) == {
        coded_secret_id,
        coded_regular_id,
    }

    assert len(selected_attributes["secrets_response"]) == 1
    assert len(selected_attributes["regulars_response"]) == 1

    assert selected_attributes["secrets_response"][0]["id"] == coded_secret_id
    assert selected_attributes["regulars_response"][0]["id"] == coded_regular_id


@pytest.mark.asyncio
async def test_secret_place_actions(
    dbsession, creator, test_client_graph, economy_values
):
    user_creator_id = await creator.create_user("Creator", coins=500)
    user_tester_id = await creator.create_user("Tester", coins=1000)
    secret_id = (
        (
            await dbsession.execute(
                sa.select(Category.id).where(Category.mark == "secret")
            )
        )
        .fetchone()
        .id
    )
    query = """mutation AddPlace($placeData: PlaceDataInput, $secretPlaceExtra: SecretPlaceExtraInput) {
                  addPlace(placeData: $placeData, secretPlaceExtra: $secretPlaceExtra) {
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
                      secretExtraField {
                        companySuggestion
                        extraSuggestion
                        foodSuggestion
                        musicSuggestion
                        timeSuggestion
                      }
                    }
                  }
                }"""
    secret_extra = {
        "companySuggestion": "Ur Bois",
        "extraSuggestion": "Take more ammo with you",
        "foodSuggestion": "Hot dogs and fries",
        "musicSuggestion": "ERONDONDON",
        "timeSuggestion": "Anytime",
    }
    variables = {
        "placeData": {
            "name": "CJ House",
            "categoryId": "Q2F0ZWdvcnlUeXBlOjM=",
            "coordinateLongitude": 19.84,
            "coordinateLatitude": 21.42,
            "address": "Groove St 4",
            "description": "Best cars of the LosSantos",
        },
        "secretPlaceExtra": secret_extra,
    }

    new_secret_place = await test_client_graph.post(
        "http://test/graphql",
        json={
            "query": query,
            "variables": variables,
        },
        headers={"Authorization": encode_gql_id("UserType", user_creator_id)},
    )
    aaa = 5
