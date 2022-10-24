import json
import asyncio
import httpx

URL_TO_OVERDRIVE = "http://127.0.0.1:8000/graphql"


async def overdrive():
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

    async with httpx.AsyncClient() as c:
        auth_response = await c.post(
            url=URL_TO_OVERDRIVE,
            json={
                "query": query,
                "variables": variables_raw,
            },
            headers={"Authorization": "VXNlclR5cGU6MQ=="} # UserType:1
            # auth=(
            #     settings.INTERNAL_GQL_USERNAME,
            #     settings.INTERNAL_GQL_PASSWORD,
            # ), # TODO maybe use this?
        )
    data = json.loads(auth_response.content)

    aaa = 5

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
    asyncio.run(overdrive())
