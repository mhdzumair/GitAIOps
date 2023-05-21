from fastapi import APIRouter, HTTPException, Request
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from services.schemas import GraphQLQuery
from utils.api_config import get_api_token

router = APIRouter()


@router.post("/", operation_id="github_graphql_api")
async def github_graphql_api(request: Request, query: GraphQLQuery):
    """
    Execute a GraphQL query on GitHub.
    Provide a GraphQLQuery object with the query string.
    The result will be the response from the GitHub API.
    """

    github_graphql_url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {get_api_token('github', request)}"}

    transport = AIOHTTPTransport(url=github_graphql_url, headers=headers)

    # Create the GraphQL client
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        # Define the GraphQL query
        gql_query = gql(query.query)

        # Execute the query
        try:
            result = await session.execute(gql_query)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error executing GraphQL query: {e}"
            )

    return result
