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
    user_creator_id = await creator.create_user("Creator")
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
    idk_response = await test_client_graph.post(
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
        "idk_response": idk_response,
        "all_response": all_response,
        "secrets_response": secrets_response,
        "regulars_response": regulars_response,
    }
    data = {k: v.json()["data"]["selectPlaces"]["edges"] for k, v in data.items()}
    aa = 5
    temp = {
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
