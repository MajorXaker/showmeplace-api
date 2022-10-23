import json

from httpx import AsyncClient


def overdrive():

    query = """
            query ExampleQuery($includeMyPlaces: Boolean, $secretsFilter: SecretPlacesFilterEnum, $decayFilter: DecayingPlacesFilterEnum, $after: String, $first: Int) {
              selectPlaces(includeMyPlaces: $includeMyPlaces, secretsFilter: $secretsFilter, decayFilter: $decayFilter, after: $after, first: $first) {
                edges {
                  node {
                    id
                    name
                    description
                    coordinateLongitude
                    coordinateLatitude
                  }
                }
                pageInfo {
                  endCursor
                }
              }
            }

            """

    variables_raw = {
        "includeMyPlaces": True,
        "secretsFilter": "ALL",
        "decayFilter": "ALL",
        "after": None,
        "first": 1000,
    }

    # variables = json.dumps(variables_raw)
    #
    #
    # api_response = self.simulate_post(
    #     "/graphql",
    #     json={
    #         "operationName": "ExampleQuery",
    #         "query": query,
    #         "variables": variables
    #         ),
    #     },
    # )
    #
    # async with AsyncClient(app=test_client_rest, base_url="http://test") as cl:
    #     response = await cl.post(
    #         "http://test/aqa/create-sale",
    #         json=create_sale_data,
    #     )


if __name__ == "__main__":
    pass
